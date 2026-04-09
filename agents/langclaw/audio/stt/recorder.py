"""Audio Recorder - Records from microphone"""

import tempfile
from pathlib import Path
from typing import Optional

class AudioRecorder:
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "langclaw_stt"
        self.temp_dir.mkdir(exist_ok=True)
    
    def record(self, duration: int = 5) -> Optional[Path]:
        """Record audio from microphone"""
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np
            
            print(f"   🎤 Recording {duration}s...")
            
            sample_rate = 16000
            recording = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=1, 
                              dtype='float32')
            sd.wait()
            
            audio_file = self.temp_dir / f"recording_{int(np.__version__)}.wav"
            sf.write(audio_file, recording, sample_rate)
            return audio_file
            
        except ImportError:
            print("   ⚠️ Install: pip install sounddevice soundfile")
        except Exception as e:
            print(f"   ⚠️ Record failed: {e}")
        
        return None
