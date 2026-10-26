import os
import re
from typing import Dict, Optional

class EnvManager:
    """Manages reading and writing to the .env file while preserving structure and comments."""
    
    def __init__(self, file_path: str = ".env"):
        self.file_path = file_path

    def update_key(self, key: str, value: str) -> bool:
        """
        Updates a specific key in the .env file. 
        Creates the file if it doesn't exist.
        """
        return self.update_keys({key: value})

    def update_keys(self, updates: Dict[str, str]) -> bool:
        """
        Updates multiple keys in the .env file in a single pass while preserving
        comments and order. Appends missing keys at the end.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                for k, v in updates.items():
                    f.write(f'{k}="{v}"\n')
            return True

        with open(self.file_path, "r") as f:
            lines = f.readlines()

        updated_keys = set()
        new_lines = []

        for line in lines:
            line_stripped = line.strip()
            matched = False
            for k, v in updates.items():
                pattern = re.compile(f"^{re.escape(k)}\\s*=")
                if pattern.match(line_stripped):
                    new_lines.append(f'{k}="{v}"\n')
                    updated_keys.add(k)
                    matched = True
                    break
            if not matched:
                new_lines.append(line)

        # Append remaining keys
        for k, v in updates.items():
            if k not in updated_keys:
                if new_lines and not new_lines[-1].endswith("\n"):
                    new_lines[-1] += "\n"
                new_lines.append(f'{k}="{v}"\n')

        with open(self.file_path, "w") as f:
            f.writelines(new_lines)

        return True

    def get_value(self, key: str) -> Optional[str]:
        """Reads a specific value from the .env file manually (to avoid caching issues)."""
        if not os.path.exists(self.file_path):
            return os.getenv(key)
            
        with open(self.file_path, "r") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    # Basic quote stripping
                    parts = line.strip().split("=", 1)
                    if len(parts) > 1:
                        val = parts[1].strip()
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            return val[1:-1]
                        return val
        return os.getenv(key)

# Global instance
env_manager = EnvManager()
