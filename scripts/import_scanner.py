"""Forbidden Import Scanner - Detects constitutional bypass attempts."""
from pathlib import Path
from typing import List, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_IMPORTS = {
    "subprocess": "Use GuardedExecutor.run_subprocess()",
    "os.system": "Use GuardedExecutor - os.system is BLOCKED",
    "shutil.rmtree": "Use GuardedExecutor.delete_directory()",
    "Path.unlink": "Use GuardedExecutor.delete_file()",
    "shell=True": "Shell execution is PERMANENTLY BLOCKED",
}

EXEMPT = {"shared/llm/", "shared/guarded_executor.py", "shared/execution_policy.py", "scripts/", "_archive/", "__pycache__/"}

def scan_file(filepath: Path) -> List[Dict]:
    violations = []
    try:
        lines = filepath.read_text(encoding='utf-8', errors='ignore').splitlines()
    except:
        return violations
    for i, line in enumerate(lines, 1):
        for pattern, reason in FORBIDDEN_IMPORTS.items():
            if pattern in line and not line.strip().startswith('#'):
                violations.append({"file": str(filepath.relative_to(PROJECT_ROOT)), "line": i, "pattern": pattern, "reason": reason})
    return violations

def scan_all_agents() -> Dict:
    all_v = []
    for py_file in (PROJECT_ROOT / "agents").rglob("*.py"):
        if any(e in str(py_file) for e in EXEMPT): continue
        all_v.extend(scan_file(py_file))
    return {"violations": all_v, "count": len(all_v), "compliant": len(all_v) == 0}

__all__ = ["scan_file", "scan_all_agents"]