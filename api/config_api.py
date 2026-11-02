import orjson
import aiofiles
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.config import settings
import window_manager
from services.llm_service import verify_provider_connection
from services.vision_service import verify_vision_provider_connection
from core.env_utils import env_manager
import shutil
import os
import sys

from core.provider_service import load_providers_config, save_providers_config

router = APIRouter()

class TransparencyRequest(BaseModel):
    transparency: float  # 0.0 to 1.0

class TransparencyPercentRequest(BaseModel):
    percent: int  # 0 to 100

class ProviderVerifyRequest(BaseModel):
    name: str
    model: str

class SaveProvidersRequest(BaseModel):
    providers: list

class SaveKeyRequest(BaseModel):
    key: str

@router.get("/api/config")
async def get_config():
    """
    Returns frontend configuration values including DEV_MODE.
    This allows JavaScript to access centralized config values.
    """
    return {
        "DEV_MODE": settings.DEV_MODE,
        "LOG_LEVEL": settings.LOG_LEVEL,
        "CAPTURE_PROTECTION_ENABLED": window_manager.window_manager.capture_protection_applied,
        "CAPTURE_PROTECTION_LIMITED": sys.platform == "darwin"
    }


@router.get("/api/audio-diagnostics")
async def get_audio_diagnostics():
    """Local level-only counters for debugging capture; never returns audio content."""
    from api.session_manager import session_manager

    sessions = []
    for session in session_manager.active_sessions.values():
        bridge = session.native_audio
        sessions.append({
            "connected": session.websocket is not None,
            "microphone_packets": session.microphone_packets_received,
            "deepgram_connected": bool(session.stt_manager and session.stt_manager.is_connected),
            "system_deepgram_connected": bool(session.system_stt_manager and session.system_stt_manager.is_connected),
            "system_capture_running": bool(bridge and bridge.process and bridge.process.returncode is None),
            "system_packets": bridge.packets_received if bridge else 0,
            "system_nonzero_packets": bridge.nonzero_packets_received if bridge else 0,
            "system_packets_sent": session.system_packets_sent,
            "system_final_transcripts": session.system_final_transcripts,
            "microphone_final_transcripts": session.microphone_final_transcripts,
        })
    return {"sessions": sessions}

@router.get("/api/ai-providers")
async def get_ai_providers():
    """
    Reads provider configurations (with models and keys loaded from .env)
    and returns a client-safe list of providers to the frontend.
    """
    try:
        providers = load_providers_config()
        
        # Sanitize the data before sending to the client
        client_safe_providers = [
            {
                "name": p.get("name"),
                "models": p.get("models", []),
                "visionModels": p.get("visionModels", []),
                "supportsVision": p.get("supportsVision", False),
                "defaultPrimary": p.get("defaultPrimary", False),
                "defaultSecondary": p.get("defaultSecondary", False),
                "defaultVisionPrimary": p.get("defaultVisionPrimary", False),
                "defaultVisionSecondary": p.get("defaultVisionSecondary", False),
                "defaultModel": p.get("defaultModel"),
                "defaultVisionModel": p.get("defaultVisionModel"),
                # Keep legacy default for backward compatibility
                "default": p.get("defaultPrimary", False)
            }
            for p in providers
        ]
        return client_safe_providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading provider config: {e}")

@router.get("/api/ai-providers/full")
async def get_ai_providers_full():
    """
    Returns editable provider metadata without sending stored API keys to the UI.
    """
    try:
        providers = load_providers_config()
        return [{**{k: v for k, v in p.items() if k not in ("apiKey", "apiKeys")},
                 "apiKeys": [], "keyCount": len(p.get("apiKeys") or [])} for p in providers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading full provider config: {e}")

@router.post("/api/save-ai-providers")
async def save_ai_providers(request: SaveProvidersRequest):
    """Saves provider API keys and models to .env and metadata to ai_providers.json."""
    try:
        success = save_providers_config(request.providers)
        if success:
            return {"success": True, "message": "AI Providers saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save provider config")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving provider config: {e}")

@router.get("/api/deepgram-key")
async def get_deepgram_key():
    """Reports whether a Deepgram key is stored without returning it."""
    key = env_manager.get_value("DEEPGRAM_API_KEY")
    return {"configured": bool(key)}

@router.post("/api/save-deepgram-key")
async def save_deepgram_key(request: SaveKeyRequest):
    """Updates the DEEPGRAM_API_KEY in the .env file."""
    try:
        success = env_manager.update_key("DEEPGRAM_API_KEY", request.key)
        if success:
            return {"success": True, "message": "Deepgram API key saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update .env file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving Deepgram key: {e}")

@router.post("/api/verify-provider")
async def verify_ai_provider(request: ProviderVerifyRequest):
    """
    Verifies a connection to the selected AI provider.
    Tries all available apiKeys if the first one fails.
    """
    try:
        providers = load_providers_config()
        provider_config = next((p for p in providers if p["name"] == request.name), None)

        if not provider_config:
            raise HTTPException(status_code=404, detail=f"Provider '{request.name}' not found.")

        # Get all available keys, with fallback to single apiKey
        api_keys = provider_config.get("apiKeys", [provider_config.get("apiKey", "")])
        if not api_keys:
            api_keys = [provider_config.get("apiKey", "")]

        # Try each key until one works
        for i, key in enumerate(api_keys):
            if not key or key.startswith("YOUR_"):
                continue
            is_valid = await verify_provider_connection(
                base_url=provider_config.get("baseURL"),
                api_key=key,
                model_name=request.model
            )
            if is_valid:
                return {"success": True}
            print(f"⚠️ Key {i+1}/{len(api_keys)} failed for {request.name}, trying next...")
        
        return {"success": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify provider: {e}")

@router.post("/api/verify-vision-provider")
async def verify_vision_ai_provider(request: ProviderVerifyRequest):
    """
    Verifies a connection to the selected vision AI provider.
    Tries all available apiKeys if the first one fails.
    """
    try:
        providers = load_providers_config()
        provider_config = next((p for p in providers if p["name"] == request.name), None)

        if not provider_config:
            raise HTTPException(status_code=404, detail=f"Provider '{request.name}' not found.")

        if not provider_config.get("supportsVision", False):
            raise HTTPException(status_code=400, detail=f"Provider '{request.name}' does not support vision.")

        # Check if model exists in visionModels and extract model config (handle both string and object formats)
        vision_models = provider_config.get("visionModels", [])
        model_config = None
        
        for vision_model in vision_models:
            if isinstance(vision_model, str) and vision_model == request.model:
                model_config = {"modelName": vision_model}  # Normalize to dict
                break
            elif isinstance(vision_model, dict) and vision_model.get("modelName") == request.model:
                model_config = vision_model
                break
        
        if not model_config:
            raise HTTPException(status_code=400, detail=f"Model '{request.model}' is not a vision model for '{request.name}'.")

        # Get all available keys, with fallback to single apiKey
        api_keys = provider_config.get("apiKeys", [provider_config.get("apiKey", "")])
        if not api_keys:
            api_keys = [provider_config.get("apiKey", "")]

        # Try each key until one works
        for i, key in enumerate(api_keys):
            if not key or key.startswith("YOUR_"):
                continue
            is_valid = await verify_vision_provider_connection(
                base_url=provider_config.get("baseURL"),
                api_key=key,
                model_name=request.model,
                request_params=model_config.get("requestParams")
            )
            if is_valid:
                return {"success": True}
            print(f"⚠️ Vision key {i+1}/{len(api_keys)} failed for {request.name}, trying next...")
        
        return {"success": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify vision provider: {e}")

@router.get("/api/transparency")
async def get_transparency():
    """Get current window transparency information"""
    return window_manager.get_transparency_info()

@router.post("/api/transparency")
async def set_transparency(request: TransparencyRequest):
    """Set window transparency (0.0 = transparent, 1.0 = opaque)"""
    success = window_manager.set_app_transparency(request.transparency)
    if success:
        return {
            "success": True,
            "transparency": request.transparency,
            "message": f"Transparency set to {request.transparency*100:.0f}%"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to set transparency")

@router.post("/api/transparency/percent")
async def set_transparency_percent(request: TransparencyPercentRequest):
    """Set window transparency as percentage (0 = transparent, 100 = opaque)"""
    success = window_manager.set_app_transparency_percent(request.percent)
    if success:
        return {
            "success": True,
            "percent": request.percent,
            "transparency": request.percent / 100.0,
            "message": f"Transparency set to {request.percent}%"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to set transparency")

@router.post("/api/transparency/presets/transparent")
async def make_transparent():
    """Make window 60% transparent (40% opacity) - good for interviews"""
    success = window_manager.make_app_transparent()
    if success:
        return {"success": True, "message": "Window set to interview mode (40% opacity)"}
    else:
        raise HTTPException(status_code=400, detail="Failed to set transparency")

@router.post("/api/transparency/presets/semi-transparent")
async def make_semi_transparent():
    """Make window semi-transparent (70% opacity)"""
    success = window_manager.make_app_semi_transparent()
    if success:
        return {"success": True, "message": "Window set to semi-transparent (70% opacity)"}
    else:
        raise HTTPException(status_code=400, detail="Failed to set transparency")

@router.post("/api/transparency/presets/opaque")
async def make_opaque():
    """Make window fully opaque (100% opacity)"""
    success = window_manager.make_app_opaque()
    if success:
        return {"success": True, "message": "Window set to opaque (100% opacity)"}
    else:
        raise HTTPException(status_code=400, detail="Failed to set transparency")

