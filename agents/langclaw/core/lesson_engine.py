"""Language Lesson Engine"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.llm_wrapper import LLMManager

# Try to import chronicle, but don't fail if not available
try:
    from shared.chronicle_helper import search_chronicle
    HAS_CHRONICLE = True
except:
    HAS_CHRONICLE = False
    search_chronicle = lambda q, l: []

class LessonEngine:
    def __init__(self, language: str):
        self.language = language.lower()
        self.llm = LLMManager()
        self.chronicle_refs = search_chronicle(self.language, 5) if HAS_CHRONICLE else []
    
    def get_lesson(self, topic: str, level: str = "beginner") -> str:
        ref_text = ""
        if self.chronicle_refs:
            ref_text = "\n\n📚 References:\n" + "\n".join([f"   • {r.url}" for r in self.chronicle_refs])
        
        prompt = f"Create a {level} lesson for {self.language} on {topic}. Include vocabulary, grammar, examples, and practice exercises.{ref_text}"
        return self.llm.chat_sync(prompt)
    
    def get_conversation(self, scenario: str) -> str:
        prompt = f"Create a natural conversation in {self.language} for: {scenario}. Include English translation."
        return self.llm.chat_sync(prompt)
    
    def get_practice(self, topic: str = None) -> str:
        topic_text = f" on {topic}" if topic else ""
        prompt = f"Create 10 practice exercises for {self.language}{topic_text} with answer key."
        return self.llm.chat_sync(prompt)
    
    def get_vocab(self, word: str) -> str:
        prompt = f"Define '{word}' in {self.language} with pronunciation, examples, and usage notes."
        return self.llm.chat_sync(prompt)
