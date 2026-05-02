"""Code Generator Engine - Extracted from agent_handler.

Handles: code generation, self-repair loop, compiler validation, file saving.
Does NOT handle: A2A routing, shared memory, delegation (that's the handler's job).
"""
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
EXPORTS = PROJECT_ROOT / "exports"

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

def _detect_lang(task):
    t = task.lower()
    for lang in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if lang in t: return lang
    return "python"

def _extract_code(text):
    code = text
    if "`" in code:
        blocks = code.split("`")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                block = block.split("\n", 1)[1] if "\n" in block else block
                code = block
                break
    return code

def _validate_code(filepath, lang):
    """Run compiler/linter. Returns (passed: bool, output: str)."""
    try:
        if lang == "python":
            result = subprocess.run(["python","-m","py_compile",str(filepath)],
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr or "Syntax OK"
        elif lang == "rust":
            result = subprocess.run(["rustc","--edition","2024","--emit=metadata",str(filepath)],
                                  capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stderr or "Compilation OK"
        elif lang == "go":
            result = subprocess.run(["go","fmt",str(filepath)],
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr or "Format OK"
        elif lang in ("javascript","typescript"):
            if lang == "typescript":
                result = subprocess.run(["npx","tsc","--noEmit",str(filepath)],
                                      capture_output=True, text=True, timeout=15)
            else:
                result = subprocess.run(["node","--check",str(filepath)],
                                      capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr or "Syntax OK"
    except FileNotFoundError:
        return None, f"{lang} compiler not installed"
    except Exception as e:
        return None, str(e)
    return None, f"No validator for {lang}"

class CodeGenerator:
    """Generates code with optional self-repair loop.
    
    Usage:
        gen = CodeGenerator(llm_callable)
        result = gen.generate("python", "async web scraper")
    """
    
    def __init__(self, llm_callable):
        """llm_callable: function(prompt) -> str that calls the LLM"""
        self.llm = llm_callable
        self.max_repair_attempts = 3
    
    def generate(self, language: str, query: str, context: str = "", validate: bool = True, save: bool = True) -> dict:
        """Generate code with optional self-repair.
        
        Returns: {
            "code": str,
            "language": str,
            "filepath": str or None,
            "validated": bool or None,
            "validation_output": str,
            "attempts": int,
            "repaired": bool
        }
        """
        lang = language or _detect_lang(query)
        version = LANG_VERSION.get(lang, "latest")
        
        prompt = f"Write clean {lang} {version} code. Return only the code with brief comments.\n\nTask: {query}"
        if context:
            prompt = f"Reference:\n{context[:3000]}\n\n{prompt}"
        
        result = self.llm(prompt)
        code = _extract_code(result)
        attempts = 1
        repaired = False
        
        # Self-repair loop
        if validate:
            for attempt in range(self.max_repair_attempts):
                passed, validation = self._validate_snippet(code, lang)
                if passed:
                    break
                if attempt < self.max_repair_attempts - 1:
                    repair_prompt = f"Fix this {lang} code. Compiler error:\n{validation}\n\nCode:\n{code}\n\nReturn ONLY the corrected code:"
                    code = _extract_code(self.llm(repair_prompt))
                    attempts += 1
                    repaired = True
        else:
            passed, validation = None, "Validation skipped"
        
        # Save
        filepath = None
        if save:
            name = query.replace(" ","_").replace(chr(92),"").replace("/","")[:50]
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = LANG_EXT.get(lang, ".txt")
            fn = f"{name}_{ts}{ext}"
            filepath = EXPORTS / fn
            EXPORTS.mkdir(exist_ok=True)
            filepath.write_text(code, encoding="utf-8")
            
            # Re-validate saved file if we haven't yet
            if not validate:
                passed, validation = _validate_code(filepath, lang)
        
        return {
            "code": code,
            "language": lang,
            "filepath": str(filepath) if filepath else None,
            "filename": fn if filepath else None,
            "validated": passed,
            "validation_output": validation if 'validation' in dir() else "",
            "attempts": attempts,
            "repaired": repaired,
            "raw_response": result
        }
    
    def _validate_snippet(self, code, lang):
        """Validate a code snippet by writing to temp file."""
        import tempfile
        ext = LANG_EXT.get(lang, ".txt")
        with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp_path = f.name
        passed, output = _validate_code(Path(tmp_path), lang)
        Path(tmp_path).unlink(missing_ok=True)
        return passed, output
