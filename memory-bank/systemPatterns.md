# System Patterns: Gekko AI

## Architecture Overview
The application follows a decoupled desktop-web hybrid architecture:

```
+-----------------------------------------------------------+
|                   PyWebView Window                        |
|   Frontend: HTML5 / Modern CSS / Vanilla ES6 JavaScript   |
|   - Brand: "Gekko AI" / "GEKKO"                           |
|   - Live Cockpit UI & Markdown Streaming                   |
+-----------------------------^-----------------------------+
                              | WebSocket & REST (FastAPI)
+-----------------------------v-----------------------------+
|                     FastAPI Backend                       |
|   - main.py: Application lifecycle & Webview supervisor   |
|   - api/: Session management, WebSockets, config APIs     |
|   - services/: STT (Deepgram), LLMs (Cerebras, Groq, etc.)|
|   - core/: Prompts, provider dispatch, env utils          |
+-----------------------------^-----------------------------+
                              | OS Win32 API Interop
+-----------------------------v-----------------------------+
|                Windows OS / Window Manager                |
|   - window_manager.py: FindWindowW("Gekko AI")            |
|   - Stealth flags: WDA_EXCLUDEFROMCAPTURE, WS_EX_LAYERED  |
|   - Global Hotkeys via pynput/ctypes                      |
+-----------------------------------------------------------+
```

## Key Technical Decisions & Patterns
1. **Window Identification**: The window manager targets the window title `"Gekko AI"`. All window matching, process naming, and inter-process command files (`gekko_command.json`) must remain synchronized.
2. **Branding Convention**:
   - Product Name: **Gekko AI**
   - Moniker / Short Brand: **Gekko**
   - CSS / Header Logo: `GEKKO`
   - Command File: `gekko_command.json`
3. **Frontend Architecture**: Modular JavaScript using custom events, streaming markdown parser, audio worklets, and hotkey dispatcher.
4. **Resilience & Fallback**: Provider rotation across multiple API keys and fallback across Cerebras -> Groq -> Gemini -> OpenRouter.

