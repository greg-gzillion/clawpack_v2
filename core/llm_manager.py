"""LLM Manager - Handles multiple LLM providers"""

import os
from pathlib import Path
from typing import Optional, Dict, List

class LLMManager:
    def __init__(self):
        self.groq_client = None
        self.ollama_client = None
        self.available_models = []
        self._init_groq()
        self._init_ollama()
    
    def _init_groq(self):
        try:
            from groq import Groq
            api_key = os.environ.get('GROQ_API_KEY')
            if api_key:
                self.groq_client = Groq(api_key=api_key)
                print("⚡ Groq available", file=sys.stderr)
        except:
            pass
    
    def _init_ollama(self):
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            if response.status_code == 200:
                self.ollama_client = True
                print("🦙 Ollama available", file=sys.stderr)
        except:
            pass
    
    def chat_sync(self, prompt: str, task_type: str = "general") -> str:
        """Synchronous chat completion"""
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=4096
                )
                return response.choices[0].message.content
            except:
                pass
        
        # Fallback response
        return f"[LLM Response] Processed: {prompt[:100]}..."

def get_llm_manager() -> LLMManager:
    return LLMManager()
