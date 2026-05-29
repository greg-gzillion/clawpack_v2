"""claw_coder shared utilities — constitutional command helpers.

Import in any claw_coder command:
    from agents.claw_coder.commands._helpers import (
        get_lang_info, format_code_block, validate_syntax, save_code
    )
"""
import subprocess
from pathlib import Path
from datetime import datetime

CODER_DIR = Path(__file__).resolve().parent.parent
EXPORTS = CODER_DIR.parent.parent / "exports"

LANG_EXT = {
    "python":".py","rust":".rs","go":".go","javascript":".js","typescript":".ts",
    "java":".java","c":".c","cpp":".cpp","csharp":".cs","ruby":".rb","php":".php",
    "swift":".swift","kotlin":".kt","scala":".scala","r":".r","julia":".jl",
    "lua":".lua","perl":".pl","haskell":".hs","clojure":".clj","elixir":".ex",
    "erlang":".erl","dart":".dart","bash":".sh","powershell":".ps1","sql":".sql",
    "html":".html","css":".css","yaml":".yaml","json":".json","xml":".xml",
    "assembly":".asm","fortran":".f90","cobol":".cbl","groovy":".groovy",
    "nim":".nim","zig":".zig","matlab":".m","makefile":".mk"
}

LANG_VERSION = {
    "python":"3.12","rust":"2024 edition","go":"1.23","javascript":"ES2024",
    "typescript":"5.5","java":"21","cpp":"C++23","c":"C17","csharp":".NET 9",
    "kotlin":"2.0","swift":"6.0","zig":"0.13"
}


def get_lang_info(task: str) -> tuple:
    """Detect language and version from task description."""
    t = task.lower()
    lang = "python"
    for name in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if name in t:
            lang = name
            break
    version = LANG_VERSION.get(lang, "latest")
    ext = LANG_EXT.get(lang, ".txt")
    return lang, version, ext


def format_code_block(code: str, lang: str = "") -> str:
    """Format code as a markdown code block."""
    return f"```{lang}\n{code}\n```"


def extract_code(text: str) -> str:
    """Extract code from markdown code blocks or raw text."""
    if "```" in text:
        blocks = text.split("```")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                # Remove language tag if present
                if "\n" in block:
                    block = block.split("\n", 1)[1]
                return block.strip()
    return text.strip()


def save_code(code: str, lang: str, query: str) -> tuple:
    """Save code to exports directory. Returns (filename, filepath)."""
    ext = LANG_EXT.get(lang, ".txt")
    name = query.replace(" ", "_").replace("\\", "").replace("/", "")[:50]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"{name}_{ts}{ext}"
    EXPORTS.mkdir(exist_ok=True)
    filepath = EXPORTS / fn
    filepath.write_text(code, encoding="utf-8")
    return fn, filepath


def validate_syntax(filepath: Path, lang: str) -> tuple:
    """Validate code syntax. Returns (passed: bool, message: str)."""
    try:
        if lang == "python":
            result = subprocess.run(
                ["python", "-m", "py_compile", str(filepath)],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, result.stderr or "Syntax OK"
        elif lang == "rust":
            result = subprocess.run(
                ["rustc", "--edition", "2024", "--emit=metadata", str(filepath)],
                capture_output=True, text=True, timeout=30
            )
            return result.returncode == 0, result.stderr or "Compilation OK"
        elif lang == "go":
            result = subprocess.run(
                ["go", "fmt", str(filepath)],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0, result.stderr or "Format OK"
        elif lang in ("javascript", "typescript"):
            if lang == "typescript":
                result = subprocess.run(
                    ["npx", "tsc", "--noEmit", str(filepath)],
                    capture_output=True, text=True, timeout=15
                )
            else:
                result = subprocess.run(
                    ["node", "--check", str(filepath)],
                    capture_output=True, text=True, timeout=10
                )
            return result.returncode == 0, result.stderr or "Syntax OK"
    except FileNotFoundError:
        return None, f"{lang} compiler not installed"
    except Exception as e:
        return None, str(e)
    return None, f"No validator for {lang}"
