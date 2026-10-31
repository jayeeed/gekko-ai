# Tech Context: Gekko AI

## Tech Stack
- **Backend**: Python 3.10+ (FastAPI, Uvicorn, WebSockets, asyncio)
- **GUI Framework**: pywebview with Win32 / Cocoa native webview
- **OS Automation & Window Management**: ctypes, Win32 API (`user32.dll`, `dwmapi.dll`), `pynput`
- **Speech-to-Text**: Deepgram SDK / Live WebSocket audio streaming
- **LLM Integrations**: Cerebras Cloud SDK, Groq SDK, Google Generative AI (Gemini), OpenRouter, OpenAI
- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Modern CSS3 (Grid/Flexbox, CSS variables)
- **Tooling & Environments**: Python venv, RTK CLI for token-efficient commands

## Runtime & Launch Scripts
- `run.bat`: Windows batch script for automated environment setup and launch.
- `silent_run.vbs`: VBScript wrapper for launching without visible console windows.
- `main.py`: Main entry point orchestrating FastAPI server thread and pywebview GUI window.
- `window_manager.py`: OS-level window manipulation for transparency, click-through, and capture exclusion.

