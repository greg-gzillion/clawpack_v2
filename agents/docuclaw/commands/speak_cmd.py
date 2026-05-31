name = "/speak"
def run(args, agent=None):
    from shared.speech import speak
    if not args:
        return "/speak <text> - Speak text aloud in current language"
    speak(args)
    return f"[TTS] Speaking: {args[:100]}..."
