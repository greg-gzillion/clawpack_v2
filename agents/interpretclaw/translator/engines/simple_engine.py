"""Simple word-based translation engine (fallback)"""

from .base import TranslationEngine

class SimpleEngine(TranslationEngine):
    """Simple word-for-word translation as fallback"""
    
    @property
    def name(self) -> str:
        return "Simple Engine"
    
    def is_available(self) -> bool:
        return True  # Always available
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        # Simple word mapping for common words
        word_map = {
            'en': {'es': {'hello': 'hola', 'world': 'mundo', 'good': 'bueno', 'day': 'día'}},
            'es': {'en': {'hola': 'hello', 'mundo': 'world', 'bueno': 'good', 'día': 'day'}}
        }
        
        words = text.lower().split()
        translated = []
        
        for word in words:
            if source_lang in word_map and target_lang in word_map[source_lang]:
                translated.append(word_map[source_lang][target_lang].get(word, f"[{word}]"))
            else:
                translated.append(f"[{word}]")
        
        result = " ".join(translated)
        
        # Add note about using WebClaw for better translation
        if len(text) > 50:
            result += "\n\n💡 For better translation, start WebClaw: python agents/webclaw/webclaw_agent.py"
        
        return result
