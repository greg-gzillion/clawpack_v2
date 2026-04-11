def run(args):
    """Speech-to-text using microphone"""
    import sys
    import speech_recognition as sr
    
    try:
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        
        with sr.Microphone() as source:
            # Print to stderr so it shows in terminal
            print("🎤 Adjusting for noise...", file=sys.stderr)
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening... speak now", file=sys.stderr)
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("🎤 Processing...", file=sys.stderr)
        
        text = recognizer.recognize_google(audio)
        # Return the result (this goes to stdout)
        return f"📝 You said: {text}"
        
    except sr.WaitTimeoutError:
        return "❌ No speech detected"
    except sr.UnknownValueError:
        return "❌ Could not understand audio"
    except sr.RequestError as e:
        return f"❌ Recognition error: {e}"
    except Exception as e:
        return f"❌ Error: {e}"
