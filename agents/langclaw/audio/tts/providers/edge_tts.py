"""Edge TTS Provider - Better quality using Microsoft Edge"""

import asyncio
from pathlib import Path
from typing import Optional

class EdgeTTSProvider:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.voices = {
            "es": "es-ES-AlvaroNeural", "fr": "fr-FR-HenriNeural",
            "de": "de-DE-ConradNeural", "it": "it-IT-DiegoNeural",
            "ja": "ja-JP-KeitaNeural", "ko": "ko-KR-InJoonNeural",
            "zh": "zh-CN-XiaoxiaoNeural", "ru": "ru-RU-DmitryNeural",
            "pt": "pt-PT-DuarteNeural", "nl": "nl-NL-MaartenNeural"
        }
    
    def speak(self, text: str, lang: str) -> Optional[Path]:
        """Generate speech using Edge TTS"""
        try:
            import edge_tts
            
            voice = self.voices.get(lang, f"{lang}-{lang.upper()}-Neural")
            cache_file = self.cache_dir / f"edge_{lang}_{hash(text)}.mp3"
            
            async def _speak():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(str(cache_file))
            
            asyncio.run(_speak())
            return cache_file
            
        except ImportError:
            pass
        except Exception as e:
            print(f"   ⚠️ Edge TTS: {e}")
        
        return None
