#!/usr/bin/env python3
"""Listen command - Speech to Text"""
import sys
import json

def execute(args):
    """Convert speech to text"""
    text = ""
    
    # Try speech_recognition first
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...", file=sys.stderr)
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing...", file=sys.stderr)
        
        # Try Google (free)
        try:
            text = r.recognize_google(audio)
            return f"🗣️ {text}"
        except:
            pass
        
        # Try Sphinx (offline)
        try:
            text = r.recognize_sphinx(audio)
            return f"🗣️ {text}"
        except:
            pass
            
    except ImportError:
        pass
    except Exception as e:
        return f"❌ Microphone error: {e}"
    
    # Try whisper if available
    if not text:
        try:
            import whisper
            import tempfile
            import sounddevice as sd
            import numpy as np
            import wave
            
            print("🎤 Recording 5 seconds...", file=sys.stderr)
            fs = 16000
            recording = sd.rec(int(5 * fs), samplerate=fs, channels=1)
            sd.wait()
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                with wave.open(f.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(fs)
                    wf.writeframes((recording * 32767).astype(np.int16).tobytes())
                
                model = whisper.load_model("base")
                result = model.transcribe(f.name)
                return f"🗣️ {result['text']}"
                
        except ImportError:
            pass
        except Exception as e:
            return f"❌ Whisper error: {e}"
    
    if not text:
        return "❌ No STT available. Install: pip install speechrecognition pyaudio"
    
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(execute(' '.join(sys.argv[1:])))
    else:
        print(execute(""))
