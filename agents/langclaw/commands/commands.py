"""Command handlers for Langclaw"""

from core.agent import LangclawAgent

class LangCommands:
    def __init__(self, agent: LangclawAgent):
        self.agent = agent
    
    def translate(self, text: str, target_lang: str) -> str:
        return self.agent.translate(text, target_lang)
    
    def get_languages(self) -> list:
        return self.agent.get_available_languages()
    
    def get_stats(self) -> dict:
        return self.agent.get_stats()
