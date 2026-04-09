"""LangClaw LLM Agent - Language learning and linguistics"""
from .. import get_llm

class LangClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def teach_phrase(self, phrase: str, language: str, context: str = "conversational") -> str:
        """Teach a phrase in another language"""
        prompt = f"Teach how to say '{phrase}' in {language} for {context} context. Include pronunciation and usage examples."
        return self.llm.generate(prompt, task="translation").text
    
    def explain_grammar(self, rule: str, language: str) -> str:
        """Explain grammar rules"""
        prompt = f"Explain the grammar rule '{rule}' in {language}. Include examples and common mistakes."
        return self.llm.generate(prompt, task="translation").text
    
    def practice_conversation(self, language: str, scenario: str, level: str = "beginner") -> str:
        """Generate conversation practice"""
        prompt = f"Create a {level} level conversation practice in {language} for scenario: {scenario}. Include both sides."
        return self.llm.generate(prompt, task="translation").text
    
    def correct_sentence(self, sentence: str, target_language: str) -> str:
        """Correct sentences in target language"""
        prompt = f"Correct this {target_language} sentence and explain the corrections:\n\n{sentence}"
        return self.llm.generate(prompt, task="translation").text
    
    def cultural_note(self, topic: str, culture: str) -> str:
        """Provide cultural context"""
        prompt = f"Provide cultural context about {topic} in {culture} that would help language learners."
        return self.llm.generate(prompt, task="translation").text
