"""Langclaw CLI Interface"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.agent import LangclawAgent
from audio.tts.engine import TTSEngine
from audio.stt.engine import STTEngine

LANGUAGE_NAMES = {
    "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
    "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese",
    "ru": "Russian", "ar": "Arabic", "hi": "Hindi", "vi": "Vietnamese",
    "th": "Thai", "tr": "Turkish", "nl": "Dutch", "en": "English"
}

class LangclawCLI:
    def __init__(self):
        self.agent = LangclawAgent()
        self.tts = TTSEngine()
        self.stt = STTEngine()
    
    def run(self):
        self._show_header()
        while True:
            try:
                cmd = input("\n🌐 Lang > ").strip()
                if not cmd:
                    continue
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/clear":
                    os.system('cls')
                    self._show_header()
                elif cmd == "/help":
                    self._show_help()
                elif cmd == "/languages":
                    self._show_languages()
                elif cmd == "/stats":
                    self._show_stats()
                elif cmd.startswith("/resources"):
                    self._show_resources(cmd[10:].strip())
                elif cmd.startswith("/speak"):
                    self._speak(cmd[6:].strip())
                elif cmd.startswith("/listen"):
                    self._listen()
                elif cmd.startswith("/translate"):
                    self._translate(cmd[10:].strip())
                else:
                    print("Unknown command. Type /help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_header(self):
        print("\n" + "="*70)
        print("LANGCLAW - Language Translation Agent".center(70))
        print("="*70)
        self._show_help()
    
    def _show_help(self):
        print("""
🌐 /translate <text> to <lang>  - Translate
🎤 /speak <text> in <lang>      - Text to speech
🎙️ /listen                      - Speech to text
📚 /resources <lang>            - Online resources
📊 /stats                       - Statistics
🌍 /languages                   - List languages

EXAMPLES:
  /translate Hello to es
  /speak Hola in es
  /listen
""")
    
    def _show_languages(self):
        langs = self.agent.get_available_languages()
        print(f"\n📚 Available languages ({len(langs)}):")
        for code in sorted(langs)[:20]:
            if code in LANGUAGE_NAMES:
                print(f"   {code}: {LANGUAGE_NAMES[code]}")
    
    def _show_stats(self):
        stats = self.agent.get_stats()
        print(f"\n📊 Queries: {stats['queries']}")
    
    def _show_resources(self, arg):
        if arg:
            print(self.agent.get_resources(arg.strip().lower()))
        else:
            print("Usage: /resources <lang>")
    
    def _speak(self, arg):
        if " in " in arg:
            parts = arg.split(" in ", 1)
            text, lang = parts[0].strip(), parts[1].strip().lower()
        else:
            text, lang = arg.strip(), "en"
        
        if text:
            self.tts.speak(text, lang)
        else:
            print("Usage: /speak <text> in <lang>")
    
    def _listen(self):
        print("\n🎤 Listening... (5 seconds)")
        text = self.stt.listen()
        if text:
            print(f'\n📝 "{text}"')
        else:
            print("\n❌ Could not transcribe")
    
    def _translate(self, arg):
        if " to " in arg:
            parts = arg.split(" to ", 1)
            text, target = parts[0].strip(), parts[1].strip().lower()
            print(f"\n🔄 '{text}' → {LANGUAGE_NAMES.get(target, target)}")
            print(self.agent.translate(text, target))
        else:
            print("Usage: /translate <text> to <lang>")
