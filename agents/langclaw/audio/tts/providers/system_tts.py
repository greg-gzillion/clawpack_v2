"""System TTS Provider - Windows built-in speech"""

import subprocess
import sys

class SystemTTSProvider:
    def speak(self, text: str, lang: str = "en") -> bool:
        """Use Windows SAPI or PowerShell for speech"""
        
        # Try PowerShell (works on all Windows)
        try:
            cmd = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text}")'
            result = subprocess.run(['powershell', '-Command', cmd], 
                                   capture_output=True, timeout=30)
            if result.returncode == 0:
                return True
        except:
            pass
        
        # macOS
        if sys.platform == "darwin":
            try:
                subprocess.run(['say', text], timeout=30)
                return True
            except:
                pass
        
        return False
