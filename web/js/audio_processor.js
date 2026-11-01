// --- web/js/audio_processor.js ---

/**
 * Mixed audio processor that combines microphone and system audio
 * while tracking volume levels for speaker detection.
 */
class MixedProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.micInputIndex = 0;
        this.systemInputIndex = 1;
        // 2048 samples at 48 kHz is about 43 ms per packet.
        this.packet = new Int16Array(2048);
        this.packetLength = 0;
        this.micLevelSum = 0;
        this.systemLevelSum = 0;
    }

    process(inputs, outputs, parameters) {
        // We expect two inputs: [0] = microphone, [1] = system audio
        const micInput = inputs[0] && inputs[0][0] ? inputs[0][0] : new Float32Array(128);
        const systemInput = inputs[1] && inputs[1][0] ? inputs[1][0] : new Float32Array(128);
        
        const frameLength = Math.max(micInput.length, systemInput.length);
        if (frameLength === 0) return true;

        // Mix and encode into small packets to avoid flooding the WebSocket.
        for (let i = 0; i < frameLength; i++) {
            const micSample = i < micInput.length ? micInput[i] : 0;
            const systemSample = i < systemInput.length ? systemInput[i] : 0;
            const s = Math.max(-1, Math.min(1, (micSample + systemSample) * 0.7));
            this.packet[this.packetLength++] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            this.micLevelSum += Math.abs(micSample);
            this.systemLevelSum += Math.abs(systemSample);

            if (this.packetLength === this.packet.length) {
                const pcmData = this.packet;
                this.port.postMessage({
                    audioData: pcmData.buffer,
                    micLevel: this.micLevelSum / pcmData.length,
                    systemLevel: this.systemLevelSum / pcmData.length
                }, [pcmData.buffer]);
                this.packet = new Int16Array(2048);
                this.packetLength = 0;
                this.micLevelSum = 0;
                this.systemLevelSum = 0;
            }
        }

        return true;
    }
}

registerProcessor('mixed-processor', MixedProcessor);
