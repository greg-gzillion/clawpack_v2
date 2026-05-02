"""ClawCoder Data I/O - Shared memory and cross-agent delegation"""
import json
from pathlib import Path

AGENT_DIR = Path(__file__).parent
PROJECT_ROOT = AGENT_DIR.parent.parent
SHARED_DATA = PROJECT_ROOT / "shared" / "shared_data.json"
EXPORTS_DIR = AGENT_DIR / "data"

def read_shared(key=None):
    if not SHARED_DATA.exists():
        return {}, None
    try:
        data = json.loads(SHARED_DATA.read_text(encoding="utf-8"))
        if key:
            return data.get(key, {}), None
        return data, None
    except Exception as e:
        return {}, f"Shared read error: {e}"

def write_shared(key, value):
    try:
        data = {}
        if SHARED_DATA.exists():
            data = json.loads(SHARED_DATA.read_text(encoding="utf-8"))
        data[key] = value
        SHARED_DATA.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        return f"[OK] Shared: {key}"
    except Exception as e:
        return f"[FAIL] Shared write: {e}"

def list_exports():
    files = sorted(EXPORTS_DIR.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        return "No exports yet"
    lines = []
    for f in files[:20]:
        lines.append(f"  {f.name} ({f.stat().st_size:,} bytes)")
    return "\n".join(lines)
