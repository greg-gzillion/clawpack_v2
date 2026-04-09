"""STT Engine - Coordinates speech-to-text"""

from audio.stt.recorder import AudioRecorder
from audio.stt.providers.google_stt import GoogleSTTProvider

class STTEngine:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.google = GoogleSTTProvider()
    
    def listen(self, duration: int = 5) -> str:
        """Listen and transcribe"""
        audio_file = self.recorder.record(duration)
        
        if not audio_file:
            return ""
        
        text = self.google.transcribe(audio_file)
        
        # Cleanup
        if audio_file.exists():
            audio_file.unlink()
        
        return text or ""
