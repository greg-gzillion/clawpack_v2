name = "/access"
def run(args, agent=None):
    from shared.accessibility_toggles import toggle_braille, toggle_neuralink, toggle_eye, status
    if not args:
        return status() + "\nUsage: /access braille|neuralink|eye on|off"
    parts = args.lower().split()
    if len(parts) < 2:
        return status() + "\nUsage: /access braille|neuralink|eye on|off"
    toggle_type = parts[0]
    if toggle_type == "braille":
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
        return f"Unknown toggle: {toggle_type}. Use: braille, neuralink, eye"
