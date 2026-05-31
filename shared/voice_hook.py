import sys, threading

_voice_active = False
_listener_thread = None
_current_agent = None

BANNER_ON = '\n' + '='*60 + '\n  MIC ACTIVE - Speak now. Ctrl+Shift+V to deactivate.\n' + '='*60 + '\n'
BANNER_OFF = '\n' + '='*60 + '\n  VOICE MODE OFF.\n' + '='*60 + '\n'

def is_active():
    return _voice_active

def set_agent(agent_handler):
    global _current_agent
    _current_agent = agent_handler

def _listen_loop():
    global _voice_active, _current_agent
    from shared.accessibility import listen_and_translate, translate, speak
    while _voice_active:
        try:
            print("\n[VOICE] Listening...")
            text, lang, translated = listen_and_translate('en')
            if text.startswith('[STT]'):
                print(f"[VOICE] {text}")
                continue
            print(f"[VOICE] {lang.upper()}: {text[:100]}")
            if _current_agent and translated:
                print(f"[VOICE] Processing: {translated[:100]}")
                response = _current_agent.handle(translated)
                response_text = response.get('result', str(response))
                if lang and lang != 'en':
                    final = translate(response_text, lang, 'en')
                else:
                    final = response_text
                print(f"[VOICE] Response: {final[:200]}...")
                speak(final, lang or 'en')
            else:
                speak("Voice mode active.", 'en')
        except Exception as e:
            print(f"[VOICE] Error: {str(e)[:100]}")
            import time
            time.sleep(1)

def toggle(agent_handler=None):
    global _voice_active, _listener_thread, _current_agent
    if agent_handler:
        _current_agent = agent_handler
    _voice_active = not _voice_active
    if _voice_active:
        _listener_thread = threading.Thread(target=_listen_loop, daemon=True)
        _listener_thread.start()
        return BANNER_ON
    else:
        return BANNER_OFF

try:
    import keyboard
    _kb = True
except ImportError:
    _kb = False

def register_hotkey(agent_handler=None):
    global _current_agent
    if agent_handler:
        _current_agent = agent_handler
    if not _kb:
        print("[VOICE] pip install keyboard for Ctrl+Shift+V hotkey")
        print("[VOICE] Use /voice command instead.")
        return False
    def on_hotkey():
        msg = toggle(_current_agent)
        print(msg)
    keyboard.add_hotkey('ctrl+shift+v', on_hotkey)
    keyboard.add_hotkey('ctrl+shift+b', lambda: print(toggle_braille()))
    keyboard.add_hotkey('ctrl+shift+n', lambda: print(toggle_neuralink()))
    keyboard.add_hotkey('ctrl+shift+e', lambda: print(toggle_eye()))
    print('[ACCESSIBILITY] Hotkeys: Ctrl+Shift+V=voice B=braille N=neuralink E=eye')
    print("[VOICE] Ctrl+Shift+V registered for voice toggle.")
    return True

def unregister_hotkey():
    if _kb:
        try:
            keyboard.remove_hotkey('ctrl+shift+v')
            keyboard.remove_hotkey('ctrl+shift+b')
            keyboard.remove_hotkey('ctrl+shift+n')
            keyboard.remove_hotkey('ctrl+shift+e')
        except:
            pass
