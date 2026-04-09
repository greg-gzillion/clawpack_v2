"""InterpretClaw LLM Agent"""
from .. import get_llm

class InterpretClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        prompt = f"Translate from {source_lang} to {target_lang}: {text}"
        return self.llm.generate(prompt, task="translation").text
    
    def explain(self, phrase: str, language: str = "en") -> str:
        prompt = f"Explain the meaning and usage of '{phrase}' in {language}"
        return self.llm.generate(prompt, task="general").text
