# shared/accessibility.py - Universal TTS/STT/Braille layer
import sys
from pathlib import Path

def speak(text, lang="en"):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        for voice in voices:
            if lang in voice.id.lower() or lang in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        return f"[TTS] Spoken: {text[:100]}..."
    except ImportError:
        return "[TTS] pyttsx3 not installed"
    except Exception as e:
        return f"[TTS] Error: {str(e)[:100]}"

def listen(timeout=5, phrase_limit=10):
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        try:
            return r.recognize_google(audio, language="en-US")
        except:
            return r.recognize_google(audio)
    except ImportError:
        return "[STT] speech_recognition not installed"
    except Exception as e:
        return f"[STT] {str(e)[:100]}"

def detect_language(text):
    import re
    if re.search(r"[\u0400-\u04FF]", text): return "ru"
    if re.search(r"[\u0600-\u06FF]", text): return "ar"
    if re.search(r"[\u4E00-\u9FFF]", text): return "zh"
    t = text.lower()
    if any(w in t for w in ["el","la","los","es","de","que","en"]): return "es"
    if any(w in t for w in ["le","la","les","des","une","dans"]): return "fr"
    if any(w in t for w in ["der","die","das","ist","und"]): return "de"
    return "en"

def translate(text, target_lang="en", source_lang=None):
    if not source_lang: source_lang = detect_language(text)
    if source_lang == target_lang: return text
    try:
        from shared.llm.client import get_llm_client
        client = get_llm_client()
        prompt = f"Translate from {source_lang} to {target_lang}. Return ONLY the translation:\n\n{text}"
        result = client.call_sync(prompt, agent="accessibility", max_tokens=1000)
        return result.content.strip()
    except:
        return text

def to_braille(text):
    bm = {"a":"\u2801","b":"\u2803","c":"\u2809","d":"\u2819","e":"\u2811","f":"\u280B","g":"\u281B","h":"\u2813","i":"\u280A","j":"\u281A","k":"\u2805","l":"\u2807","m":"\u280D","n":"\u281D","o":"\u2815","p":"\u280F","q":"\u281F","r":"\u2817","s":"\u280E","t":"\u281E","u":"\u2825","v":"\u2827","w":"\u283A","x":"\u282D","y":"\u282D","z":"\u2835"," ":" "}
    return "".join(bm.get(c, c) for c in text.lower())

def listen_and_translate(target_lang="en"):
    text = listen()
    if text.startswith("[STT]"): return text, None, text
    lang = detect_language(text)
    return text, lang, translate(text, target_lang, lang) if lang != target_lang else text

def speak_response(text, target_lang="en", original_lang=None):
    if original_lang and original_lang != "en": text = translate(text, original_lang, "en")
    return speak(text, original_lang or target_lang)

def read_aloud(args):
    from shared.speech import speak as tts, list_voices, set_voice, set_rate, stop, read_file, get_current_voice_info
    if not args: return "/read <text> | /read voices | /read voice <lang> <num> | /read rate <lang> <wpm> | /read file <path> | /read stop"
    parts = args.split(maxsplit=2)
    cmd = parts[0].lower()
    if cmd == "voices": return list_voices()
    elif cmd == "voice" and len(parts) >= 3: return set_voice(parts[1], int(parts[2]))
    elif cmd == "rate" and len(parts) >= 3: return set_rate(parts[1], int(parts[2]))
    elif cmd == "file" and len(parts) >= 2: return read_file(parts[1])
    elif cmd == "stop": return stop()
    elif cmd == "info": return get_current_voice_info()
    else:
        tts(args)
        return f"[TTS] Reading: {args[:100]}..."
