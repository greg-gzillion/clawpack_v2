"""Mediclaw Configuration"""
import os
from pathlib import Path

ENV_PATH = Path("str(PROJECT_ROOT)/.env")

def _load_key(prefix):
    if ENV_PATH.exists():
        with open(ENV_PATH, 'r') as f:
            for line in f:
                if line.startswith(prefix):
                    return line.split('=', 1)[1].strip()
    return None

class Config:
    OPENROUTER_KEY = _load_key('OPENROUTER_API_KEY=')
    ANTHROPIC_KEY = _load_key('ANTHROPIC_API_KEY=')
    GROQ_KEY = _load_key('GROQ_API_KEY=')
    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_MODEL = "codellama:7b"
    WEBCLAW_PATH = Path("str(PROJECT_ROOT)/agents/webclaw/references/mediclaw")
    DATA_PATH = WEBCLAW_PATH

    @classmethod
    def show_status(cls):
        print(f"OpenRouter: {'Yes' if cls.OPENROUTER_KEY else 'No'}")
        print(f"Anthropic: {'Yes' if cls.ANTHROPIC_KEY else 'No'}")
        print(f"Groq: {'Yes' if cls.GROQ_KEY else 'No'}")
        print(f"Ollama: {cls.OLLAMA_URL} | Model: {cls.OLLAMA_MODEL}")
        print(f"Data: {'Yes' if cls.DATA_PATH.exists() else 'No'}")

    @classmethod
    def get_specialties(cls):
        if cls.WEBCLAW_PATH.exists():
            return [d.name for d in cls.WEBCLAW_PATH.iterdir() if d.is_dir()]
        return []
