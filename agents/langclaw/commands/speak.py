def run(args):
    if not args:
        return "Usage: speak <text>"
    
    import subprocess
    try:
        subprocess.run(["espeak", args], capture_output=True, timeout=10)
        return f"🔊 Speaking: {args}"
    except FileNotFoundError:
        return "🔊 Install espeak: sudo apt install espeak"
