"""Intelligent LLM Router - Groq primary + specialized local models"""
import json
from pathlib import Path
from typing import Dict, List, Optional

class LLMRouter:
    """Routes tasks to the most appropriate LLM - Groq first, then specialized locals"""
    
    def __init__(self):
        self.llms = self._load_llms()
        self.has_groq = False
        self._check_groq()
        self.task_model_map = self._build_task_map()
    
    def _load_llms(self) -> List[Dict]:
        with open(Path(__file__).parent.parent / "working_llms.json") as f:
            return json.load(f)
    
    def _check_groq(self):
        """Check if Groq is available"""
        import os
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key != "gsk_your_groq_api_key_here" and "gsk_" in api_key:
            self.has_groq = True
    
    def _build_task_map(self) -> Dict:
        """Map task types to recommended models (fallbacks if Groq not available)"""
        return {
            # Programming - use deepseek-coder for complex code
            'code': ['deepseek-coder:6.7b', 'codellama:7b', 'qwen3-coder:30b'],
            'debug': ['deepseek-coder:6.7b', 'codellama:7b'],
            'explain': ['deepseek-coder:6.7b', 'codellama:7b'],
            
            # Reasoning tasks - use deepseek-r1
            'law': ['deepseek-r1:8b', 'llama3.2:3b'],
            'legal': ['deepseek-r1:8b', 'llama3.2:3b'],
            'medical': ['llama3.2:3b', 'gemma3:4b'],
            
            # General tasks - use fastest models
            'general': ['llama3.2:3b', 'gemma3:4b'],
            'translate': ['llama3.2:3b', 'gemma3:4b'],
            'math': ['deepseek-r1:8b', 'llama3.2:3b'],
            
            # Vision - use qwen3-vl
            'vision': ['qwen3-vl:30b'],
        }
    
    def select_model(self, task_type: str) -> str:
        """Select best model - Groq always wins if available"""
        # Groq is always preferred for speed
        if self.has_groq:
            return "groq"
        
        # Fallback to local models
        models = self.task_model_map.get(task_type, self.task_model_map['general'])
        available_models = [llm['model'] for llm in self.llms]
        
        for model in models:
            if model in available_models:
                return model
        
        return "llama3.2:3b"

_router = None

def get_router():
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
