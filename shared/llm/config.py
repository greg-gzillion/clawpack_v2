"""Constants and configuration for the sovereign gateway."""

import os
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
CHRONICLE_PATH = DATA_DIR / "chronicle_ledger.json"
ACTIVE_MODEL_PATH = MODELS_DIR / "active_model.json"
WORKING_LLMS_PATH = MODELS_DIR / "working_llms.json"
BUDGET_PATH = DATA_DIR / "llm_budget.json"


def load_config() -> Dict[str, str]:
    """Load API keys from .env and export to os.environ"""
    config = {}
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().split('\n'):
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip(chr(34)).strip(chr(39))
                config[key] = value
                if key.endswith('_API_KEY') and value:
                    os.environ[key] = value
    return config


__all__ = [
    'PROJECT_ROOT', 'MODELS_DIR', 'DATA_DIR',
    'CHRONICLE_PATH', 'ACTIVE_MODEL_PATH',
    'WORKING_LLMS_PATH', 'BUDGET_PATH', 'load_config',
]
