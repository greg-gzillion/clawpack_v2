# shared/accessibility_eye_tracker.py - Eye tracking integration
# Requires: Windows Eye Control (Settings > Accessibility > Eye Control)
# Tobii Eye Tracker 4C/5 or compatible

def is_available():
    import os
    return os.sys.platform == 'win32'

def get_input(prompt=""):
    if is_available():
        print(f"[EYE TRACKING] {prompt}Dwell-select characters using eye gaze...")
        return input()
    return input(prompt)

def calibrate():
    return "Eye Tracker Setup:\n1. Windows Settings > Accessibility > Eye Control\n2. Turn on Eye Control\n3. Follow calibration dot with eyes\n4. Dwell-select keyboard appears\n5. Use /access eye on to enable"
