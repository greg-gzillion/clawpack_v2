name = "/read"
def run(args, agent=None):
    """Text-to-speech reader with voice selection.
    /read <text>           - Read text aloud with default voice
    /read file <path>      - Read a file aloud
    /read voice <name>     - Select TTS voice
    /read voices           - List available voices
    /read stop             - Stop reading
    /read speed <rate>     - Set reading speed (100-300 words/min, default 150)"""
    from shared.accessibility import speak
    
    if not args:
        return "Usage: /read <text> | /read file <path> | /read voice <name> | /read voices | /read speed <rate> | /read stop"
    
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
                result += f"  [{i}] {v.name} ({v.id[:30]}...)\n"
                result += f"      Languages: {v.languages}\n"
            return result
        except ImportError:
            return "[TTS] pyttsx3 not installed. Run: pip install pyttsx3"
    
    elif cmd == 'voice' and rest:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            # Try numeric index first, then name match
            try:
                idx = int(rest)
                if 0 <= idx < len(voices):
                    engine.setProperty('voice', voices[idx].id)
                    # Save preference
                    import json
                    prefs = {}
                    try:
                        with open('data/tts_prefs.json') as f:
                            prefs = json.load(f)
                    except:
                        pass
                    prefs['voice_index'] = idx
                    prefs['voice_name'] = voices[idx].name
                    with open('data/tts_prefs.json', 'w') as f:
                        json.dump(prefs, f)
                    return f"[TTS] Voice set to: {voices[idx].name}"
            except ValueError:
                for v in voices:
                    if rest.lower() in v.name.lower():
                        engine.setProperty('voice', v.id)
                        return f"[TTS] Voice set to: {v.name}"
            return f"[TTS] Voice '{rest}' not found. Use /read voices to list."
        except ImportError:
            return "[TTS] pyttsx3 not installed."
    
    elif cmd == 'speed' and rest:
        try:
            rate = int(rest)
            rate = max(50, min(400, rate))
            import json
            prefs = {}
            try:
                with open('data/tts_prefs.json') as f:
                    prefs = json.load(f)
            except:
                pass
            prefs['speed'] = rate
            with open('data/tts_prefs.json', 'w') as f:
                json.dump(prefs, f)
            return f"[TTS] Reading speed set to {rate} words/min"
        except ValueError:
            return "[TTS] Speed must be a number (50-400)"
    
    elif cmd == 'file' and rest:
        try:
            with open(rest, 'r', encoding='utf-8') as f:
                text = f.read()
            # Load saved voice preference
            import json
            lang = 'en'
            try:
                with open('data/tts_prefs.json') as f:
                    prefs = json.load(f)
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
            except:
                pass
            # Truncate if too long
            if len(text) > 50000:
                text = text[:50000] + "... [truncated at 50000 chars]"
            speak(text)
            return f"[TTS] Reading file: {rest} ({len(text)} chars)"
        except FileNotFoundError:
            return f"[TTS] File not found: {rest}"
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"
    
    elif cmd == 'stop':
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.stop()
            return "[TTS] Stopped."
        except:
            return "[TTS] Nothing to stop."
    
    else:
        # Read the text directly
        try:
            import json
            lang = 'en'
            try:
                with open('data/tts_prefs.json') as f:
                    prefs = json.load(f)
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
            except:
                pass
            speak(args)
            return f"[TTS] Reading: {args[:100]}..."
        except Exception as e:
            return f"[TTS] Error: {str(e)[:100]}"
