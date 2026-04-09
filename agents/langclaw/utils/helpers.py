"""Utility helpers for Langclaw"""

import re

def parse_translate_command(cmd: str):
    """Parse /translate command"""
    match = re.search(r'/(?:translate)\s+(.+?)\s+to\s+(\w+)', cmd)
    if match:
        return {"text": match.group(1), "target": match.group(2)}
    return None

def get_language_flag(lang_code: str) -> str:
    """Get flag emoji for language code"""
    flags = {
        "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪", "it": "🇮🇹", "pt": "🇵🇹",
        "ja": "🇯🇵", "ko": "🇰🇷", "zh": "🇨🇳", "ru": "🇷🇺", "ar": "🇸🇦",
        "hi": "🇮🇳", "vi": "🇻🇳", "th": "🇹🇭", "tr": "🇹🇷", "nl": "🇳🇱"
    }
    return flags.get(lang_code, "🌐")
