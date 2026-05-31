# PLATFORM CONTRACT — Clawpack V2
# Version 1.0.0 — Frozen 2026-05-30
# All agents depend on this contract. Do not change return schemas.

## Required Exports

### current_platform() -> str
Returns one of: 'windows', 'mac', 'linux', 'raspberry_pi', 'android', 'ios'
Represents the canonical platform identifier.

### get_feature(feature_name: str) -> dict
Returns a feature dict with guaranteed keys:
  - engine: str (name of the implementation)
  - quality: str ('excellent', 'good', 'functional', 'unavailable')
  - offline: bool (works without internet)
  May include: voices, install, driver, path, hardware, builtin, note

### get_tts_info() -> dict
Schema: { engine: str, voices: str, quality: str, offline: bool }
Guaranteed keys: engine, quality, offline

### get_stt_info() -> dict
Schema: { engine: str, quality: str, offline: bool }
Guaranteed keys: engine, quality, offline

### get_eye_tracking_info() -> dict
Schema: { engine: str, builtin: bool }
Guaranteed keys: engine, builtin
May include: install, hardware, note

### get_neuralink_info() -> dict
Schema: { path: str, driver: str }
Guaranteed keys: path, driver

### get_braille_info() -> dict
Schema: { support: str }
Guaranteed keys: support
May include: driver

### get_setup_guide() -> str
Returns human-readable platform setup instructions.

### mobile_connect_url() -> str
Returns the URL for mobile PWA connection.
Format: http://{ip}:8766

## Agent Usage

`python
from shared.platform_config import get_tts_info, get_eye_tracking_info

tts = get_tts_info()
if tts['offline']:
    # Use local TTS
else:
    # Fall back to cloud TTS

eye = get_eye_tracking_info()
if eye['builtin']:
    # Enable eye tracking UX
else:
    # Show keyboard-only interface
Version History
1.0.0 — Initial contract. May 30, 2026.
