# shared/locale.py - System-wide language preference
# All agent responses translated to user's language automatically.
# Agents work in English internally. Translation at A2A boundary.
# /language es -> Spanish everywhere. /language en -> back to English.

import os

_user_language = 'en'
_supported = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese',
    'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
    'nl': 'Dutch', 'pl': 'Polish', 'sv': 'Swedish', 'tr': 'Turkish',
    'vi': 'Vietnamese', 'th': 'Thai', 'el': 'Greek', 'he': 'Hebrew'
}

def set_language(lang_code):
    """Set system-wide language. Returns confirmation message."""
    global _user_language
    lang_code = lang_code.lower().strip()
    if lang_code in _supported:
        _user_language = lang_code
        return f"[LANGUAGE] Set to {_supported[lang_code]} ({lang_code}). All responses will be in {_supported[lang_code]}."
    else:
        codes = ', '.join(_supported.keys())
        return f"[LANGUAGE] Unknown code: {lang_code}. Supported: {codes}"

def get_language():
    return _user_language

def get_language_name():
    return _supported.get(_user_language, 'English')

def needs_translation():
    """Returns True if user language is not English."""
    return _user_language != 'en'

def translate_response(text):
    """Translate response to user's language if needed. Returns original if English."""
    if not needs_translation():
        return text
    try:
        from shared.accessibility import translate
        return translate(text, _user_language, 'en')
    except:
        return text

def list_languages():
    """Return formatted list of supported languages."""
    lines = ["Supported languages:"]
    for code, name in sorted(_supported.items()):
        marker = " <-- CURRENT" if code == _user_language else ""
        lines.append(f"  {code}: {name}{marker}")
    return '\n'.join(lines)

print('shared/locale.py created')
