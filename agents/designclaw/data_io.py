"""DesignClaw Data I/O - Shared memory."""
import json
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
SHARED_DATA = PROJECT_ROOT / "shared" / "shared_data.json"
def read_shared(key=None):
    if not SHARED_DATA.exists(): return {}, None
    try:
        data = json.loads(SHARED_DATA.read_text(encoding="utf-8"))
        return (data.get(key, {}), None) if key else (data, None)
    except: return {}, None
def write_shared(key, value):
    try:
        data = json.loads(SHARED_DATA.read_text(encoding="utf-8")) if SHARED_DATA.exists() else {}
        data[key] = value
        SHARED_DATA.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        return f"[OK] Shared: {key}"
    except: return "[FAIL] Shared write"
