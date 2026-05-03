"""TTS Engine - Text to Speech using multiple providers"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import quote

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TTSEngine:
    def __init__(self):
        self.cache_dir = Path("str(PROJECT_ROOT)/agents/langclaw/tts_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.voices = {
            "es": "es-ES-Standard-A",
            "fr": "fr-FR-Standard-A",
            "de": "de-DE-Standard-A",
            "it": "it-IT-Standard-A",
            "ja": "ja-JP-Standard-A",
            "ko": "ko-KR-Standard-A",
            "zh": "cmn-CN-Standard-A",
            "ru": "ru-RU-Standard-A",
            "pt": "pt-PT-Standard-A",
            "nl": "nl-NL-Standard-A"
        }
    
    def speak_google_tts(self, text: str, lang: str) -> Optional[str]:
        """Use Google Translate TTS (free)"""
        try:
            import requests
            
            # Google TTS URL
            encoded_text = quote(text)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded_text}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Save to cache
                cache_file = self.cache_dir / f"{lang}_{hash(text)}.mp3"
                cache_file.write_bytes(response.content)
                
                # Play audio
                self._play_audio(cache_file)
                return str(cache_file)
        except Exception as e:
            print(f"   ⚠️ Google TTS failed: {e}")
        
        return None
    
    def speak_edge_tts(self, text: str, lang: str) -> Optional[str]:
        """Use Edge TTS (requires edge-tts package)"""
        try:
            import asyncio
            import edge_tts
            
            voice = self.voices.get(lang, f"{lang}-{lang.upper()}-Standard-A")
            cache_file = self.cache_dir / f"edge_{lang}_{hash(text)}.mp3"
            
            async def _speak():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(str(cache_file))
            
            asyncio.run(_speak())
            self._play_audio(cache_file)
            return str(cache_file)
        except ImportError:
            pass
        except Exception as e:
            print(f"   ⚠️ Edge TTS failed: {e}")
        
        return None
    
    def speak_system_tts(self, text: str, lang: str) -> bool:
        """Use Windows built-in TTS"""
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
            return True
        except ImportError:
            pass
        except Exception:
            pass
        
        # Fallback to PowerShell
        try:
            subprocess.run([
                'powershell', '-Command',
                f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text}")'
            ], capture_output=True, timeout=30)
            return True
        except:
            return False
    
    def _play_audio(self, filepath: Path):
        """Play audio file"""
        if sys.platform == "win32":
            os.startfile(str(filepath))
        elif sys.platform == "darwin":
            subprocess.run(["afplay", str(filepath)])
        else:
            subprocess.run(["xdg-open", str(filepath)])
    
    def speak(self, text: str, lang: str = "en") -> bool:
        """Main speak method - tries multiple TTS engines"""
        print(f"   🔊 Speaking: '{text}' in {lang}")
        
        # Try Google TTS first
        result = self.speak_google_tts(text, lang)
        if result:
            print(f"   ✅ TTS via Google")
            return True
        
        # Try Edge TTS
        result = self.speak_edge_tts(text, lang)
        if result:
            print(f"   ✅ TTS via Edge")
            return True
        
        # Fallback to system TTS
        if self.speak_system_tts(text, lang):
            print(f"   ✅ TTS via System")
            return True
        
        print(f"   ❌ All TTS engines failed")
        return False
    
    def list_available_voices(self):
        """List all available Edge TTS voices"""
        try:
            import asyncio
            import edge_tts
            
            async def _list():
                voices = await edge_tts.list_voices()
                return voices
            
            return asyncio.run(_list())
        except:
            return []
