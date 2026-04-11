def run(args):
    """Text-to-speech using espeak"""
    if not args:
        return "Usage: speak <text>"
    
    import subprocess
    import sys
    
    try:
        # Try espeak (Linux)
        result = subprocess.run(
            ["espeak", args],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return f"🔊 Speaking: {args}"
        else:
            return f"🔊 TTS error: {result.stderr}"
    except FileNotFoundError:
        return "🔊 espeak not installed. Run: sudo apt install espeak"
    except Exception as e:
        return f"🔊 Error: {e}"
