"""PlotClaw Data I/O - CSV, JSON, shared/data integration"""
import csv
import json
from pathlib import Path
from io import StringIO

AGENT_DIR = Path(__file__).parent
PROJECT_ROOT = AGENT_DIR.parent.parent
SHARED_DATA = PROJECT_ROOT / "shared" / "shared_data.json"
DATA_DIR = AGENT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def read_csv(filepath, col=None):
    """Read CSV file, optionally extract a column. Returns (headers, rows, column_data)."""
    path = Path(filepath)
    if not path.exists():
        # Try data dir
        path = DATA_DIR / filepath
    if not path.exists():
        # Try shared exports
        path = PROJECT_ROOT / "exports" / filepath
    if not path.exists():
        return None, None, f"File not found: {filepath}"
    
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        reader = csv.reader(StringIO(text))
        rows = list(reader)
        if not rows:
            return None, None, "Empty CSV"
        
        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []
        
        if col:
            # Extract specific column by name or index
            if col in headers:
                idx = headers.index(col)
                col_data = [float(row[idx]) for row in data_rows if idx < len(row) and row[idx].strip()]
            else:
                try:
                    idx = int(col)
                    col_data = [float(row[idx]) for row in data_rows if idx < len(row) and row[idx].strip()]
                except:
                    return headers, data_rows, f"Column not found: {col}"
            return headers, data_rows, col_data
        
        return headers, data_rows, None
    except Exception as e:
        return None, None, f"CSV error: {e}"

def read_json(filepath, key=None):
    """Read JSON file, optionally extract a key."""
    path = Path(filepath)
    if not path.exists():
        path = DATA_DIR / filepath
    if not path.exists():
        path = PROJECT_ROOT / "exports" / filepath
    if not path.exists():
        return None, f"File not found: {filepath}"
    
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if key:
            return data.get(key, f"Key not found: {key}"), None
        return data, None
    except Exception as e:
        return None, f"JSON error: {e}"

def read_shared(key=None):
    """Read data written by other agents to shared/shared_data.json"""
    if not SHARED_DATA.exists():
        return {}, None
    try:
        data = json.loads(SHARED_DATA.read_text(encoding="utf-8"))
        if key:
            return data.get(key, {}), None
        return data, None
    except Exception as e:
        return {}, f"Shared data error: {e}"

def write_shared(key, value):
    """Write chart data/results for other agents to consume"""
    try:
        data = {}
        if SHARED_DATA.exists():
            data = json.loads(SHARED_DATA.read_text(encoding="utf-8"))
        data[key] = value
        SHARED_DATA.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        return f"[OK] Shared: {key}"
    except Exception as e:
        return f"[FAIL] Shared write: {e}"

def list_data_dir():
    """List available data files"""
    files = []
    for d in [DATA_DIR, PROJECT_ROOT / "exports"]:
        if d.exists():
            for f in d.iterdir():
                if f.suffix in ['.csv', '.json', '.txt']:
                    files.append(str(f.relative_to(PROJECT_ROOT)))
    return files if files else ["No data files found"]
