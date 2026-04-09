"""API Provider for Langclaw - Using Shared API"""

import sys
from pathlib import Path

# Add root to path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

# Import the shared API
from shared.llm.api import call as shared_call
from config.settings import DEFAULT_MODEL

def api_call(prompt: str, model: str = None) -> str:
    """Make API call through shared LLM module"""
    model = model or DEFAULT_MODEL
    try:
        # The shared API expects prompt and model
        response = shared_call(prompt, model=model)
        
        # Handle different response types
        if response is None:
            return "No response from API"
        elif isinstance(response, dict):
            return response.get('content', str(response))
        else:
            return str(response)
            
    except Exception as e:
        return f"API Error: {str(e)}"

def translate(text: str, from_lang: str, to_lang: str) -> str:
    """Translate text between languages"""
    prompt = f'Translate this from {from_lang} to {to_lang}. Return ONLY the translation, no quotes or explanations:\n\n{text}'
    result = api_call(prompt)
    # Clean up common issues
    result = result.strip('"\'')
    return result

def teach_word(word: str, target_lang: str, native_lang: str = "english") -> str:
    """Teach a word with pronunciation and examples"""
    prompt = f"""Teach the word '{word}' to a {native_lang} speaker learning {target_lang}.

Format exactly like this:

📖 WORD: {word}
🔤 IN {target_lang}: [translation]
🗣️ PRONUNCIATION: [simple guide]
📝 EXAMPLE: [sentence in {target_lang}]
💡 MEANING: [translation]
🎯 TIP: [memory tip]

Keep it brief and helpful."""
    return api_call(prompt)

def generate_quiz(language: str, level: str = "beginner") -> str:
    """Generate a language quiz"""
    prompt = f"Create a {level} quiz for learning {language}. Include 5 multiple choice questions. Show answers at the end."
    return api_call(prompt)
