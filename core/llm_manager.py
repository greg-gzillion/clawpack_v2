"""LLM Manager - Groq first, Ollama fallback"""
import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self):
        self.llms = []
        self.selected_model: Optional[Dict] = None
        self.load_config()
        self.groq_client = None
        self._init_groq()
    
    def _init_groq(self):
        """Initialize Groq client if API key available"""
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key != "gsk_your_groq_api_key_here":
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=api_key)
                print("✅ Groq client initialized")
            except Exception as e:
                print(f"⚠️ Groq init failed: {e}")
    
    def load_config(self):
        config_path = Path("working_llms.json")
        if config_path.exists():
            data = json.loads(config_path.read_text())
            self.llms = data
    
    def list_models(self) -> str:
        if not self.llms:
            return "No LLMs configured"
        output = [f"\n📦 Working LLMs ({len(self.llms)} total):\n"]
        sources = {}
        for llm in self.llms:
            src = llm["source"]
            if src not in sources:
                sources[src] = []
            sources[src].append(llm["model"])
        for src, models in sources.items():
            output.append(f"\n{src.upper()} ({len(models)}):")
            for m in models:
                marker = " ✅" if self.selected_model and self.selected_model["model"] == m else ""
                output.append(f"  • {m}{marker}")
        return '\n'.join(output)
    
    def chat_sync(self, prompt: str, model: str = None) -> str:
        """Chat using Groq (fast) or fallback to Ollama"""
        
        # Try Groq first
        if self.groq_client:
            try:
                model_name = model or os.getenv("DEFAULT_MODEL", "llama3-8b-8192")
                completion = self.groq_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1024
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"Groq error: {e}, falling back to Ollama")
        
        # Fallback to Ollama
        try:
            ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
            result = subprocess.run(
                ["ollama", "run", ollama_model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
            return f"Ollama error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"

_llm_manager = None

def get_llm_manager():
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
