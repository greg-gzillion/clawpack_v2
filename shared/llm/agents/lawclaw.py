"""LawClaw LLM Agent"""
from .. import get_llm

class LawClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(self, text: str) -> str:
        return self.llm.generate(text, task="legal").text
    
    def summarize_case(self, case_text: str) -> str:
        prompt = f"Summarize this legal case: {case_text}"
        return self.llm.generate(prompt, task="legal").text
