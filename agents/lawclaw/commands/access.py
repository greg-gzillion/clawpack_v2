name = "/access"
def run(args, agent=None):
    from shared.accessibility import toggle_braille, toggle_neuralink, toggle_eye, status
    if not args:
        return status() + "\nUsage: /access voice|braille|neuralink|eye on|off"
    parts = args.lower().split()
    if len(parts) < 2:
        return status() + "\nUsage: /access voice|braille|neuralink|eye on|off"
    toggle_type = parts[0]
    if toggle_type == "voice":
        try:
            from shared.accessibility import toggle_voice
            current = toggle_voice(agent)
            return f"Voice mode: {'ON' if current else 'OFF'}"
        except Exception:
            return "Voice toggle unavailable. pip install keyboard speech_recognition"
    elif toggle_type == "braille":
        current = toggle_braille()
        return f"Braille output: {'ON' if current else 'OFF'}"
    elif toggle_type == "neuralink":
        current = toggle_neuralink()
        return f"Neuralink interface: {'ON' if current else 'OFF'}"
    elif toggle_type == "eye":
        current = toggle_eye()
        if current:
            from shared.accessibility_eye_tracker import calibrate
            return f"Eye tracking: ON\n{calibrate()}"
        return "Eye tracking: OFF"
    elif toggle_type == "status":
        return status()
    else:
        return f"Unknown toggle: {toggle_type}. Use: voice, braille, neuralink, eye"
