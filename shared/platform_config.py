# shared/platform_config.py - Cross-platform compatibility matrix
# Every device that can run Python can run Clawpack.
# This module tells agents what features are available on the current platform.

import os, sys

def get_platform():
    if sys.platform == 'win32': return 'windows'
    elif sys.platform == 'darwin': return 'mac'
    else: return 'linux'

def get_device_type():
    """Detect if running on desktop, phone, tablet, or single-board computer."""
    plat = get_platform()
    # Check for mobile/embedded indicators
    if os.path.exists('/proc/device-tree/model'):
        with open('/proc/device-tree/model') as f:
            model = f.read().lower()
            if 'raspberry' in model: return 'raspberry_pi'
    if os.path.exists('/sys/class/power_supply'):
        return 'laptop_or_mobile'
    if plat == 'linux' and 'ANDROID_DATA' in os.environ:
        return 'android'
    return 'desktop'

# ============================================================
# FEATURE MATRIX: What works on each platform
# ============================================================

FEATURES = {
    'windows': {
        'tts': {'engine': 'pyttsx3', 'voices': 'David (M), Zira (F)', 'quality': 'good', 'offline': True},
        'stt': {'engine': 'speech_recognition + google', 'quality': 'good', 'offline': False},
        'eye_tracking': {'engine': 'Windows Eye Control', 'hardware': 'Tobii 4C/5', 'builtin': True},
        'braille_display': {'support': 'USB HID', 'driver': 'built-in'},
        'neuralink': {'path': 'COM4', 'driver': 'BLE serial via pyserial'},
        'hotkeys': {'module': 'keyboard', 'needs_admin': False},
        'display': {'type': 'terminal', 'colors': True},
    },
    'mac': {
        'tts': {'engine': 'say (built-in)', 'voices': '80+ voices including multilingual', 'quality': 'excellent', 'offline': True},
        'stt': {'engine': 'speech_recognition + google', 'quality': 'good', 'offline': False},
        'eye_tracking': {'engine': 'Head Pointer (built-in)', 'path': 'Accessibility > Pointer Control > Head Pointer', 'builtin': True},
        'braille_display': {'support': 'USB HID', 'driver': 'VoiceOver built-in'},
        'neuralink': {'path': '/dev/tty.Neuralink-N1-SPPDev', 'driver': 'BLE serial via pyserial'},
        'hotkeys': {'module': 'keyboard', 'needs_admin': True},
        'display': {'type': 'terminal', 'colors': True},
    },
    'linux': {
        'tts': {'engine': 'espeak or pyttsx3', 'voices': 'espeak multilingual', 'quality': 'functional', 'offline': True},
        'stt': {'engine': 'speech_recognition + google', 'quality': 'good', 'offline': False},
        'eye_tracking': {'engine': 'eviacam', 'install': 'sudo apt install eviacam', 'builtin': False},
        'braille_display': {'support': 'USB HID', 'driver': 'brltty (sudo apt install brltty)'},
        'neuralink': {'path': '/dev/ttyACM0', 'driver': 'BLE serial via pyserial'},
        'hotkeys': {'module': 'keyboard', 'needs_admin': True},
        'display': {'type': 'terminal', 'colors': True},
    },
    'raspberry_pi': {
        'tts': {'engine': 'espeak', 'voices': 'multilingual', 'quality': 'functional', 'offline': True},
        'stt': {'engine': 'speech_recognition + google', 'quality': 'good', 'offline': False},
        'eye_tracking': {'engine': 'eviacam', 'note': 'limited by CPU'},
        'braille_display': {'support': 'USB HID via brltty'},
        'neuralink': {'path': '/dev/ttyACM0'},
        'hotkeys': {'module': 'keyboard', 'needs_admin': True},
        'display': {'type': 'terminal or HDMI', 'colors': True},
    },
    'android': {
        'tts': {'engine': 'Android TTS via PWA', 'note': 'Use mobile PWA at http://server:8766'},
        'stt': {'engine': 'Web Speech API via PWA', 'note': 'Built into Chrome'},
        'eye_tracking': {'engine': 'Not available on mobile'},
        'braille_display': {'support': 'Bluetooth Braille via Android Accessibility'},
        'neuralink': {'path': 'BLE via Android Neuralink app'},
        'display': {'type': 'PWA browser', 'colors': True},
    },
    'iphone': {
        'tts': {'engine': 'VoiceOver (built-in)', 'quality': 'excellent'},
        'stt': {'engine': 'Siri/dictation (built-in)', 'quality': 'excellent'},
        'eye_tracking': {'engine': 'Not available on mobile'},
        'braille_display': {'support': 'Bluetooth Braille via VoiceOver'},
        'neuralink': {'path': 'BLE via iOS Neuralink app'},
        'display': {'type': 'PWA browser', 'colors': True},
    },
}

# ============================================================
# Auto-detection
# ============================================================

def current_platform():
    plat = get_platform()
    device = get_device_type()
    if device == 'raspberry_pi': return 'raspberry_pi'
    if device == 'android': return 'android'
    return plat

def get_feature(feature_name):
    """Get feature availability for current platform."""
    plat = current_platform()
    return FEATURES.get(plat, FEATURES['linux']).get(feature_name, {})

def get_tts_info():
    return get_feature('tts')

def get_stt_info():
    return get_feature('stt')

def get_eye_tracking_info():
    return get_feature('eye_tracking')

def get_neuralink_info():
    return get_feature('neuralink')

def get_braille_info():
    return get_feature('braille_display')

# ============================================================
# Setup instructions
# ============================================================

def get_setup_guide():
    plat = current_platform()
    info = FEATURES.get(plat, FEATURES['linux'])
    lines = [f'CLAMPACK V2 - {plat.upper()} SETUP', '='*50, '']
    
    tts = info.get('tts', {})
    lines.append(f'TTS: {tts.get("engine", "none")} ({tts.get("quality", "unknown")} quality)')
    lines.append(f'Voices: {tts.get("voices", "check platform settings")}')
    lines.append('')
    
    stt = info.get('stt', {})
    lines.append(f'STT: {stt.get("engine", "none")}')
    lines.append('')
    
    eye = info.get('eye_tracking', {})
    lines.append(f'Eye Tracking: {eye.get("engine", "not available")}')
    if eye.get('install'):
        lines.append(f'Install: {eye["install"]}')
    lines.append('')
    
    braille = info.get('braille_display', {})
    lines.append(f'Braille Display: {braille.get("support", "not available")}')
    if braille.get('driver'):
        lines.append(f'Driver: {braille.get("driver", "")}')
    lines.append('')
    
    neuralink = info.get('neuralink', {})
    lines.append(f'Neuralink: {neuralink.get("path", "not available")}')
    lines.append('')
    
    display = info.get('display', {})
    lines.append(f'Display: {display.get("type", "terminal")}')
    
    return '\n'.join(lines)

def mobile_connect_url():
    """Return the URL for mobile PWA connection."""
    import socket
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return f'http://{ip}:8766'
    except:
        return 'http://127.0.0.1:8766'

# ============================================================
# Quick test
# ============================================================
if __name__ == '__main__':
    print(get_setup_guide())
    print(f'\nMobile PWA URL: {mobile_connect_url()}')
