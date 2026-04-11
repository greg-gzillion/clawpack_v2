"""LLM Manager - Integrates with existing modular LLM system"""
import sys
import os
import subprocess
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

class LLMManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.groq_client = None
        self._init_groq()
    
    def _init_groq(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and "gsk_" in api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=api_key)
                print("⚡ Groq available", file=sys.stderr)
            except:
                pass
    
    def _get_local_model(self, task_type: str) -> str:
        if task_type == "code":
            return "deepseek-coder:6.7b"
        elif task_type == "reasoning":
            return "deepseek-r1:8b"
        else:
            return "llama3.2:3b"
    
    def chat_sync(self, prompt: str, task_type: str = "general") -> str:
        # Try Groq first
        if self.groq_client:
            try:
                model = "llama-3.3-70b-versatile" if task_type == "code" else "llama-3.1-8b-instant"
                completion = self.groq_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2048
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"Groq error: {e}", file=sys.stderr)
        
        # Use local model
        model = self._get_local_model(task_type)
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
            return f"Error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"

_llm_manager = None

def get_llm_manager():
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
