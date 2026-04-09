import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from audio.tts.player import AudioPlayer

# Test with a simple beep or existing audio file
test_file = Path("C:/Windows/Media/Windows Notify.wav")
if test_file.exists():
    print(f"Testing playback with: {test_file}")
    AudioPlayer.play_simple(test_file)
    print("✅ Playback test complete")
else:
    print("Test audio file not found, but player is ready")
