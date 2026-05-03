"""STT Engine - Speech to Text using multiple providers"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

class STTEngine:
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "langclaw_stt"
        self.temp_dir.mkdir(exist_ok=True)
    
    def listen_microphone(self, duration: int = 5) -> Optional[str]:
        """Record from microphone and transcribe"""
        audio_file = self._record_audio(duration)
        if audio_file:
            return self.transcribe_google(audio_file)
        return None
    
    def _record_audio(self, duration: int = 5) -> Optional[Path]:
        """Record audio from microphone"""
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np
            
            print(f"   🎤 Recording for {duration} seconds...")
            
            # Record audio
            sample_rate = 16000
            recording = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=1, 
                              dtype='float32')
            sd.wait()
            
            # Save to file
            audio_file = self.temp_dir / f"recording_{int(np.time())}.wav"
            sf.write(audio_file, recording, sample_rate)
            
            return audio_file
            
        except ImportError:
            print("   ⚠️ sounddevice not installed. Install with: pip install sounddevice soundfile")
            return None
        except Exception as e:
            print(f"   ⚠️ Recording failed: {e}")
            return None
    
    def transcribe_google(self, audio_file: Path) -> Optional[str]:
        """Transcribe using Google Speech Recognition"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(str(audio_file)) as source:
                audio = recognizer.record(source)
            
            text = recognizer.recognize_google(audio)
            return text
            
        except ImportError:
            print("   ⚠️ speech_recognition not installed. Install with: pip install SpeechRecognition")
        except sr.UnknownValueError:
            print("   ⚠️ Could not understand audio")
        except sr.RequestError as e:
            print(f"   ⚠️ Recognition service error: {e}")
        except Exception as e:
            print(f"   ⚠️ Transcription failed: {e}")
        
        return None
    
    def transcribe_whisper(self, audio_file: Path) -> Optional[str]:
        """Transcribe using OpenAI Whisper (local)"""
        try:
            import whisper
            
            print("   🤖 Transcribing with Whisper...")
            model = whisper.load_model("base")
            result = model.transcribe(str(audio_file))
            return result["text"]
            
        except ImportError:
            print("   ⚠️ whisper not installed. Install with: pip install openai-whisper")
        except Exception as e:
            print(f"   ⚠️ Whisper failed: {e}")
        
        return None
    
    def transcribe_vosk(self, audio_file: Path) -> Optional[str]:
        """Transcribe using Vosk (offline)"""
        try:
            import vosk
            import wave
            import json
            
            model_path = Path("str(PROJECT_ROOT)/agents/langclaw/models/vosk-model-small-en-us-0.15")
            
            if not model_path.exists():
                print("   ⚠️ Vosk model not found")
                return None
            
            model = vosk.Model(str(model_path))
            
            wf = wave.open(str(audio_file), "rb")
            rec = vosk.KaldiRecognizer(model, wf.getframerate())
            
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    results.append(result.get("text", ""))
            
            final = json.loads(rec.FinalResult())
            results.append(final.get("text", ""))
            
            return " ".join(results).strip()
            
        except ImportError:
            print("   ⚠️ vosk not installed")
        except Exception as e:
            print(f"   ⚠️ Vosk failed: {e}")
        
        return None
    
    def listen_and_transcribe(self, method: str = "google") -> Optional[str]:
        """Main method - record and transcribe"""
        audio_file = self._record_audio()
        
        if not audio_file:
            return None
        
        if method == "google":
            text = self.transcribe_google(audio_file)
        elif method == "whisper":
            text = self.transcribe_whisper(audio_file)
        elif method == "vosk":
            text = self.transcribe_vosk(audio_file)
        else:
            text = self.transcribe_google(audio_file)
        
        # Cleanup
        if audio_file.exists():
            audio_file.unlink()
        
        return text
