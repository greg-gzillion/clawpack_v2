"""Task router - detects intent"""
import re

class TaskRouter:
    def detect(self, text: str) -> str:
        text_lower = text.lower()
        
        if " to " in text_lower and any(lang in text_lower for lang in 
            ["spanish", "french", "german", "japanese", "chinese", "italian"]):
            return "translate"
        
        code_keywords = ["function", "class", "def ", "import", "code", "python", "javascript"]
        if any(kw in text_lower for kw in code_keywords):
            return "code"
        
        return "default"
    
    def build_prompt(self, text: str, task: str) -> str:
        if task == "translate":
            match = re.search(r"(.+?)\s+to\s+(\w+)", text, re.IGNORECASE)
            if match:
                return f"Translate '{match.group(1)}' to {match.group(2)}. Give ONLY the translation."
        return text
