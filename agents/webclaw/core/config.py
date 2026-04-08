"""WebClaw configuration"""

from pathlib import Path
import os

ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack_v2")
WEB_REFS = Path(__file__).parent.parent / "references"
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

def load_env():
    """Load .env file from root directory"""
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        return True
    return False

# Load environment variables on import
load_env()

def get_config():
    return {
        "root_dir": ROOT_DIR,
        "web_refs": WEB_REFS,
        "shared_db": SHARED_DB,
        "api_key": os.environ.get('OPENROUTER_API_KEY')
    }
