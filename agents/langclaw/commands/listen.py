# agents/langclaw/commands/listen.py
name = "/listen"
def run(args, agent=None):
    '''Listen to microphone and transcribe'''
    from shared.accessibility import listen, detect_language
    text = listen()
    if text.startswith('[STT]'):
        return text
    lang = detect_language(text)
    return f"[{lang.upper()}] {text}"
