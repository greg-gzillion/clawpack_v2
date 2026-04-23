"""Cargo operations"""
import sys, subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run(args):
    if not args:
        return "Usage: /cargo <command>\nExample: /cargo build"
    
    try:
        result = subprocess.run(
            ["cargo"] + args.split(),
            capture_output=True, text=True, timeout=60,
            cwd=str(Path.home() / "dev")
        )
        return result.stdout or result.stderr or "Cargo completed"
    except Exception as e:
        return f"Cargo error: {e}"
