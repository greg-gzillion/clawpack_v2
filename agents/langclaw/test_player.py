import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from audio.tts.player import AudioPlayer

test_file = Path("C:/Windows/Media/Windows Notify.wav")
if test_file.exists():
    print("Testing hidden PowerShell MediaPlayer...")
    result = AudioPlayer.play(test_file)
    if result:
        print("✅ Hidden playback successful!")
        print("   (You should have heard a sound)")
    else:
        print("❌ Hidden playback failed")
