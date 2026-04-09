"""ClawCoder LLM Agent"""
from .. import get_llm

class ClawCoderLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def generate_code(self, description: str, language: str = "python") -> str:
        prompt = f"Write {language} code for: {description}"
        return self.llm.generate(prompt, task="code").text
    
    def debug(self, code: str, error: str) -> str:
        prompt = f"Debug this code:\n{code}\nError: {error}"
        return self.llm.generate(prompt, task="code").text
