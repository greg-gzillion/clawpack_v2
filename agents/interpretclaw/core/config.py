"""InterpretClaw configuration - Human Language Hub"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# 39 Human Languages for translation
SUPPORTED_LANGUAGES = {
    # European (20)
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
    "el": "Greek",
    "cs": "Czech",
    "hu": "Hungarian",
    "ro": "Romanian",
    "uk": "Ukrainian",
    "bg": "Bulgarian",
    
    # Asian (12)
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "hi": "Hindi",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "bn": "Bengali",
    
    # Middle Eastern (4)
    "ar": "Arabic",
    "he": "Hebrew",
    "fa": "Persian",
    "ku": "Kurdish",
    
    # Other (3)
    "sw": "Swahili",
    "tl": "Tagalog",
    "hr": "Croatian"
}

def get_config():
    return {
        "shared_db": SHARED_DB,
        "languages": SUPPORTED_LANGUAGES,
        "total_languages": len(SUPPORTED_LANGUAGES)
    }
