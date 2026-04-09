#!/usr/bin/env python3
"""LANGCLAW - Language Teaching Agent with TTS"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Import TTS
try:
    from tts.tts_engine import TTSEngine
    tts = TTSEngine()
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False
    tts = None

class LangClaw:
    def __init__(self):
        self.commands = {}
        self._load_commands()
        self.mode = "normal"
        self.tts_enabled = TTS_AVAILABLE
    
    def _load_commands(self):
        cmds_path = Path(__file__).parent / "commands"
        for py_file in cmds_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'name') and hasattr(module, 'run'):
                    self.commands[module.name] = module.run
            except Exception as e:
                print(f"Error loading {py_file.name}: {e}")
    
    def run(self):
        print("\n" + "="*60)
        print("🦞 LANGCLAW - Language Teaching Agent".center(60))
        print("="*60)
        print("Learn languages with interactive lessons!".center(60))
        if self.tts_enabled:
            print("🔊 TTS: ENABLED".center(60))
        print("="*60)
        
        print("\n📚 TEACHING COMMANDS:")
        print("  /lesson <lang> <topic>  - Take a lesson")
        print("  /teach <lang>            - Interactive teaching mode")
        print("  /practice <lang> <topic> - Practice exercises")
        print("  /speak <text> in <lang>  - Speak text out loud")
        print("  /tts on/off              - Enable/disable speech")
        print("  /help                    - Show all commands")
        print("  /quit                    - Exit")
        
        print("\n📖 EXAMPLE:")
        print("  /lesson es greetings")
        print("  /speak Hola in es")
        
        while True:
            try:
                cmd = input("\n🦞 Lang > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("¡Adiós! Au revoir! Auf Wiedersehen!")
                    break
                elif cmd == "/help":
                    self._show_help()
                elif cmd == "/tts on":
                    self.tts_enabled = True
                    print("🔊 TTS enabled")
                elif cmd == "/tts off":
                    self.tts_enabled = False
                    print("🔇 TTS disabled")
                elif cmd.startswith("/speak"):
                    if self.tts_enabled and tts:
                        parts = cmd[6:].strip().split(" in ")
                        if len(parts) == 2:
                            text, lang = parts
                            print(f"🔊 Speaking: {text}")
                            tts.speak(text, lang)
                        else:
                            print("Usage: /speak <text> in <lang>")
                    else:
                        print("TTS not available or disabled")
                elif cmd.startswith("/"):
                    parts = cmd[1:].split(maxsplit=1)
                    cmd_name = parts[0]
                    args = parts[1] if len(parts) > 1 else ""
                    
                    if cmd_name in self.commands:
                        result = self.commands[cmd_name](args)
                        print(result)
                        
                        # Auto-speak vocabulary if TTS is on
                        if self.tts_enabled and tts and cmd_name == "vocab" and args:
                            parts = args.split()
                            if len(parts) >= 2:
                                word = parts[1]
                                lang = parts[0]
                                tts.speak(word, lang)
                    else:
                        print(f"Unknown command: /{cmd_name}")
                else:
                    print("Commands start with / (type /help)")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_help(self):
        print("\n📚 Available commands:")
        for name in sorted(self.commands.keys()):
            print(f"  /{name} - {self.commands[name].__doc__ or 'No description'}")
        print("\n🎤 TTS Commands:")
        print("  /speak <text> in <lang> - Speak text out loud")
        print("  /tts on/off - Enable/disable speech")

if __name__ == "__main__":
    LangClaw().run()
