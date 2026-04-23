"""Shim to redirect core.llm_manager to core.llm.manager.Manager"""

# Redirect to the Manager that actually has chat()
from core.llm.manager import Manager

# Create a compatible wrapper
class LLMManager:
    """Wrapper that provides the expected interface"""
    
    def __init__(self):
        self.manager = Manager()
        # Proxy common attributes
        self.groq_client = getattr(self.manager, '_groq', None)
    
    def chat(self, prompt: str, **kwargs) -> str:
        """Forward to manager.chat()"""
        return self.manager.chat(prompt, **kwargs)
    
    def __getattr__(self, name):
        """Proxy other attributes to manager"""
        return getattr(self.manager, name)

def get_llm_manager():
    """Factory function"""
    return LLMManager()

__all__ = ['get_llm_manager', 'LLMManager']
