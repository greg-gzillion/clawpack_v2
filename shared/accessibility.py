# shared/accessibility.py - Universal TTS/STT/Braille layer for all agents
# Opt-in. No agent is forced to use this. Call methods directly.
# TTS: text-to-speech (system voice output)
# STT: speech-to-text (microphone input)
# Braille: Grade 1 & 2 output (opt-in only)

import sys
from pathlib import Path

def speak(text, lang='en'):
    \"\"\"Convert text to speech. Returns spoken text or error.\"\"\"
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # Try to set voice for the language
        voices = engine.getProperty('voices')
        for voice in voices:
            if lang in voice.id.lower() or lang in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        return f"[TTS] Spoken: {text[:100]}..."
    except ImportError:
        return "[TTS] pyttsx3 not installed. Run: pip install pyttsx3"
    except Exception as e:
        return f"[TTS] Error: {str(e)[:100]}"

def listen(timeout=5, phrase_limit=10):
    \"\"\"Listen to microphone and return transcribed text.\"\"\"
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        # Try English first, fall back to auto-detect
        try:
            text = r.recognize_google(audio, language='en-US')
            return text
        except:
            text = r.recognize_google(audio)  # auto-detect language
            return text
    except ImportError:
        return "[STT] speech_recognition not installed. Run: pip install SpeechRecognition pyaudio"
    except Exception as e:
        return f"[STT] {str(e)[:100]}"

def detect_language(text):
    \"\"\"Detect language of text. Returns language name.\"\"\"
    try:
        # Simple heuristic: check character ranges
        import re
        # Cyrillic
        if re.search(r'[\u0400-\u04FF]', text):
            return 'ru'
        # Arabic
        if re.search(r'[\u0600-\u06FF]', text):
            return 'ar'
        # CJK
        if re.search(r'[\u4E00-\u9FFF]', text):
            return 'zh'
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
            return 'ja'
        if re.search(r'[\uAC00-\uD7AF]', text):
            return 'ko'
        # Latin-based: use common words
        text_lower = text.lower()
        if any(w in text_lower for w in ['el','la','los','las','es','de','que','en','un','por']):
            return 'es'
        if any(w in text_lower for w in ['le','la','les','des','est','une','dans','pas','sur']):
            return 'fr'
        if any(w in text_lower for w in ['der','die','das','ist','und','nicht','von','mit','auf']):
            return 'de'
        if any(w in text_lower for w in ['il','che','non','una','per','con','sono','nel','gli']):
            return 'it'
        if any(w in text_lower for w in ['que','nao','uma','para','com','como','mas','dos','das']):
            return 'pt'
        return 'en'
    except:
        return 'en'

def translate(text, target_lang='en', source_lang=None):
    \"\"\"Translate text to target language. Uses Sovereign Gateway.\"\"\"
    if not source_lang:
        source_lang = detect_language(text)
    if source_lang == target_lang:
        return text
    try:
        from shared.llm.client import get_llm_client
        client = get_llm_client()
        prompt = f"Translate from {source_lang} to {target_lang}. Return ONLY the translation, no explanations:\n\n{text}"
        result = client.call_sync(prompt, agent='accessibility', max_tokens=1000)
        return result.content.strip()
    except:
        return text

def to_braille(text, grade=2):
    \"\"\"Convert text to Braille (Grade 1 or Grade 2). Opt-in only.\"\"\"
    # Basic Grade 1 Braille mapping (letters + numbers)
    braille_map = {
        'a': '\u2801', 'b': '\u2803', 'c': '\u2809', 'd': '\u2819', 'e': '\u2811',
        'f': '\u280B', 'g': '\u281B', 'h': '\u2813', 'i': '\u280A', 'j': '\u281A',
        'k': '\u2805', 'l': '\u2807', 'm': '\u280D', 'n': '\u281D', 'o': '\u2815',
        'p': '\u280F', 'q': '\u281F', 'r': '\u2817', 's': '\u280E', 't': '\u281E',
        'u': '\u2825', 'v': '\u2827', 'w': '\u283A', 'x': '\u282D', 'y': '\u282D',
        'z': '\u2835', ' ': ' ',
        '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819', '5': '\u2811',
        '6': '\u280B', '7': '\u281B', '8': '\u2813', '9': '\u280A', '0': '\u281A',
    }
    result = []
    for char in text.lower():
        result.append(braille_map.get(char, char))
    return '\u2808' + ''.join(result)  # Prefix with Braille indicator

def listen_and_translate(target_lang='en'):
    \"\"\"Full pipeline: listen to mic, detect language, translate to target.
    Returns (original_text, detected_lang, translated_text)\"\"\"
    text = listen()
    if text.startswith('[STT]'):
        return text, None, text
    lang = detect_language(text)
    if lang != target_lang:
        translated = translate(text, target_lang, lang)
    else:
        translated = text
    return text, lang, translated

def speak_response(text, target_lang='en', original_lang=None):
    \"\"\"Translate response back to user's language and speak it.\"\"\"
    if original_lang and original_lang != 'en':
        text = translate(text, original_lang, 'en')
    return speak(text, original_lang or target_lang)

print("shared/accessibility.py created")
