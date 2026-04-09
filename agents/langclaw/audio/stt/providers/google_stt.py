"""Google STT Provider - Speech recognition"""

from pathlib import Path
from typing import Optional

class GoogleSTTProvider:
    def transcribe(self, audio_file: Path) -> Optional[str]:
        """Transcribe using Google Speech Recognition"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(str(audio_file)) as source:
                audio = recognizer.record(source)
            
            return recognizer.recognize_google(audio)
            
        except ImportError:
            print("   ⚠️ Install: pip install SpeechRecognition")
        except Exception as e:
            print(f"   ⚠️ Recognition: {e}")
        
        return None
