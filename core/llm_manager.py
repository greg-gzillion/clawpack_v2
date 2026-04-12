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
        """Chat using Groq with the latest supported model"""
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                from groq import Groq
                client = Groq(api_key=groq_key)
                
                # Use a currently supported model
                # Options: llama-3.3-70b-versatile (best), llama-3.1-8b-instant (fastest)
                model_to_use = model if model else "llama-3.3-70b-versatile"
                
                completion = client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                return completion.choices[0].message.content
            
            # Fallback to OpenRouter
            key = os.getenv("OPENROUTER_API_KEY")
            if key:
                import requests
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={
                        "model": "google/gemma-2-9b-it:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 500
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
            
            return "Error: No working API key. Please check GROQ_API_KEY in .env"
            
        except Exception as e:
            return f"Error: {str(e)}"

_llm_manager = None

def get_llm_manager():
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
