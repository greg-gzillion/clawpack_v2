"""TXclaw Configuration Settings"""

from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"
WEBCLAW_PATH = Path("str(PROJECT_ROOT)/agents/webclaw/references/txclaw")

# API configuration
DEFAULT_MODEL = "openrouter/gpt-3.5-turbo"
TIMEOUT_SECONDS = 60
MAX_RETRIES = 3

def get_api_key() -> str | None:
    """Get OpenRouter API key from .env file"""
    if ENV_PATH.exists():
        try:
            with open(ENV_PATH, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    if 'OPENROUTER_API_KEY' in line and '=' in line:
                        return line.split('=', 1)[1].strip().strip('"\'').strip()
        except Exception:
            pass
    return os.environ.get("OPENROUTER_API_KEY")

def get_webclaw_sources() -> list:
    """Get list of available webclaw sources"""
    if WEBCLAW_PATH.exists():
        return [d.name for d in WEBCLAW_PATH.iterdir() if d.is_dir()]
    return []
