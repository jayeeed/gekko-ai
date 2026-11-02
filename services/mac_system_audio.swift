// Streams macOS system output as 48 kHz mono signed 16-bit PCM on stdout.
// Diagnostic messages go to stderr; no audio is written to disk.
import Foundation
import ScreenCaptureKit
import CoreMedia
import AudioToolbox

final class SystemAudioOutput: NSObject, SCStreamOutput {
    private var pending: [Int16] = []
    private let packetSamples = 2048
    private var reportedUnsupportedFormat = false

    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .audio, sampleBuffer.isValid else { return }
        guard let format = sampleBuffer.formatDescription?.audioStreamBasicDescription,
              format.mFormatID == kAudioFormatLinearPCM,
              format.mFormatFlags & kAudioFormatFlagIsFloat != 0,
              format.mBitsPerChannel == 32,
              format.mSampleRate == 48000
        else {
            if !reportedUnsupportedFormat {
                fputs("Unsupported system audio format\n", stderr)
                reportedUnsupportedFormat = true
                exit(2)
            }
            return
        }

        _ = try? sampleBuffer.withAudioBufferList { (audioBufferList, _) -> Void in
            let buffers = UnsafeMutableAudioBufferListPointer(
                UnsafeMutablePointer(mutating: audioBufferList.unsafePointer)
            )
            let channels = Int(format.mChannelsPerFrame)
            let frames = CMSampleBufferGetNumSamples(sampleBuffer)
            let planar = format.mFormatFlags & kAudioFormatFlagIsNonInterleaved != 0
            guard channels > 0, channels <= 8, frames > 0, frames <= 8192 else { return }

            for frame in 0..<frames {
                var total: Float = 0
                var used = 0
                if planar {
                    for channel in 0..<min(channels, buffers.count) {
                        let buffer = buffers[channel]
                        guard let data = buffer.mData, frame * 4 < Int(buffer.mDataByteSize) else { continue }
                        total += data.assumingMemoryBound(to: Float.self)[frame]
                        used += 1
                    }
                } else if let data = buffers.first?.mData {
                    let sampleCount = Int(buffers[0].mDataByteSize) / 4
                    for channel in 0..<channels where frame * channels + channel < sampleCount {
                        total += data.assumingMemoryBound(to: Float.self)[frame * channels + channel]
                        used += 1
                    }
                }
                let average = used > 0 ? total / Float(used) : 0
                let mono = average.isFinite ? max(-1, min(1, average)) : 0
                pending.append(Int16(mono * 32767))
            }

            while pending.count >= packetSamples {
                let packet = Array(pending.prefix(packetSamples))
                pending.removeFirst(packetSamples)
                packet.withUnsafeBufferPointer { samples in
                    guard let pointer = samples.baseAddress else { return }
                    FileHandle.standardOutput.write(Data(bytes: pointer, count: packetSamples * 2))
                }
            }
        }
    }
}

var activeStream: SCStream?
var activeOutput: SystemAudioOutput?
let expectedParentPID = Int32(CommandLine.arguments.dropFirst().first ?? "") ?? getppid()

Task {
    while true {
        try? await Task.sleep(for: .seconds(1))
        if getppid() != expectedParentPID { exit(0) }
    }
}

Task {
    do {
        let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
        guard let display = content.displays.first else { throw NSError(domain: "GekkoSystemAudio", code: 1) }
        let filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
        let configuration = SCStreamConfiguration()
        configuration.capturesAudio = true
        configuration.excludesCurrentProcessAudio = true
        configuration.sampleRate = 48000
        configuration.channelCount = 2
        configuration.width = 2
        configuration.height = 2

        let output = SystemAudioOutput()
        let stream = SCStream(filter: filter, configuration: configuration, delegate: nil)
        try stream.addStreamOutput(output, type: .audio, sampleHandlerQueue: DispatchQueue(label: "gekko.system.audio"))
        try await stream.startCapture()
        activeOutput = output
        activeStream = stream
        fputs("System audio capture ready\n", stderr)
    } catch {
        fputs("System audio capture failed: \(error)\n", stderr)
        exit(1)
    }
}
RunLoop.main.run()
