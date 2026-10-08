#!/usr/bin/env python3
"""
run.py - One-command launcher with platform auto-detection.
Starts the A2A server AND launches the clawpack menu automatically.

vs clawpack.py: just the menu (requires a2a_server.py already running).
vs claw.py: launches a single agent directly (bypasses A2A, for quick testing).
vs a2a_server.py: the server only, no menu.

Use run.py when you want everything in one command.
Use the two-terminal approach (a2a_server.py + clawpack.py) for development.
"""
# run.py - Clawpack V2 launcher with platform auto-detection
# Works on Windows, Mac, Linux, Raspberry Pi
# Usage: python run.py

import os, sys, platform

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_platform_info():
    system = platform.system()
    if system == 'Windows': return 'windows'
    elif system == 'Darwin': return 'mac'
    else: return 'linux'

def check_python():
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("Clawpack requires Python 3.10+. You have {}.{}.{}".format(v.major, v.minor, v.micro))
        print("Install from https://python.org")
        sys.exit(1)
    return True

def check_dependencies():
    """Required deps block startup; optional deps only warn."""
    missing = []
    try: import requests
    except ImportError: missing.append('requests')

    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        print("Or: pip install -r requirements.txt")
        return False

    # Optional audio deps — voice/braille commands will be disabled if missing
    optional = []
    try: import pyttsx3
    except ImportError: optional.append('pyttsx3')
    try: import speech_recognition
    except ImportError: optional.append('speech_recognition')
    if optional:
        print(f"Optional packages not installed: {', '.join(optional)}")
        print(f"  Voice/braille features disabled. To enable: pip install {' '.join(optional)}")
        print()

    return True

def print_setup_guide(plat):
    guides = {
        'windows': """
WINDOWS SETUP
============================================
1. Open PowerShell or Command Prompt
2. cd <wherever you cloned clawpack_v2>
3. python run.py
4. The A2A server starts automatically on port 8766
5. Menu appears. Select an agent (1-21).

TTS Voices: David (male), Zira (female) built-in.
More voices: Settings > Time & Language > Speech > Add voices
Eye Tracking: Settings > Accessibility > Eye Control

Firewall: Allow Python on first launch if prompted.
""",
        'mac': """
MAC SETUP
============================================
1. Open Terminal
2. cd ~/dev/clawpack_v2  (or wherever you cloned)
3. python3 run.py
4. The A2A server starts automatically on port 8766
5. Menu appears. Select an agent (1-21).

TTS: Built-in say command (80+ voices).
STT: brew install portaudio first.
Eye Tracking: Accessibility > Pointer Control > Head Pointer

Firewall: Allow Python on first launch if prompted.
""",
        'linux': """
LINUX SETUP
============================================
1. Open Terminal
2. cd ~/dev/clawpack_v2  (or wherever you cloned)
3. python3 run.py
4. The A2A server starts automatically on port 8766
5. Menu appears. Select an agent (1-21).

Dependencies:
  sudo apt install espeak portaudio19-dev python3-pyaudio
  pip install -r requirements.txt

Eye Tracking: sudo apt install eviacam
Braille Display: sudo apt install brltty
Hotkeys: sudo python3 run.py (keyboard module needs root)

Raspberry Pi: Same as Linux. TTS via espeak.
"""
    }
    return guides.get(plat, guides['linux'])

def wait_for_server(timeout=30, poll_interval=1):
    """Poll /health until the server responds or we give up."""
    import requests, time
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get('http://127.0.0.1:8766/health', timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(poll_interval)
    return False

if __name__ == '__main__':
    clear()
    check_python()
    plat = get_platform_info()

    print("""
    CLAWPACK V2 - CONSTITUTIONAL MULTI-AGENT RUNTIME
    """)
    print(print_setup_guide(plat))

    deps_ok = check_dependencies()
    if not deps_ok:
        input("Press Enter after installing required dependencies...")

    print("Starting A2A server on port 8766...")

    # Start server. Inherit stdout/stderr so logs stream to this terminal
    # and the pipe buffer never fills (which would deadlock the server).
    import subprocess
    server_proc = subprocess.Popen(
        [sys.executable, 'a2a_server.py'],
        stdout=None,
        stderr=None,
    )

    # Wait for the server to actually be ready (not a fixed sleep).
    # First-run warm-up includes mem0 + Chronicle + 21 agent registrations.
    print("Waiting for server to become ready...")
    if not wait_for_server(timeout=30):
        print("Server did not respond within 30 seconds. Aborting.")
        server_proc.terminate()
        sys.exit(1)
    print("Server ready.")
    print()

    try:
        # Launch menu in a separate process, inheriting our stdio
        menu_proc = subprocess.Popen(
            [sys.executable, 'clawpack.py'],
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
        menu_proc.wait()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        # Give the server a moment to shut down cleanly.
        # terminate() is abrupt on Windows, but the resulting Qdrant
        # warning on exit is harmless.
        print("Stopping server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Server did not stop in 5s; killing.")
            server_proc.kill()
        print("Server stopped.")

