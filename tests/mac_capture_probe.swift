// Run with: swift tests/mac_capture_probe.swift
// Requires Screen Recording permission for the Terminal running this probe.
import AppKit
import ScreenCaptureKit
import CoreMedia
import CoreImage

final class FrameReceiver: NSObject, SCStreamOutput {
    let ready = DispatchSemaphore(value: 0)
    var image: CGImage?

    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .screen, image == nil,
              let buffer = CMSampleBufferGetImageBuffer(sampleBuffer),
              let frame = CIContext().createCGImage(CIImage(cvImageBuffer: buffer), from: CIImage(cvImageBuffer: buffer).extent)
        else { return }
        image = frame
        ready.signal()
    }
}

func greenSamples(_ image: CGImage) -> Int {
    let bitmap = NSBitmapImageRep(cgImage: image)
    var count = 0
    for y in stride(from: 0, to: bitmap.pixelsHigh, by: 8) {
        for x in stride(from: 0, to: bitmap.pixelsWide, by: 8) {
            guard let color = bitmap.colorAt(x: x, y: y)?.usingColorSpace(.deviceRGB) else { continue }
            if color.greenComponent > 0.65 &&
                color.greenComponent > color.redComponent * 1.5 &&
                color.greenComponent > color.blueComponent * 1.5 {
                count += 1
            }
        }
    }
    return count
}

func captureWithSystemTool(_ windowID: Int?, to url: URL) throws -> (Int32, Int) {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/sbin/screencapture")
    process.arguments = ["-x"] + (windowID.map { ["-l", String($0)] } ?? []) + [url.path]
    try process.run()
    process.waitUntilExit()
    defer { try? FileManager.default.removeItem(at: url) }
    guard process.terminationStatus == 0,
          let image = NSImage(contentsOf: url),
          let data = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: data),
          let cgImage = bitmap.cgImage else {
        return (process.terminationStatus, 0)
    }
    return (process.terminationStatus, greenSamples(cgImage))
}

func captureWithScreenCaptureKit() async throws -> Int {
    let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
    guard let display = content.displays.first else { throw NSError(domain: "capture-probe", code: 1) }
    let filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
    let configuration = SCStreamConfiguration()
    configuration.width = display.width
    configuration.height = display.height
    let image = try await SCScreenshotManager.captureImage(contentFilter: filter, configuration: configuration)
    return greenSamples(image)
}

func captureStreamFrame() async throws -> Int {
    let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
    guard let display = content.displays.first else { throw NSError(domain: "capture-probe", code: 2) }
    let filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
    let configuration = SCStreamConfiguration()
    configuration.width = display.width
    configuration.height = display.height
    let receiver = FrameReceiver()
    let stream = SCStream(filter: filter, configuration: configuration, delegate: nil)
    try stream.addStreamOutput(receiver, type: .screen, sampleHandlerQueue: DispatchQueue(label: "gekko.capture.probe"))
    try await stream.startCapture()
    let received = receiver.ready.wait(timeout: .now() + 5) == .success
    try await stream.stopCapture()
    guard received, let image = receiver.image else { throw NSError(domain: "capture-probe", code: 3) }
    return greenSamples(image)
}

let app = NSApplication.shared
app.setActivationPolicy(.regular)
let window = NSWindow(
    contentRect: NSRect(x: 180, y: 180, width: 300, height: 200),
    styleMask: [.titled], backing: .buffered, defer: false
)
window.title = "Gekko capture probe"
window.backgroundColor = NSColor(calibratedRed: 0.05, green: 0.95, blue: 0.05, alpha: 1)
window.level = .statusBar
window.makeKeyAndOrderFront(nil)
app.activate(ignoringOtherApps: true)

Task {
    do {
        let base = FileManager.default.temporaryDirectory
        var results: [(String, Int32, Int, Int32, Int, Int)] = []
        for (label, sharingType) in [("control", NSWindow.SharingType.readOnly), ("protected", .none)] {
            await MainActor.run { window.sharingType = sharingType }
            try await Task.sleep(for: .milliseconds(600))
            let (displayStatus, displayGreen) = try captureWithSystemTool(nil, to: base.appendingPathComponent("gekko-\(label)-display.png"))
            let windowID = await MainActor.run { window.windowNumber }
            let (windowStatus, _) = try captureWithSystemTool(windowID, to: base.appendingPathComponent("gekko-\(label)-window.png"))
            let sckGreen = try await captureWithScreenCaptureKit()
            let streamGreen = try await captureStreamFrame()
            results.append((label, displayStatus, displayGreen, windowStatus, sckGreen, streamGreen))
            print("\(label): display_status=\(displayStatus), display_green=\(displayGreen), window_status=\(windowStatus), sck_green=\(sckGreen), stream_green=\(streamGreen)")
        }
        let control = results[0]
        let protected = results[1]
        let passed = control.1 == 0 && control.2 > 10 && control.3 == 0 && control.4 > 10 && control.5 > 10 &&
            protected.1 == 0 && protected.2 < 10 && protected.3 != 0 && protected.4 < 10 && protected.5 < 10
        print(passed ? "PASS" : "FAIL")
        exit(passed ? 0 : 1)
    } catch {
        print("FAIL: \(error)")
        exit(1)
    }
}
RunLoop.main.run()
