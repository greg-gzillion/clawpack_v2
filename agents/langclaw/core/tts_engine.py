"""Text-to-Speech Engine for Langclaw"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Optional

class TTSEngine:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.system = platform.system()
    
    def speak(self, text: str, language: str = "en", voice: str = None) -> bool:
        """Speak text using system TTS"""
        try:
            if self.system == "Windows":
                return self._speak_windows(text, voice)
            elif self.system == "Darwin":  # macOS
                return self._speak_mac(text, voice)
            else:  # Linux
                return self._speak_linux(text, voice)
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _speak_windows(self, text: str, voice: str = None) -> bool:
        """Windows TTS using PowerShell"""
        import ctypes
        try:
            # Use Windows SAPI
            cmd = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
            subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            return True
        except:
            # Fallback to basic beep
            print(f"\n🔊 {text}\n")
            return False
    
    def _speak_mac(self, text: str, voice: str = None) -> bool:
        """macOS TTS using say command"""
        voice = voice or "Alex"
        subprocess.run(["say", "-v", voice, text])
        return True
    
    def _speak_linux(self, text: str, voice: str = None) -> bool:
        """Linux TTS using espeak"""
        try:
            subprocess.run(["espeak", text], capture_output=True)
            return True
        except:
            print(f"\n🔊 {text}\n")
            return False
    
    def save_audio(self, text: str, filename: str, language: str = "en") -> Optional[Path]:
        """Save TTS to audio file (requires additional setup)"""
        # This would require external libraries like pyttsx3 or gTTS
        print(f"Audio saving not yet implemented. Text: {text}...")
        return None
