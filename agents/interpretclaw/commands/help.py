"""Help command"""
name = "/help"

def run(args):
    print("\n" + "="*60)
    print("🌐 INTERPRETCLAW COMMANDS")
    print("="*60)
    print("  /languages      - List all 39 supported languages")
    print("  /translate <lang> <text> - Translate text")
    print("  /detect <text>  - Detect language")
    print("  /speak <text>   - Text-to-speech")
    print("  /listen         - Speech-to-text (microphone)")
    print("  /help           - This menu")
    print("  /quit           - Exit")
    print("="*60)
    print("\n💡 Example: /translate es Hello world")
    print("   Example: /detect Bonjour le monde")
    print("   Example: /speak Good morning")
    print("   Example: /listen (then speak into microphone)")
