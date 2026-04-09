"""Core Medical Engine"""

from pathlib import Path
from config.settings import Config
from providers import ProviderRegistry

class MedicalEngine:
    def __init__(self):
        self.providers = ProviderRegistry()
        self.data_path = Config.DATA_PATH
    
    def generate(self, prompt: str) -> tuple:
        return self.providers.generate(prompt)
    
    def research(self, query: str) -> str:
        prompt = f"Medical research on {query}. Provide current treatments and guidelines."
        result, provider = self.generate(prompt)
        return f"[{provider}]\n{result}"
    
    def diagnose(self, symptoms: str) -> str:
        prompt = f"Differential diagnosis for {symptoms}. Include primary, secondary, red flags, tests, urgency."
        result, provider = self.generate(prompt)
        return f"[{provider}]\n{result}"
    
    def treatment(self, condition: str) -> str:
        prompt = f"Treatment guidelines for {condition}. Include first-line, medications, monitoring, follow-up."
        result, provider = self.generate(prompt)
        return f"[{provider}]\n{result}"
    
    def list_sources(self) -> list:
        if self.data_path.exists():
            return sorted([d.name for d in self.data_path.iterdir() if d.is_dir()])
        return []
