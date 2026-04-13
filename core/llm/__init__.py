from .manager import Manager, get_manager

LLMManager = Manager

def get_llm_manager():
    return get_manager()
