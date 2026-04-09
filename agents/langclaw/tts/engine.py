"""TTS Engine - Coordinates TTS providers"""

from pathlib import Path
from audio.tts.providers.google_tts import GoogleTTSProvider
from audio.tts.providers.system_tts import SystemTTSProvider
from audio.tts.player import AudioPlayer

class TTSEngine:
    def __init__(self):
        self.cache_dir = Path("C:/Users/greg/dev/clawpack_v2/agents/langclaw/tts_cache")
        self.google = GoogleTTSProvider(self.cache_dir)
        self.system = SystemTTSProvider()
        self.player = AudioPlayer()
    
    def speak(self, text: str, lang: str = "en") -> bool:
        """Speak text - tries providers in order"""
        print(f"   🔊 Speaking: '{text}'")
        
        # Try Google TTS first (generates MP3)
        audio_file = self.google.speak(text, lang)
        if audio_file:
            print(f"   ✅ Audio generated")
            if self.player.play(audio_file):
                print(f"   ✅ Playing (background)")
                return True
        
        # Try system TTS (direct speech)
        print(f"   🔄 Trying system speech...")
        if self.system.speak(text, lang):
            print(f"   ✅ System speech")
            return True
        
        print(f"   ❌ TTS failed")
        return False
