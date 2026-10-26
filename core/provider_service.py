import os
from typing import List, Dict, Any, Optional
import orjson
from core.env_utils import env_manager

AI_PROVIDERS_FILE = "ai_providers.json"
AI_PROVIDERS_EXAMPLE_FILE = "ai_providers.example.json"
DEFAULT_PROVIDERS = ["Groq", "Cerebras", "Gemini", "OpenRouter"]


def get_env_prefix(provider_name: str) -> str:
    """Returns the environment variable prefix for a given provider name, e.g. GROQ_."""
    return provider_name.upper().replace(" ", "_").replace("-", "_") + "_"


def parse_list_from_env(val: Optional[str]) -> List[str]:
    """Parses a comma-separated or newline-separated string from .env into a clean list of strings."""
    if not val:
        return []
    val_stripped = val.strip()
    if val_stripped.startswith("[") and val_stripped.endswith("]"):
        try:
            parsed = orjson.loads(val_stripped)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except Exception:
            pass
    delimiter = "\n" if "\n" in val else ","
    return [item.strip() for item in val.split(delimiter) if item.strip()]


def parse_bool_from_env(val: Optional[str], default: bool = False) -> bool:
    """Parses a boolean value from an environment variable."""
    if val is None:
        return default
    return str(val).strip().lower() in ("true", "1", "yes", "on")


def load_providers_config(file_path: str = AI_PROVIDERS_FILE) -> List[Dict[str, Any]]:
    """
    Loads all AI provider configurations directly from .env (and environment variables).
    Each provider's baseURL, vision support, keys, models, and defaults are defined in .env.
    """
    env_providers_val = env_manager.get_value("AI_PROVIDERS")
    if env_providers_val:
        provider_names = parse_list_from_env(env_providers_val)
    else:
        # Check if any provider has BASE_URL or API_KEYS defined in .env
        detected = [
            p for p in DEFAULT_PROVIDERS
            if env_manager.get_value(f"{get_env_prefix(p)}BASE_URL") or env_manager.get_value(f"{get_env_prefix(p)}API_KEYS")
        ]
        provider_names = detected if detected else DEFAULT_PROVIDERS

    providers = []
    for name in provider_names:
        prefix = get_env_prefix(name)

        base_url = env_manager.get_value(f"{prefix}BASE_URL") or ""
        supports_vision = parse_bool_from_env(env_manager.get_value(f"{prefix}SUPPORTS_VISION"), default=False)
        default_primary = parse_bool_from_env(env_manager.get_value(f"{prefix}DEFAULT_PRIMARY"), default=False)
        default_secondary = parse_bool_from_env(env_manager.get_value(f"{prefix}DEFAULT_SECONDARY"), default=False)
        default_vision_primary = parse_bool_from_env(env_manager.get_value(f"{prefix}DEFAULT_VISION_PRIMARY"), default=False)
        default_vision_secondary = parse_bool_from_env(env_manager.get_value(f"{prefix}DEFAULT_VISION_SECONDARY"), default=False)

        # 1. API Keys
        env_keys = env_manager.get_value(f"{prefix}API_KEYS") or env_manager.get_value(f"{prefix}API_KEY")
        keys = parse_list_from_env(env_keys) if env_keys else []

        # 2. Models
        env_models = env_manager.get_value(f"{prefix}MODELS") or env_manager.get_value(f"{prefix}MODEL")
        models = parse_list_from_env(env_models) if env_models else []

        # 3. Vision Models
        env_vision_models = env_manager.get_value(f"{prefix}VISION_MODELS") or env_manager.get_value(f"{prefix}VISION_MODEL")
        vision_models = parse_list_from_env(env_vision_models) if env_vision_models else []

        # 4. Default Model
        default_model = env_manager.get_value(f"{prefix}DEFAULT_MODEL")
        if not default_model and models:
            first_m = models[0]
            default_model = first_m.get("modelName") if isinstance(first_m, dict) else first_m

        # 5. Default Vision Model
        default_vision_model = env_manager.get_value(f"{prefix}DEFAULT_VISION_MODEL")
        if not default_vision_model and vision_models:
            first_vm = vision_models[0]
            default_vision_model = first_vm.get("modelName") if isinstance(first_vm, dict) else first_vm

        provider = {
            "name": name,
            "baseURL": base_url,
            "supportsVision": supports_vision,
            "apiKey": keys[0] if keys else "",
            "apiKeys": keys,
            "models": models,
            "visionModels": vision_models,
            "defaultModel": default_model,
            "defaultVisionModel": default_vision_model,
            "defaultPrimary": default_primary,
            "defaultSecondary": default_secondary,
            "defaultVisionPrimary": default_vision_primary,
            "defaultVisionSecondary": default_vision_secondary,
            "default": default_primary
        }
        providers.append(provider)

    return providers


def save_providers_config(providers: List[Dict[str, Any]], file_path: str = AI_PROVIDERS_FILE) -> bool:
    """
    Saves all provider configurations (baseURL, keys, models, vision models, flags)
    directly into the .env file.
    """
    env_updates: Dict[str, str] = {}
    provider_names = []

    for p in providers:
        name = p.get("name", "")
        if not name:
            continue
        provider_names.append(name)
        prefix = get_env_prefix(name)

        if p.get("baseURL"):
            env_updates[f"{prefix}BASE_URL"] = str(p["baseURL"]).strip()

        env_updates[f"{prefix}SUPPORTS_VISION"] = "true" if p.get("supportsVision") else "false"

        if "defaultPrimary" in p:
            env_updates[f"{prefix}DEFAULT_PRIMARY"] = "true" if p["defaultPrimary"] else "false"
        if "defaultSecondary" in p:
            env_updates[f"{prefix}DEFAULT_SECONDARY"] = "true" if p["defaultSecondary"] else "false"
        if "defaultVisionPrimary" in p:
            env_updates[f"{prefix}DEFAULT_VISION_PRIMARY"] = "true" if p["defaultVisionPrimary"] else "false"
        if "defaultVisionSecondary" in p:
            env_updates[f"{prefix}DEFAULT_VISION_SECONDARY"] = "true" if p["defaultVisionSecondary"] else "false"

        api_keys = p.get("apiKeys") or ([p["apiKey"]] if p.get("apiKey") else [])
        if api_keys:
            env_updates[f"{prefix}API_KEYS"] = ",".join(k.strip() for k in api_keys if k.strip())

        models = p.get("models")
        if models:
            model_names = [m.get("modelName") if isinstance(m, dict) else str(m) for m in models]
            env_updates[f"{prefix}MODELS"] = ",".join(m.strip() for m in model_names if m.strip())

        vision_models = p.get("visionModels")
        if vision_models:
            v_names = [vm.get("modelName") if isinstance(vm, dict) else str(vm) for vm in vision_models]
            env_updates[f"{prefix}VISION_MODELS"] = ",".join(v.strip() for v in v_names if v.strip())

        if p.get("defaultModel"):
            env_updates[f"{prefix}DEFAULT_MODEL"] = str(p["defaultModel"]).strip()
        if p.get("defaultVisionModel"):
            env_updates[f"{prefix}DEFAULT_VISION_MODEL"] = str(p["defaultVisionModel"]).strip()

    env_updates["AI_PROVIDERS"] = ",".join(provider_names)

    # Save everything into .env
    success = env_manager.update_keys(env_updates)

    # Keep ai_providers.json empty
    try:
        if os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(orjson.dumps([], option=orjson.OPT_INDENT_2))
    except Exception as e:
        print(f"⚠️ Note: Could not update {file_path}: {e}")

    return success
