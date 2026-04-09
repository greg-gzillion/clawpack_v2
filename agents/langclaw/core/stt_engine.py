"""Speech-to-Text Engine for Langclaw"""

import subprocess
import platform
from typing import Optional
from pathlib import Path

class STTEngine:
    def __init__(self):
        self.system = platform.system()
        self.listening = False
    
    def listen(self, timeout: int = 5, language: str = "en-US") -> Optional[str]:
        """Listen for speech and convert to text"""
        print("\n🎤 Listening... (speak now)")
        
        try:
            if self.system == "Windows":
                return self._listen_windows(timeout, language)
            elif self.system == "Darwin":  # macOS
                return self._listen_mac(timeout)
            else:  # Linux
                return self._listen_linux(timeout)
        except Exception as e:
            print(f"STT Error: {e}")
            return None
    
    def _listen_windows(self, timeout: int, language: str) -> Optional[str]:
        """Windows speech recognition"""
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1)
                print(f"Listening for {timeout} seconds...")
                audio = r.listen(source, timeout=timeout)
                
            try:
                text = r.recognize_google(audio, language=language)
                print(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Recognition service error: {e}")
                return None
        except ImportError:
            print("Speech recognition not available. Install: pip install SpeechRecognition pyaudio")
            return None
    
    def _listen_mac(self, timeout: int) -> Optional[str]:
        """macOS speech recognition"""
        # Fallback to Windows method
        return self._listen_windows(timeout, "en-US")
    
    def _listen_linux(self, timeout: int) -> Optional[str]:
        """Linux speech recognition"""
        return self._listen_windows(timeout, "en-US")
