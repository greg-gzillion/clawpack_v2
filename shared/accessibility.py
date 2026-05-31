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
def voice_mode(agent_handler, target_lang='en'):
    """Universal voice mode for any agent. 
    Listens, translates, processes through the agent, translates response back, speaks it.
    Usage in any agent handler:
        elif cmd == "/voice":
            from shared.accessibility import voice_mode
            result = voice_mode(self)
    """
    print("[VOICE] Listening... (speak now)")
    text, lang, translated = listen_and_translate(target_lang)
    if text.startswith('[STT]'):
        return text
    
    print(f"[VOICE] Detected: {lang} -> "{text[:80]}..."")
    print(f"[VOICE] Translated: "{translated[:80]}..."")
    
    # Process through the agent
    response = agent_handler.handle(translated)
    response_text = response.get('result', str(response))
    
    # Translate response back if needed
    if lang and lang != target_lang:
        print(f"[VOICE] Translating response to {lang}...")
        final_text = translate(response_text, lang, target_lang)
    else:
        final_text = response_text
    
    # Speak the response
    print(f"[VOICE] Speaking response...")
    speak(final_text, lang or target_lang)
    
    return f"[VOICE] ({lang.upper()}) {text}\n-> {translated}\n\nResponse: {response_text[:500]}"

def voice_mode(agent_handler, target_lang='en'):
    """Universal voice mode for any agent. 
    Listens, translates, processes through the agent, translates response back, speaks it.
    Usage in any agent handler:
        elif cmd == "/voice":
            from shared.accessibility import voice_mode
            result = voice_mode(self)
    """
    print("[VOICE] Listening... (speak now)")
    text, lang, translated = listen_and_translate(target_lang)
    if text.startswith('[STT]'):
        return text
    
    print(f"[VOICE] Detected: {lang} -> "{text[:80]}..."")
    print(f"[VOICE] Translated: "{translated[:80]}..."")
    
    # Process through the agent
    response = agent_handler.handle(translated)
    response_text = response.get('result', str(response))
    
    # Translate response back if needed
    if lang and lang != target_lang:
        print(f"[VOICE] Translating response to {lang}...")
        final_text = translate(response_text, lang, target_lang)
    else:
        final_text = response_text
    
    # Speak the response
    print(f"[VOICE] Speaking response...")
    speak(final_text, lang or target_lang)
    
    return f"[VOICE] ({lang.upper()}) {text}\n-> {translated}\n\nResponse: {response_text[:500]}"


def read_aloud(args):
    """TTS reader with voice selection. Called by /read command."""
    if not args:
        return "TTS READER\n/read <text> - Read aloud\n/read voices - List voices\n/read voice 0 - Switch voice\n/read speed 150 - Set speed\n/read file <path> - Read file\n/read stop - Stop"
    
    parts = args.split(maxsplit=1)
    cmd = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""
    
    if cmd == 'voices':
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            result = "Available TTS Voices:\n"
            for i, v in enumerate(voices):
                gender = 'Female' if 'zira' in v.name.lower() or 'sabina' in v.name.lower() else 'Male'
                result += f"  [{i}] {v.name} ({gender})\n      Languages: {v.languages}\n"
            return result
        except ImportError:
            return "[TTS] pyttsx3 not installed. Run: pip install pyttsx3"
    
    elif cmd == 'voice' and rest:
        try:
            import pyttsx3, json
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            try:
                idx = int(rest)
                if 0 <= idx < len(voices):
                    engine.setProperty('voice', voices[idx].id)
                    prefs = {}
                    try:
                        with open('data/tts_prefs.json') as f: prefs = json.load(f)
                    except: pass
                    prefs['voice_index'] = idx
                    prefs['voice_name'] = voices[idx].name
                    with open('data/tts_prefs.json', 'w') as f: json.dump(prefs, f)
                    return f"[TTS] Voice set to: {voices[idx].name}"
            except ValueError:
                for v in voices:
                    if rest.lower() in v.name.lower():
                        return f"[TTS] Voice set to: {v.name}"
            return f"[TTS] Voice '{rest}' not found."
        except ImportError:
            return "[TTS] pyttsx3 not installed."
    
    elif cmd == 'speed' and rest:
        try:
            import json
            rate = max(50, min(400, int(rest)))
            prefs = {}
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
            except: pass
            prefs['speed'] = rate
            with open('data/tts_prefs.json', 'w') as f: json.dump(prefs, f)
            return f"[TTS] Reading speed set to {rate} words/min"
        except ValueError:
            return "[TTS] Speed must be a number (50-400)"
    
    elif cmd == 'file' and rest:
        try:
            import json
            with open(rest, 'r', encoding='utf-8') as f: text = f.read()
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
                if 'voice_index' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    if prefs['voice_index'] < len(voices):
                        engine.setProperty('voice', voices[prefs['voice_index']].id)
                if 'speed' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', prefs['speed'])
            except: pass
            if len(text) > 50000: text = text[:50000] + "... [truncated]"
            speak(text)
            return f"[TTS] Reading file: {rest} ({len(text)} chars)"
        except FileNotFoundError:
            return f"[TTS] File not found: {rest}"
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"
    
    elif cmd == 'stop':
        try:
            import pyttsx3
            pyttsx3.init().stop()
            return "[TTS] Stopped."
        except:
            return "[TTS] Nothing to stop."
    
    else:
        try:
            import json
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
                if 'voice_index' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    if prefs['voice_index'] < len(voices):
                        engine.setProperty('voice', voices[prefs['voice_index']].id)
                if 'speed' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', prefs['speed'])
            except: pass
            speak(args)
            return f"[TTS] Reading: {args[:100]}..."
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"

def read_aloud(args):
    """TTS reader with voice selection. Called by /read command."""
    if not args:
        return "TTS READER\n/read <text> - Read aloud\n/read voices - List voices\n/read voice 0 - Switch voice\n/read speed 150 - Set speed\n/read file <path> - Read file\n/read stop - Stop"
    
    parts = args.split(maxsplit=1)
    cmd = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""
    
    if cmd == 'voices':
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            result = "Available TTS Voices:\n"
            for i, v in enumerate(voices):
                gender = 'Female' if 'zira' in v.name.lower() or 'sabina' in v.name.lower() else 'Male'
                result += f"  [{i}] {v.name} ({gender})\n      Languages: {v.languages}\n"
            return result
        except ImportError:
            return "[TTS] pyttsx3 not installed. Run: pip install pyttsx3"
    
    elif cmd == 'voice' and rest:
        try:
            import pyttsx3, json
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            try:
                idx = int(rest)
                if 0 <= idx < len(voices):
                    engine.setProperty('voice', voices[idx].id)
                    prefs = {}
                    try:
                        with open('data/tts_prefs.json') as f: prefs = json.load(f)
                    except: pass
                    prefs['voice_index'] = idx
                    prefs['voice_name'] = voices[idx].name
                    with open('data/tts_prefs.json', 'w') as f: json.dump(prefs, f)
                    return f"[TTS] Voice set to: {voices[idx].name}"
            except ValueError:
                for v in voices:
                    if rest.lower() in v.name.lower():
                        return f"[TTS] Voice set to: {v.name}"
            return f"[TTS] Voice '{rest}' not found."
        except ImportError:
            return "[TTS] pyttsx3 not installed."
    
    elif cmd == 'speed' and rest:
        try:
            import json
            rate = max(50, min(400, int(rest)))
            prefs = {}
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
            except: pass
            prefs['speed'] = rate
            with open('data/tts_prefs.json', 'w') as f: json.dump(prefs, f)
            return f"[TTS] Reading speed set to {rate} words/min"
        except ValueError:
            return "[TTS] Speed must be a number (50-400)"
    
    elif cmd == 'file' and rest:
        try:
            import json
            with open(rest, 'r', encoding='utf-8') as f: text = f.read()
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
                if 'voice_index' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    if prefs['voice_index'] < len(voices):
                        engine.setProperty('voice', voices[prefs['voice_index']].id)
                if 'speed' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', prefs['speed'])
            except: pass
            if len(text) > 50000: text = text[:50000] + "... [truncated]"
            speak(text)
            return f"[TTS] Reading file: {rest} ({len(text)} chars)"
        except FileNotFoundError:
            return f"[TTS] File not found: {rest}"
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"
    
    elif cmd == 'stop':
        try:
            import pyttsx3
            pyttsx3.init().stop()
            return "[TTS] Stopped."
        except:
            return "[TTS] Nothing to stop."
    
    else:
        try:
            import json
            try:
                with open('data/tts_prefs.json') as f: prefs = json.load(f)
                if 'voice_index' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    if prefs['voice_index'] < len(voices):
                        engine.setProperty('voice', voices[prefs['voice_index']].id)
                if 'speed' in prefs:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', prefs['speed'])
            except: pass
            speak(args)
            return f"[TTS] Reading: {args[:100]}..."
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"
