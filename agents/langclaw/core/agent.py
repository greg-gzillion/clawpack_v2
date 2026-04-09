"""Core Langclaw Agent - Coordinates all modules"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.translator import Translator
from core.session_manager import SessionManager
from providers.webclaw_provider import WebclawLangProvider

class LangclawAgent:
    def __init__(self):
        self.translator = Translator()
        self.session = SessionManager()
        self.provider = WebclawLangProvider()
    
    def get_available_languages(self):
        return self.provider.get_language_folders()
    
    def get_language_name(self, code: str) -> str:
        return self.translator.get_language_name(code)
    
    def translate(self, text: str, target_lang: str) -> str:
        result = self.translator.translate(text, target_lang)
        self.session.add_query(text, target_lang, result["success"], result.get("translation"))
        
        if result["success"]:
            return f"""
✅ **Translation Found** (via {result['method']})

   "{text}" → "{result['translation']}"

📎 Source: {result['source']}
"""
        elif result["dictionary_urls"]:
            urls_text = "\n".join(f"🔗 {url}" for url in result["dictionary_urls"][:3])
            return f"""
📚 **No automatic translation found**

Try these online dictionaries for "{text}":

{urls_text}

💡 Tip: Visit the URL to get the translation
"""
        else:
            return f"❌ No translation resources found for {self.get_language_name(target_lang)}"
    
    def get_resources(self, language_code: str) -> str:
        urls = self.provider.extract_urls_from_references(language_code)
        
        output = f"\n📚 **Online Resources for {self.get_language_name(language_code)}**\n"
        
        if urls.get("dictionaries"):
            output += "\n--- Dictionaries ---\n"
            for url in urls["dictionaries"][:3]:
                output += f"🔗 {url}\n"
        
        if urls.get("translation_apis"):
            output += "\n--- Translation APIs ---\n"
            for url in urls["translation_apis"][:3]:
                output += f"🔗 {url}\n"
        
        return output
    
    def get_stats(self):
        stats = self.session.get_stats()
        return {"queries": stats["total_queries"], "details": stats}
