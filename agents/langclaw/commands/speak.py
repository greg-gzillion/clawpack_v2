"""speak command - Cross-platform text-to-speech for language learning"""
import sys
import subprocess
from pathlib import Path

def run(args, agent=None):
    if not args:
        return "Usage: /speak <text>  — Speaks text aloud for pronunciation practice"
    
    text = args.strip()
    platform = sys.platform
    
    try:
        if platform == "win32":
            # Windows SAPI TTS via PowerShell
            ps_script = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak("{text}")'
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True, timeout=15)
            return f"Speaking: {text[:100]}"
        
        elif platform == "darwin":
            # macOS say command
            subprocess.run(["say", text], capture_output=True, timeout=15)
            return f"Speaking: {text[:100]}"
        
        else:
            # Linux espeak
            subprocess.run(["espeak", text], capture_output=True, timeout=10)
            return f"Speaking: {text[:100]}"
    
    except FileNotFoundError:
        return "TTS not available. Install espeak (Linux) or use Windows/macOS."
    except Exception as e:
        return f"TTS error: {str(e)[:100]}"
