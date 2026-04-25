"""Code Scanner - Scans Python and Rust codebases for structure, imports, and complexity"""
import os
from pathlib import Path

class CodeScanner:
    def __init__(self):
        pass

    def scan(self, path, language=None):
        """Scan a file or directory for code structure"""
        p = Path(path)
        if not p.exists():
            return {"error": f"Path not found: {path}"}
        
        if p.is_file():
            return self._scan_file(p, language)
        
        results = {"files": 0, "lines": 0, "languages": {}}
        for ext in [".py", ".rs"]:
            for f in p.rglob(f"*{ext}"):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    lines = content.count("\n") + 1
                    results["files"] += 1
                    results["lines"] += lines
                    lang = "python" if ext == ".py" else "rust"
                    if lang not in results["languages"]:
                        results["languages"][lang] = {"files": 0, "lines": 0, "functions": 0}
                    results["languages"][lang]["files"] += 1
                    results["languages"][lang]["lines"] += lines
                    # Count functions
                    if lang == "python":
                        results["languages"][lang]["functions"] += content.count("\ndef ")
                        results["languages"][lang]["functions"] += content.count("\nasync def ")
                    elif lang == "rust":
                        results["languages"][lang]["functions"] += content.count("fn ")
                except:
                    pass
        return results

    def _scan_file(self, path, language=None):
        ext = path.suffix
        if ext not in [".py", ".rs"]:
            return {"error": f"Unsupported file type: {ext}"}
        
        content = path.read_text(encoding="utf-8", errors="ignore")
        lang = "python" if ext == ".py" else "rust"
        lines = content.count("\n") + 1
        
        result = {
            "file": str(path),
            "language": lang,
            "lines": lines,
            "size_bytes": path.stat().st_size,
        }
        
        # Extract imports
        if lang == "python":
            imports = []
            for line in content.split("\n"):
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    imports.append(line.strip())
            result["imports"] = imports[:20]
            result["classes"] = content.count("\nclass ")
            result["functions"] = content.count("\ndef ") + content.count("\nasync def ")
        elif lang == "rust":
            imports = []
            for line in content.split("\n"):
                if "use " in line and ";" in line:
                    imports.append(line.strip())
            result["imports"] = imports[:20]
            result["structs"] = content.count("\nstruct ") + content.count("\npub struct ")
            result["functions"] = content.count("fn ")
            result["unsafe_blocks"] = content.count("unsafe {")
        
        return result

    def compare(self, py_path, rs_path):
        """Compare Python and Rust implementations"""
        py = self._scan_file(Path(py_path)) if Path(py_path).exists() else {}
        rs = self._scan_file(Path(rs_path)) if Path(rs_path).exists() else {}
        return {"python": py, "rust": rs}
