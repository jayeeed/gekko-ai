// --- audio_handler.js ---
// This module handles all interactions with the Web Media APIs
// for capturing and processing audio via an AudioWorklet.

import { devLog, devWarn, devError } from './config.js';
import muteManager from './mute-manager.js';

let audioContext = null;
let micStream = null;
let systemStream = null;
let micGainNode = null;
let screenVideoTrack = null; // Store video track for screenshot reuse

/**
 * Requests permission to use the microphone and populates the dropdown.
 * @returns {Promise<boolean>} True if permission was granted, false otherwise.
 */
export async function setupMicrophone() {
    const micSelect = document.getElementById('mic-select');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        stream.getTracks().forEach(track => track.stop());

        const devices = await navigator.mediaDevices.enumerateDevices();
        const audioDevices = devices.filter(device => device.kind === 'audioinput');

        if (audioDevices.length === 0) return false;

        micSelect.innerHTML = '';
        audioDevices.forEach(device => {
            const option = document.createElement('option');
            option.value = device.deviceId;
            option.textContent = device.label || `Microphone ${micSelect.options.length + 1}`;
            micSelect.appendChild(option);
        });
        
        micSelect.disabled = false;
        return true;
    } catch (err) {
        devError("Error setting up microphone:", err);
        return false;
    }
}

/**
 * Starts audio processing by setting up the AudioContext, loading the worklet,
 * and connecting the audio streams.
 * @param {string} micId - The deviceId of the selected microphone.
 * @param {function} onAudioData - Callback function to handle the processed PCM audio data.
 * @returns {Promise<boolean>} True if processing started successfully.
 */
export async function startAudioProcessing(micId, onAudioData) {
    try {
        // 1. Get Audio Streams with Tiered Fallback
        
        // --- Step 1A: Get Microphone Stream ---
        try {
            micStream = await navigator.mediaDevices.getUserMedia({ audio: { deviceId: { exact: micId } } });
            devLog("✅ Microphone stream acquired");
        } catch (err) {
            devError("❌ Failed to acquire microphone stream:", err);
            return { success: false, error: "Microphone permission denied or device not found." };
        }

        // --- Step 1B: Get System/Screen Stream with Fallback ---
        let systemAudioAcquired = false;
        let screenVideoAcquired = false;

        const useNativeSystemAudio = navigator.platform.toUpperCase().includes('MAC');
        try {
            devLog("📡 Attempting to capture screen video and system audio...");
            systemStream = await navigator.mediaDevices.getDisplayMedia({ 
                video: { cursor: "always" }, 
                audio: !useNativeSystemAudio
            });
            systemAudioAcquired = systemStream.getAudioTracks().length > 0;
            screenVideoAcquired = systemStream.getVideoTracks().length > 0;
            if (systemAudioAcquired) {
                devLog("✅ Full screen and system audio capture acquired");
            } else {
                devWarn("⚠️ Display capture returned no system audio track");
            }
        } catch (err) {
            if (useNativeSystemAudio) {
                devWarn("⚠️ Screen video capture unavailable; native system audio can still run", err);
            } else {
                devWarn("⚠️ Could not capture system audio. Falling back to video-only...", err);
                try {
                    systemStream = await navigator.mediaDevices.getDisplayMedia({
                        video: { cursor: "always" },
                        audio: false
                    });
                    screenVideoAcquired = systemStream.getVideoTracks().length > 0;
                    devLog("✅ Screen video capture acquired (no system audio)");
                } catch (err2) {
                    devError("❌ Screen capture completely denied:", err2);
                }
            }
        }

        if (!micStream) {
            stopAudioProcessing();
            return { success: false, error: "Microphone stream is required." };
        }

        // 2. Setup AudioContext and Worklet
        // Force 48kHz to match Deepgram's configuration and avoid pitch issues
        audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: 48000
        });
        console.log(`🎵 AudioContext: ${audioContext.sampleRate}Hz`); 
        await audioContext.audioWorklet.addModule('/static/js/audio_processor.js');
        
        // 3. Create a single mixed processor for better diarization
        // Explicitly define 2 inputs: index 0 for Mic, index 1 for System
        const mixedProcessor = new AudioWorkletNode(audioContext, 'mixed-processor', {
            numberOfInputs: 2,
            numberOfOutputs: 1,
            outputChannelCount: [1]
        });
        // Keep the worklet in the active audio graph without playing captured audio.
        const silentOutput = audioContext.createGain();
        silentOutput.gain.value = 0;
        mixedProcessor.connect(silentOutput);
        silentOutput.connect(audioContext.destination);

        // Handle mixed audio with mute-aware speaker detection
        let audioProcessingCounter = 0; // For throttled logging
        
        mixedProcessor.port.onmessage = (event) => {
            // If universally muted, drop all audio data immediately.
            if (muteManager.isAudioPaused()) {
                if (audioProcessingCounter % 200 === 0) {
                    devLog(`⏸️ Audio processing paused due to universal mute.`);
                }
                audioProcessingCounter++;
                return;
            }

            const { audioData, micLevel, systemLevel } = event.data;
            let speakerHint;

            if (muteManager.isMicrophoneMuted()) {
                // When microphone is muted, all audio is from the interviewer.
                speakerHint = 'system';
            } else {
                // When unmuted, distinguish based on volume.
                // Improved logic: if systemLevel is significant, prioritize it as 'system'
                speakerHint = systemLevel > (micLevel * 1.5) ? 'system' : 'microphone';
            }

            audioProcessingCounter++;
            onAudioData(audioData, speakerHint);
        };

        // 4. Connect sources to the mixed processor with mute control
        const micSource = audioContext.createMediaStreamSource(micStream);
        
        // Create gain node for microphone muting
        micGainNode = audioContext.createGain();
        updateMicGainNode(); // Set initial gain based on mute manager state
        
        // Listen for future changes
        muteManager.on('microphoneMuteChange', updateMicGainNode);
        
        // Connect mic through gain node for mute control to input 0
        micSource.connect(micGainNode);
        micGainNode.connect(mixedProcessor, 0, 0);
        
        // System audio connects directly to input 1 (if available)
        if (systemStream && systemStream.getAudioTracks().length > 0) {
            try {
                const systemSource = audioContext.createMediaStreamSource(systemStream);
                systemSource.connect(mixedProcessor, 0, 1);
                devLog("✅ System audio source connected to processor input 1");
            } catch (err) {
                devWarn("⚠️ Could not connect system audio source:", err);
                systemAudioAcquired = false;
            }

        } else if (!useNativeSystemAudio) {
            devWarn("ℹ️ No system audio track available; remote participants will not be transcribed.");
        }

        // Keep video available for screenshots even when display audio is absent.
        if (systemStream) {
            const videoTracks = systemStream.getVideoTracks();
            if (videoTracks.length > 0) {
                screenVideoTrack = videoTracks[0];
                devLog("📹 Screen video track stored for screenshot reuse");
                screenVideoAcquired = true;
            } else {
                devWarn("⚠️ No video track found in display media stream");
                screenVideoAcquired = false;
            }
        }

        devLog("✅ Audio processing started");
        return { 
            success: true, 
            systemAudio: systemAudioAcquired, 
            screenVideo: screenVideoAcquired 
        };

    } catch (err) {
        devError("❌ Error in startAudioProcessing lifecycle:", err);
        stopAudioProcessing();
        return { success: false, error: err.message };
    }
}

/**
 * Updates the microphone gain node based on the central mute manager state.
 */
function updateMicGainNode() {
    if (!micGainNode || !audioContext) return;
    
    const isMuted = muteManager.isMicrophoneMuted();
    const targetGain = isMuted ? 0 : 1;
    
    // Smooth transition to avoid audio pops
    micGainNode.gain.setTargetAtTime(targetGain, audioContext.currentTime, 0.05);
    devLog(`🎤 Microphone gain set to ${targetGain} based on mute manager.`);
}

// --- Legacy Functions (now wrappers for MuteManager) ---
// These are kept for backward compatibility with other modules that might call them.

/**
 * @deprecated Use muteManager.setMicrophoneMute(mute) instead.
 */
export function setMicrophoneMute(mute) {
    muteManager.setMicrophoneMute(mute);
    return muteManager.isMicrophoneMuted();
}

/**
 * @deprecated Use muteManager.isMicrophoneMuted() instead.
 */
export function isMicrophoneMuted() {
    return muteManager.isMicrophoneMuted();
}

/**
 * @deprecated Use muteManager.toggleMicrophoneMute() instead.
 */
export function toggleMicrophoneMute() {
    return muteManager.toggleMicrophoneMute();
}

/**
 * @deprecated Use muteManager.getMuteStatus() instead.
 */
export function getAudioProcessingMode() {
    return muteManager.getMuteStatus();
}

/**
 * Gets the screen video track for screenshot capture.
 * @returns {MediaStreamTrack|null} The screen video track if available.
 */
export function getScreenVideoTrack() {
    return screenVideoTrack;
}

/**
 * Checks if screen sharing is available for screenshots.
 * @returns {boolean} True if screen video track is available and active.
 */
export function isScreenSharingAvailable() {
    return screenVideoTrack && screenVideoTrack.readyState === 'live';
}

/**
 * Stops all audio streams and closes the AudioContext.
 */
export function stopAudioProcessing() {
    console.log("Stopping audio processing.");
    if (micStream) {
        micStream.getTracks().forEach(track => track.stop());
        micStream = null;
    }
    if (systemStream) {
        systemStream.getTracks().forEach(track => track.stop());
        systemStream = null;
    }
    if (screenVideoTrack) {
        screenVideoTrack.stop();
        screenVideoTrack = null;
        console.log("📹 Screen video track stopped");
    }
    if (audioContext && audioContext.state !== 'closed') {
        audioContext.close();
        audioContext = null;
    }
    
    // Reset mute state in the central manager
    muteManager.setMicrophoneMute(true);
    muteManager.setUniversalMute(false);
    micGainNode = null;
}
