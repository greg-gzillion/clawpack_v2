"""crustyclaw shared utilities — constitutional command helpers."""
import subprocess
from pathlib import Path
from datetime import datetime

CRUSTY_DIR = Path(__file__).resolve().parent.parent
EXPORTS = CRUSTY_DIR.parent.parent / "exports"


def validate_rust(filepath: Path) -> str:
    """Validate Rust code compilation. Returns status message."""
    try:
        result = subprocess.run(
            ["rustc", "--edition", "2024", "--emit=metadata", str(filepath)],
            capture_output=True, text=True, timeout=30
        )
        return "Compilation OK" if result.returncode == 0 else result.stderr[:200]
    except FileNotFoundError:
        return "rustc not installed"
    except Exception as e:
        return str(e)


def extract_code(text: str) -> str:
    """Extract code from markdown blocks or raw text."""
    if "```" in text:
        blocks = text.split("```")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                if "\n" in block:
                    block = block.split("\n", 1)[1]
                return block.strip()
    return text.strip()


def save_rust(code: str, query: str) -> tuple:
    """Save Rust code to exports. Returns (filename, filepath)."""
    name = query.replace(" ", "_").replace("\\", "").replace("/", "")[:50]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"{name}_{ts}.rs"
    EXPORTS.mkdir(exist_ok=True)
    filepath = EXPORTS / fn
    filepath.write_text(code, encoding="utf-8")
    return fn, filepath


def find_crustyclaw_binary() -> Path | None:
    """Find the crustyclaw standalone binary."""
    paths = [
        CRUSTY_DIR / "target" / "release" / "crustyclaw.exe",
        CRUSTY_DIR / "target" / "release" / "crustyclaw",
        Path.home() / ".cargo" / "bin" / "crustyclaw",
    ]
    for p in paths:
        if p.exists():
            return p
    return None


def run_standalone(command: str, args: str = "") -> str | None:
    """Run a standalone crustyclaw command if binary exists."""
    allowed = {"audit", "pinch", "explain", "fix"}
    if command not in allowed:
        return None
    binary = find_crustyclaw_binary()
    if not binary:
        return None
    safe_input = "".join(c for c in str(args) if c.isprintable() and c not in "\r\n\t")[:2000].strip()
    try:
        result = subprocess.run(
            [str(binary), command],
            input=safe_input if safe_input else None,
            capture_output=True, text=True, timeout=30
        )
        return result.stdout or result.stderr
    except Exception:
        return None
