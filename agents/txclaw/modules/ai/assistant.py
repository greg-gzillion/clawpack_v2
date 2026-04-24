"""TX AI Assistant - LLM-powered TX blockchain knowledge"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))
# LLMClaw handles all LLM via A2A

class TXAIAssistant:
    def __init__(self):
        pass  # LLMClaw via A2A

    def ask(self, query: str, context: str = "") -> str:
        prompt = f"You are a TX.org blockchain expert. Context: {context}\n\nQuestion: {query}" if context else f"You are a TX.org blockchain expert. Answer: {query}"
        result = # _llm(prompt)
        return result if result and "Error" not in result else "Unable to get response"

    def generate_code(self, prompt: str, context: str = None) -> str:
        full = f"Generate TX.org blockchain code (CosmWasm/Rust): {prompt}"
        if context: full = f"Context: {context}\n\n{full}"
        result = # _llm(full)
        return result if result else "// Code generation failed"
