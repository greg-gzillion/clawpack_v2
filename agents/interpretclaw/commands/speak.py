#!/usr/bin/env python3
"""Speak command - Text to Speech"""
import sys
import tempfile
import os

def execute(text):
    """Convert text to speech"""
    if not text:
        return "❌ No text to speak"
    
    # Method 1: pyttsx3 (offline, works on Windows/Mac/Linux)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        return f"🔊 Speaking: {text[:50]}..."
    except ImportError:
        pass
    except Exception as e:
        return f"❌ pyttsx3 error: {e}"
    
    # Method 2: Windows built-in SAPI
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
        return f"🔊 Speaking: {text[:50]}..."
    except ImportError:
        pass
    except Exception as e:
        return f"❌ SAPI error: {e}"
    
    # Method 3: gTTS (Google, internet required)
    try:
        from gtts import gTTS
        import playsound
        
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            playsound.playsound(f.name)
            os.unlink(f.name)
        return f"🔊 Speaking: {text[:50]}..."
    except ImportError:
        pass
    except Exception as e:
        return f"❌ gTTS error: {e}"
    
    # Method 4: edge-tts (Microsoft Edge)
    try:
        import asyncio
        import edge_tts
        
        async def speak_edge():
            communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                await communicate.save(f.name)
                if sys.platform == "win32":
                    os.system(f'start /min "" "{f.name}"')
                else:
                    os.system(f'mpg123 "{f.name}" 2>/dev/null &')
                await asyncio.sleep(len(text) * 0.1)
                os.unlink(f.name)
        
        asyncio.run(speak_edge())
        return f"🔊 Speaking: {text[:50]}..."
    except ImportError:
        pass
    except Exception as e:
        return f"❌ edge-tts error: {e}"
    
    return "❌ No TTS available. Install: pip install pyttsx3"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        print(execute(text))
    else:
        print(execute("Hello, this is a test of text to speech"))
