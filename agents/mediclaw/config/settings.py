"""Mediclaw Configuration"""

import os
from pathlib import Path

# Load API key from root .env
ENV_PATH = Path("C:/Users/greg/dev/clawpack_v2/.env")
API_KEY = None

if ENV_PATH.exists():
    with open(ENV_PATH, 'r') as f:
        for line in f:
            if line.startswith('OPENROUTER_API_KEY='):
                API_KEY = line.split('=')[1].strip()
                break

class Config:
    OPENROUTER_KEY = API_KEY
    WEBCLAW_PATH = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/mediclaw")
    
    @classmethod
    def show_status(cls):
        print(f"API Key: {'✅ ' + cls.OPENROUTER_KEY[:20] + '...' if cls.OPENROUTER_KEY else '❌ Not found'}")
        print(f"Webclaw: {'✅ ' + str(len(cls.get_specialties())) + ' specialties' if cls.WEBCLAW_PATH.exists() else '❌ Not found'}")
    
    @classmethod
    def get_specialties(cls):
        if cls.WEBCLAW_PATH.exists():
            return [d.name for d in cls.WEBCLAW_PATH.iterdir() if d.is_dir()]
        return []
