"""Text-to-Speech output"""
name = "/speak"

def run(args):
    if not args:
        print("Usage: /speak <text>")
        print("Example: /speak Hello world")
        return
    
    print(f"\n🔊 Speaking: {args}")
    
    import subprocess
    try:
        subprocess.run(['powershell', '-Command', 
                       f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{args}")'],
                      capture_output=True, timeout=10)
        print("   ✅ TTS complete")
    except Exception as e:
        print(f"   ⚠️ TTS error: {e}")
