"""Speech-to-Text - Listen from microphone"""
name = "/listen"

def run(args):
    print("\n🎤 Listening... (speak now)")
    print("   Press Ctrl+C to stop listening")
    
    try:
        import speech_recognition as sr
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Use microphone as source
        with sr.Microphone() as source:
            print("   Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("   Listening...")
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("   Processing...")
            
            # Try to recognize speech
            try:
                text = recognizer.recognize_google(audio)
                print(f"\n📝 You said: {text}")
                print("\n💡 Use /translate to convert this to another language")
                
            except sr.UnknownValueError:
                print("\n   ❌ Could not understand audio")
            except sr.RequestError as e:
                print(f"\n   ❌ Recognition error: {e}")
                
    except ImportError:
        print("\n   ❌ SpeechRecognition not installed")
        print("   Install: pip install SpeechRecognition pyaudio")
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        print("   Make sure you have a microphone connected")
