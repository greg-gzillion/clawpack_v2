"""Langclaw Configuration"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
WEBCLAW_PATH = Path("str(PROJECT_ROOT)/agents/webclaw/references/langclaw/languages")

# Language code mappings
LANGUAGE_NAMES = {
    "ar": "Arabic", "bg": "Bulgarian", "cs": "Czech", "da": "Danish",
    "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
    "et": "Estonian", "fi": "Finnish", "fr": "French", "he": "Hebrew",
    "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian", "id": "Indonesian",
    "it": "Italian", "ja": "Japanese", "ko": "Korean", "lt": "Lithuanian",
    "lv": "Latvian", "ms": "Malay", "nl": "Dutch", "no": "Norwegian",
    "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian",
    "sk": "Slovak", "sl": "Slovenian", "sv": "Swedish", "th": "Thai",
    "tr": "Turkish", "uk": "Ukrainian", "vi": "Vietnamese", "zh": "Chinese"
}

def get_available_languages():
    """Get list of available languages from webclaw"""
    if WEBCLAW_PATH.exists():
        return [d.name for d in WEBCLAW_PATH.iterdir() if d.is_dir()]
    return []
