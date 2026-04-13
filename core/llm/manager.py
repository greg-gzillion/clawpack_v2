"""LLM Manager"""

from .providers import discover_providers
from .cache import Cache
from .config import get_task_for_agent, get_models_for_task

class Manager:
    def __init__(self):
        self.providers = discover_providers()
        self.cache = Cache()
        self.cache.apply(self.providers)
        self._groq = self._find_groq()
    
    def _find_groq(self):
        for p in self.providers:
            if p.config.name == "groq" and p.status == "working":
                return p
        return None
    
    def chat(self, prompt: str, agent: str = None, task: str = None) -> str:
        task = task or get_task_for_agent(agent) if agent else "general"
        
        # Try Groq first
        if self._groq:
            resp = self._groq.call(prompt)
            if resp:
                return resp
        
        # Fallback to local models for task
        for model in get_models_for_task(task):
            for p in self.providers:
                if p.config.model == model and p.status == "working":
                    resp = p.call(prompt)
                    if resp:
                        return resp
        
        return "No working provider"
    
    def status(self) -> dict:
        working = [p.config.name for p in self.providers if p.status == "working"]
        return {
            "total": len(self.providers),
            "working": len(working),
            "groq": self._groq is not None
        }
    
    def list(self) -> str:
        working = [p for p in self.providers if p.status == "working"]
        if not working:
            return "No working models"
        lines = [f"Working models ({len(working)}):"]
        for p in working:
            mark = "*" if p.config.name == "groq" else " "
            lines.append(f"  [{mark}] {p.config.model} ({p.response_time:.1f}s)")
        return "\n".join(lines)

_manager = None

def get_manager() -> Manager:
    global _manager
    if _manager is None:
        _manager = Manager()
    return _manager
