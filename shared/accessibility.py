"""
shared/accessibility.py ? Universal Accessibility Layer

Voice, Braille, Neuralink, Eye Tracking, TTS, STT.
System-wide. All 21 agents share this. One background thread.
Constitutional: accessibility is shared infrastructure (Article VI).

Usage:
    from shared.accessibility import speak, listen, toggle_voice, toggle_braille, status
"""
import sys, os, threading, time, re
from pathlib import Path

# ??????????????????????????????????????????????????????????????
# GLOBAL STATE
# ??????????????????????????????????????????????????????????????
_voice_active = False

_braille_active = False
_neuralink_active = False
_eye_active = False

_current_agent = "lawclaw"
_listener_thread = None

# ??????????????????????????????????????????????????????????????
# TEXT TO SPEECH
# ??????????????????????????????????????????????????????????????
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

# ??????????????????????????????????????????????????????????????
# SPEECH TO TEXT
# ??????????????????????????????????????????????????????????????
def listen(timeout=3, phrase_limit=3):
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        r.pause_threshold = 1.2
        r.non_speaking_duration = 0.8
        r.dynamic_energy_threshold = False
        r.pause_threshold = 1.2
        r.non_speaking_duration = 0.8
        r.dynamic_energy_threshold = False
        # Prefer USB microphone over system default
        mic_index = None
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            if 'USB' in name:
                mic_index = i
                break
        mic = sr.Microphone(device_index=mic_index) if mic_index is not None else sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
            r.energy_threshold = r.energy_threshold * 2.0  # Pinned - dynamic disabled  # Pinned - dynamic disabled
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        try:
            return r.recognize_google(audio, language="en-US")
        except:
            return r.recognize_google(audio)
    except ImportError:
        return "[STT] speech_recognition not installed"
    except Exception as e:
        return f"[STT] {str(e)[:100]}"
    
# ??????????????????????????????????????????????????????????????
# LANGUAGE DETECTION & TRANSLATION
# ??????????????????????????????????????????????????????????????
def detect_language(text):
    import re
    if re.search(r"[\u0400-\u04FF]", text): return "ru"
    if re.search(r"[\u0600-\u06FF]", text): return "ar"
    if re.search(r"[\u4E00-\u9FFF]", text): return "zh"
    words = set(text.lower().split())
    if words & {"el","la","los","las","es","de","que","en","un","una","por","para","con","hola","mundo","gracias"}: return "es"
    if words & {"le","la","les","des","est","une","dans","pas","sur","pour","avec","bonjour","merci","monde"}: return "fr"
    if words & {"der","die","das","ist","und","nicht","von","mit","auf","ein","eine","auch","hallo","welt"}: return "de"
    if words & {"il","che","non","una","per","con","sono","nel","gli","ciao","mondo","grazie"}: return "it"
    if words & {"que","nao","uma","para","com","como","mas","dos","das","ola","mundo","obrigado"}: return "pt"
    return "en"
    if words & {"el","la","los","las","es","de","que","en","un","una","por","para","con","hola","mundo","gracias"}: return "es"
    if words & {"le","la","les","des","est","une","dans","pas","sur","pour","avec","bonjour","merci","monde"}: return "fr"
    if words & {"der","die","das","ist","und","nicht","von","mit","auf","ein","eine","auch","hallo","welt"}: return "de"
    if words & {"il","che","non","una","per","con","sono","nel","gli","ciao","mondo","grazie"}: return "it"
    if words & {"que","nao","uma","para","com","como","mas","dos","das","ola","mundo","obrigado"}: return "pt"
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

# ??????????????????????????????????????????????????????????????
# BRAILLE
# ??????????????????????????????????????????????????????????????
def to_braille(text):
    bm = {"a":"\u2801","b":"\u2803","c":"\u2809","d":"\u2819","e":"\u2811","f":"\u280B","g":"\u281B","h":"\u2813","i":"\u280A","j":"\u281A","k":"\u2805","l":"\u2807","m":"\u280D","n":"\u281D","o":"\u2815","p":"\u280F","q":"\u281F","r":"\u2817","s":"\u280E","t":"\u281E","u":"\u2825","v":"\u2827","w":"\u283A","x":"\u282D","y":"\u282D","z":"\u2835"," ":" "}
    return "".join(bm.get(c, c) for c in text.lower())

# ??????????????????????????????????????????????????????????????
# COMBINED FUNCTIONS
# ??????????????????????????????????????????????????????????????
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

# ??????????????????????????????????????????????????????????????
# TOGGLES ? Voice, Braille, Neuralink, Eye
# ??????????????????????????????????????????????????????????????

def toggle_braille():
    global _braille_active
    _braille_active = not _braille_active
    return _braille_active

def toggle_neuralink():
    global _neuralink_active
    _neuralink_active = not _neuralink_active
    return _neuralink_active

def toggle_eye():
    global _eye_active
    _eye_active = not _eye_active
    return _eye_active

def is_braille_active():
    return _braille_active

def is_neuralink_active():
    return _neuralink_active

def is_eye_active():
    return _eye_active

def get_active():
    active = []
    if _braille_active: active.append('BRAILLE')
    if _neuralink_active: active.append('NEURALINK')
    if _eye_active: active.append('EYE')
    if _voice_active: active.append('VOICE')
    return active

def status():
    parts = get_active()
    if not parts:
        return 'Accessibility toggles: none active. Use /access voice|braille|neuralink|eye on|off'
    return 'Active: ' + ' | '.join(parts)

# ??????????????????????????????????????????????????????????????
# VOICE LOOP ? System-wide background listener
# ??????????????????????????????????????????????????????????????

def _listen_loop():
    global _voice_active, _current_agent
    from shared.accessibility import listen_and_translate, translate, speak
    import time as _time
    awake = True
    last_speech = _time.time()
    last_indicator = ''
    while _voice_active:
        try:
            indicator = '?' if awake else '?'
            if indicator != last_indicator:
                print(f"\n[VOICE] {indicator} {'Listening...' if awake else 'Sleeping (say start listening)'}", flush=True)
                last_indicator = indicator
            text, lang, translated = listen_and_translate('en')
            if not text or text.startswith('[STT]'):
                if False and _time.time() - last_speech > 120 and awake:
                    awake = False
                    print("[VOICE] Auto-sleeping. Say 'start listening' to wake.", flush=True)
                continue
            last_speech = _time.time()
            tlow = text.lower().strip()
            if 'start listening' in tlow or 'wake up' in tlow:
                awake = True
                print("[VOICE] Awake! ?", flush=True)
                continue
            if 'stop listening' in tlow or 'go to sleep' in tlow:
                awake = False
                print("[VOICE] Sleeping. Say 'start listening' to wake.", flush=True)
                continue
            if 'switch to' in tlow:
                spoken = tlow.replace('switch to', '').strip()
                # Map spoken names to actual agent names (no underscores)
                agent_map = {
                    'law claw': 'lawclaw', 'law': 'lawclaw',
                    'flow claw': 'flowclaw', 'flow': 'flowclaw',
                    'medic claw': 'mediclaw', 'medical': 'mediclaw',
                    'web claw': 'webclaw', 'web': 'webclaw',
                    'coder': 'claw_coder', 'code': 'claw_coder',
                    'plot': 'plotclaw', 'chart': 'plotclaw',
                    'document': 'docuclaw', 'doc': 'docuclaw',
                    'data': 'dataclaw', 'file': 'fileclaw',
                    'blockchain': 'txclaw', 'dream': 'dreamclaw',
                    'draw': 'drawclaw', 'draft': 'draftclaw',
                    'design': 'designclaw', 'rust': 'crustyclaw',
                    'translate': 'interpretclaw', 'language': 'langclaw',
                    'liberate': 'liberateclaw', 'model': 'llmclaw',
                    'math': 'mathematicaclaw', 'crawler': 'rustypycraw',
                }
                # First try exact match with underscores removed
                agent = spoken.replace(' ', '_').replace('__', '_')
                # Then try the map
                for key, val in agent_map.items():
                    if key in spoken:
                        agent = val
                        break
                all_agents = ['lawclaw','mediclaw','webclaw','claw_coder','plotclaw','flowclaw','docuclaw','dataclaw','fileclaw','txclaw','dreamclaw','drawclaw','draftclaw','designclaw','crustyclaw','rustypycraw','interpretclaw','langclaw','liberateclaw','llmclaw','mathematicaclaw']
                if agent in all_agents:
                    _current_agent = agent
                    print(f"[VOICE] Switched to {agent}", flush=True)
                else:
                    print(f"[VOICE] Unknown agent: {spoken}. Try: law, medic, code, plot, flow, web, data, dream, draw", flush=True)
                continue
            if not awake:
                continue
            print(f"[VOICE] {lang.upper()}: {text[:100]}")
            if translated:
                # DEBUG: Step 1 - Raw transcript
                print(f"[VOICE RAW] '{translated[:120]}'", flush=True)
                # Auto-prefix / for known commands
                tlow = translated.lower().strip()
                known_cmds = ['court','jurisdiction','law','cite','statute','docket','police','detention','library','hospital','help','stats','search','analyze','ask','brief','federal','state','judge','precedent','oral','summarize','list','browse','correct','access','voice','language','code','plot','math','diagnose','translate','doc','draft','dream','draw','design','flow','contract','agreement','motion','filing','research','lookup','find','show','get','tell','what','who']
                prefixed = False
                # Flexible command detection - find command word anywhere in utterance
                state_map = {
                    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
                    'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
                    'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
                    'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
                    'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
                    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
                    'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
                    'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
                    'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
                    'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
                    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
                    'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
                    'wisconsin': 'WI', 'wyoming': 'WY', 'dc': 'DC', 'district of columbia': 'DC',
                }
                phrase_map = {
                    'contract': 'doc', 'agreement': 'doc', 'motion': 'doc', 'filing': 'doc',
                    'research': 'law', 'lookup': 'search', 'find': 'search',
                    'show': 'jurisdiction', 'get': 'search', 'tell': 'ask', 'what': 'ask', 'who': 'ask',
                }
                words = tlow.split()
                # Find command word anywhere in the utterance
                found_cmd = None
                for word in words:
                    if word in known_cmds:
                        found_cmd = word
                        break
                    if word in phrase_map:
                        found_cmd = phrase_map[word]
                        break
                if found_cmd:
                    # Build command: remove the command word, map state names to codes
                    rest = [w for w in words if w != found_cmd and w not in phrase_map]
                    # Replace full state names with codes
                    for i, w in enumerate(rest):
                        if w in state_map:
                            rest[i] = state_map[w]
                        # Check two-word state names
                        if i > 0 and f'{rest[i-1]} {w}' in state_map:
                            rest[i-1] = state_map[f'{rest[i-1]} {w}']
                            rest[i] = ''
                    rest = [w for w in rest if w]
                    translated = '/' + found_cmd + (' ' + ' '.join(rest) if rest else '')
                    prefixed = True
                # DEBUG: Step 2 - After prefix
                print(f"[VOICE PREFIXED] prefix={prefixed} -> '{translated[:120]}'", flush=True)
                # Push to event bus for menu-level agent switching
                try:
                    from shared.event_bus import push_event, EventIntent
                    if tlow in ('law','medic','flow','code','plot','data','web','file','dream','draw','draft','design','rust','translate','language','math','liberate','model','doc','blockchain','tx','help','menu','quit','exit','back','select','open','switch') or tlow.startswith('select ') or tlow.startswith('open ') or tlow.startswith('switch '):
                        push_event('voice', 'switch_agent', {'name': tlow}, raw_text=translated)
                    else:
                        push_event('voice', 'run_command', {'task': translated, 'agent': _current_agent}, raw_text=translated, agent=_current_agent)
                except Exception:
                    pass
                try:
                    import requests as _req, json as _json
                    r = _req.post(f'http://127.0.0.1:8766/v1/message/{_current_agent}',
                        json={'task': translated}, timeout=120)
                    if r.status_code == 200:
                        resp = r.json().get('result', '')
                        print(f"[VOICE] Response: {resp[:300]}")
                        if lang and lang != 'en':
                            final = translate(resp[:1000], lang, 'en')
                            speak(final, lang)
                    else:
                        print(f"[VOICE] Error: {r.status_code}")
                except Exception as e:
                    print(f"[VOICE] Error: {str(e)[:100]}")
        except Exception as e:
            print(f"[VOICE] Loop error: {str(e)[:100]}")
            _time.sleep(1)

def toggle_voice(agent_name=None, silent=False):
    global _voice_active, _listener_thread, _current_agent
    if agent_name:
        # Extract string name if passed an object
        if hasattr(agent_name, 'name'):
            _current_agent = agent_name.name
        elif isinstance(agent_name, str):
            _current_agent = agent_name
    _voice_active = not _voice_active
    if _voice_active:
        _listener_thread = threading.Thread(target=_listen_loop, daemon=True)
        _listener_thread.start()
        print("[VOICE] ? Voice mode active. Say 'stop listening' to sleep.", flush=True)
        return True
    else:
        print("[VOICE] ? Voice mode deactivated.", flush=True)
        return False

def is_voice_active():
    return _voice_active
