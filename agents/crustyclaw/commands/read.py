name = "/read"
def run(args, agent=None):
    from shared.speech import speak, list_voices, set_voice, set_rate, stop, read_file, get_current_voice_info
    if not args:
        return "TTS READER\n/read <text> - Read aloud\n/read file <path> - Read file\n/read voices - List voices\n/read voice <lang> <num> - Set voice\n/read rate <lang> <wpm> - Set speed\n/read info - Voice settings\n/read stop - Stop"
    parts = args.split(maxsplit=2)
    cmd = parts[0].lower()
    if cmd == 'voices':
        return list_voices()
    elif cmd == 'voice' and len(parts) >= 3:
        return set_voice(parts[1], int(parts[2]))
    elif cmd == 'rate' and len(parts) >= 3:
        return set_rate(parts[1], int(parts[2]))
    elif cmd == 'file' and len(parts) >= 2:
        return read_file(parts[1])
    elif cmd == 'stop':
        return stop()
    elif cmd == 'info':
        return get_current_voice_info()
    else:
        speak(args)
        return f"[TTS] Reading: {args[:100]}..."
