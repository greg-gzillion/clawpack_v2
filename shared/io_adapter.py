# shared/io_adapter.py - Universal Input/Output adapter
import sys, threading, time, os

def input_microphone(timeout=5):
    try:
        from shared.accessibility import listen
        return listen(timeout=timeout)
    except Exception as e:
        return f"[MIC ERROR] {str(e)[:100]}"

def input_keyboard(prompt=""):
    return input(prompt) if prompt else input()

def input_neuralink(device_path=None):
    try:
        device = device_path or os.environ.get("NEURALINK_DEVICE", "")
        if not device:
            return "[NEURALINK] Not configured. Set NEURALINK_DEVICE in .env"
        import serial
        with serial.Serial(device, 115200, timeout=1) as ser:
            data = ser.readline().decode("utf-8", errors="ignore").strip()
            return f"[NEURALINK] {data}"
    except ImportError:
        return "[NEURALINK] pyserial not installed. Run: pip install pyserial"
    except Exception as e:
        return f"[NEURALINK] {str(e)[:100]}"

def input_eye_tracker():
    return input("[EYE TRACKER] Dwell-select or type: ")

def output_speech(text, lang="en"):
    try:
        from shared.accessibility import speak
        return speak(text, lang)
    except Exception as e:
        return f"[TTS ERROR] {str(e)[:100]}"

def output_display(text):
    print(text)
    return text

def output_braille(text):
    try:
        from shared.accessibility import to_braille
        braille = to_braille(text)
        print(braille)
        return braille
    except Exception as e:
        return f"[BRAILLE ERROR] {str(e)[:100]}"

def output_neuralink(text):
    try:
        device = os.environ.get("NEURALINK_DEVICE", "")
        if not device:
            return "[NEURALINK OUTPUT] Not configured."
        import serial
        with serial.Serial(device, 115200, timeout=1) as ser:
            ser.write(f"DISPLAY:{text[:500]}\n".encode())
        return f"[NEURALINK] Sent: {text[:100]}..."
    except Exception as e:
        return f"[NEURALINK OUTPUT] {str(e)[:100]}"

def output_haptic(text):
    print(f"[HAPTIC] Alert: {text[:80]}...")
    return text

def get_input(method="auto"):
    if method == "auto":
        try:
            import speech_recognition
            return input_microphone()
        except:
            return input_keyboard()
    methods = {"mic": input_microphone, "keyboard": input_keyboard, "neuralink": input_neuralink, "eye": input_eye_tracker}
    return methods.get(method, input_keyboard)()

def send_output(text, methods=None):
    if methods is None:
        methods = ["display", "speech"]
    outputs = {"display": output_display, "speech": output_speech, "braille": output_braille, "neuralink": output_neuralink, "haptic": output_haptic}
    for method in methods:
        if method in outputs:
            try:
                outputs[method](text)
            except:
                pass
    return text

def configure_neuralink(device_path):
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("NEURALINK_DEVICE="):
            lines[i] = f"NEURALINK_DEVICE={device_path}\n"
            found = True
            break
    if not found:
        lines.append(f"\nNEURALINK_DEVICE={device_path}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)
    return f"[NEURALINK] Configured: {device_path}"

print("shared/io_adapter.py created")
