import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
STATE_FILE = PROJECT_ROOT / "models" / "active_model.json"

def get_active_model():
    """Get the currently selected model from LLMClaw"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            data = json.load(f)
            return data.get('model'), data.get('source')
    return "llama3.2:3b", "stock"
"""LLM Manager with liberated model preference"""
import json
import asyncio
from pathlib import Path
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider
from .anthropic import AnthropicProvider


def get_active_model():
    """Get the currently selected model from LLMClaw"""
    state_file = Path(__file__).parent.parent.parent / "models" / "active_model.json"
    if state_file.exists():
        with open(state_file) as f:
            data = json.load(f)
            return data.get("model"), data.get("source")
    return "llama3.2:3b", "stock"


class LLMManager:
    def __init__(self, prefer_liberated: bool = True):
        self.providers = []
        self.prefer_liberated = prefer_liberated
        self.load_working_llms()
        self.timeout = 10

    def load_working_llms(self):
        config_path = Path("working_llms.json")
        if not config_path.exists():
            return

        data = json.loads(config_path.read_text())

        if self.prefer_liberated:
            liberated = [m for m in data if "liberated" in m["model"] or m.get("obliterated", False)]
            standard = [m for m in data if "liberated" not in m["model"] and not m.get("obliterated", False)]
            data = liberated + standard

        priority_order = ["openrouter", "anthropic", "ollama"]

        for source in priority_order:
            for item in data:
                if item["source"] != source:
                    continue
                model = item["model"]
                try:
                    if source == "ollama":
                        provider = OllamaProvider(model)
                        if provider.is_available():
                            self.providers.append(provider)
                    elif source == "openrouter":
                        provider = OpenRouterProvider(model)
                        if provider.key:
                            self.providers.append(provider)
                    elif source == "anthropic":
                        provider = AnthropicProvider(model)
                        if provider.key:
                            self.providers.append(provider)
                except:
                    pass

    def get_best_for_task(self, task: str):
        if not self.providers:
            return None

        if task in ["creative", "dream", "brainstorm"]:
            for p in self.providers:
                if "liberated" in p.model or getattr(p, "obliterated", False):
                    return p

        return self.providers[0] if self.providers else None

    def list_providers(self):
        return [str(p) for p in self.providers]