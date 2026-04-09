"""LLM-powered translation engine"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.llm.client import get_llm

class LLMTranslator:
    def __init__(self):
        self.llm = get_llm()
    
    def translate(self, text: str, target_lang: str) -> str:
        prompt = f"Translate this to {target_lang}. Return ONLY the translation, no explanation:\n\n{text}"
        
        try:
            import asyncio
            response = asyncio.run(self.llm.call(prompt, max_tokens=100))
            return response.content.strip()
        except:
            return None
