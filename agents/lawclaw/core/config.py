"""Configuration - paths and API keys"""

from pathlib import Path
import os

ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack_v2")
LAW_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "lawclaw"
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

def get_api_key():
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v
    return os.environ.get('OPENROUTER_API_KEY')
