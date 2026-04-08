"""Text-to-Speech command for EagleClaw"""

import subprocess
import sys
import os
from pathlib import Path

# Try to import available TTS libraries
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

def speak_command(text):
    """Convert text to speech"""
    if not text:
        print("Usage: /speak 'Hello, this is Clawpack'")
        print("   or: /speak [--voice male/female] 'text'")
        return
    
    # Parse options
    voice = "female"  # default
    if text.startswith("--voice"):
        parts = text.split(" ", 2)
        if len(parts) >= 3:
            voice = parts[1].lower()
            text = parts[2]
    
    print(f"\n🔊 Speaking: {text[:100]}...")
    
    # Try available TTS engines in order of preference
    if EDGE_TTS_AVAILABLE:
        _speak_edge(text, voice)
    elif GTTS_AVAILABLE:
        _speak_gtts(text)
    elif PYTTSX3_AVAILABLE:
        _speak_pyttsx3(text)
    else:
        print("❌ No TTS engine available. Install one:")
        print("   pip install edge-tts    (free, high quality)")
        print("   pip install gtts        (free, Google TTS)")
        print("   pip install pyttsx3     (offline, basic)")
        return
    
    print("✅ Speaking complete")

def _speak_edge(text, voice="female"):
    """Use Microsoft Edge TTS (free, high quality)"""
    import asyncio
    
    voices = {
        "male": "en-US-ChristopherNeural",
        "female": "en-US-JennyNeural",
        "british": "en-GB-SoniaNeural",
        "australian": "en-AU-NatashaNeural"
    }
    
    voice_id = voices.get(voice, voices["female"])
    
    async def speak():
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save("temp_speech.mp3")
        # Play the audio
        if sys.platform == "win32":
            os.system("start temp_speech.mp3")
        elif sys.platform == "darwin":
            os.system("afplay temp_speech.mp3")
        else:
            os.system("mpg123 temp_speech.mp3 2>/dev/null")
    
    asyncio.run(speak())

def _speak_gtts(text):
    """Use Google TTS"""
    from gtts import gTLS
    import pygame
    
    tts = gTTS(text=text, lang='en')
    tts.save("temp_speech.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("temp_speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def _speak_pyttsx3(text):
    """Use offline pyttsx3"""
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def list_voices_command(args=None):
    """List available voices"""
    if EDGE_TTS_AVAILABLE:
        print("\n🎤 Available Edge TTS voices:")
        print("  /speak --voice male 'text'      - Male voice")
        print("  /speak --voice female 'text'    - Female voice")
        print("  /speak --voice british 'text'   - British accent")
        print("  /speak --voice australian 'text' - Australian accent")
    else:
        print("\n⚠️ Install edge-tts for best voice quality:")
        print("   pip install edge-tts")