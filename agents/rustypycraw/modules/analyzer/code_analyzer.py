"""Code Analyzer - Analyzes Python/Rust interop patterns and compatibility"""
import re

class CodeAnalyzer:
    def __init__(self):
        self.py_types_to_rust = {
            "int": "i32",
            "float": "f64", 
            "str": "String",
            "bool": "bool",
            "list": "Vec",
            "dict": "HashMap",
            "None": "Option",
            "tuple": "tuple",
            "bytes": "Vec<u8>",
        }
    
    def analyze(self, path, analysis_type="interop"):
        """Analyze code for interop patterns"""
        from pathlib import Path
        p = Path(path)
        if not p.exists():
            return {"error": f"Path not found: {path}"}
        
        if p.is_file():
            return self._analyze_file(p, analysis_type)
        
        results = []
        for ext in [".py", ".rs"]:
            for f in p.rglob(f"*{ext}"):
                result = self._analyze_file(f, analysis_type)
                if result:
                    results.append(result)
        return {"files_analyzed": len(results), "results": results[:10]}

    def _analyze_file(self, path, analysis_type):
        content = path.read_text(encoding="utf-8", errors="ignore")
        ext = path.suffix
        
        result = {"file": str(path), "language": "python" if ext == ".py" else "rust"}
        
        if analysis_type == "interop" and ext == ".py":
            result["rust_portable"] = self._check_py_rust_compat(content)
            result["type_suggestions"] = self._suggest_rust_types(content)
        elif analysis_type == "interop" and ext == ".rs":
            result["unsafe_patterns"] = self._find_unsafe_patterns(content)
            result["py_binding_potential"] = self._check_pyo3_potential(content)
        elif analysis_type == "complexity":
            result["complexity"] = self._estimate_complexity(content, ext)
        
        return result

    def _check_py_rust_compat(self, content):
        """Check if Python code can be ported to Rust"""
        issues = []
        if "eval(" in content:
            issues.append("eval() not available in Rust - use explicit logic")
        if "exec(" in content:
            issues.append("exec() not available in Rust")
        if "type(" in content and "==" in content:
            issues.append("Dynamic type checking - use Rust enums/traits instead")
        if "hasattr" in content:
            issues.append("hasattr() - use Rust trait bounds")
        if "setattr" in content:
            issues.append("setattr() - use Rust struct methods")
        if "globals()" in content or "locals()" in content:
            issues.append("globals()/locals() - no Rust equivalent")
        return {"portable": len(issues) == 0, "issues": issues} if issues else {"portable": True, "issues": []}

    def _suggest_rust_types(self, content):
        """Suggest Rust types for Python variables"""
        suggestions = []
        for py_type, rs_type in self.py_types_to_rust.items():
            if py_type in content:
                suggestions.append(f"Python '{py_type}' -> Rust '{rs_type}'")
        return suggestions[:10]

    def _find_unsafe_patterns(self, content):
        patterns = []
        if "unsafe {" in content:
            patterns.append("Contains unsafe blocks")
        if ".unwrap()" in content:
            patterns.append("Contains .unwrap() calls - consider proper error handling")
        if "panic!" in content:
            patterns.append("Contains panic! macros")
        if "as " in content and not "as " in ["as_ref", "as_mut", "as_str"]:
            patterns.append("Contains type casting with 'as'")
        return patterns

    def _check_pyo3_potential(self, content):
        """Check if Rust code could be exposed to Python via PyO3"""
        has_pub = "pub fn" in content or "pub struct" in content
        has_pyo3 = "pyo3" in content.lower() or "#[pyfunction]" in content or "#[pymodule]" in content
        return {
            "suitable": has_pub,
            "already_pyo3": has_pyo3,
            "suggestion": "Add #[pyfunction] and #[pymodule] for Python bindings" if has_pub and not has_pyo3 else None
        }

    def _estimate_complexity(self, content, ext):
        lines = content.count("\n") + 1
        if ext == ".py":
            functions = content.count("\ndef ") + content.count("\nasync def ")
            classes = content.count("\nclass ")
        else:
            functions = content.count("fn ")
            classes = content.count("struct ") + content.count("enum ") + content.count("trait ")
        
        score = (functions * 2) + (classes * 3) + (lines / 100)
        if score < 10: level = "simple"
        elif score < 30: level = "moderate"
        elif score < 60: level = "complex"
        else: level = "very complex"
        
        return {"functions": functions, "classes": classes, "lines": lines, "score": round(score, 1), "level": level}

    def find_unnecessary_clones(self, path):
        """Find unnecessary .clone() calls in Rust code"""
        p = Path(path) if isinstance(path, str) else path
        if not p.exists():
            return []
        content = p.read_text(encoding="utf-8", errors="ignore")
        clones = []
        for i, line in enumerate(content.split("\n"), 1):
            if ".clone()" in line:
                clones.append({"line": i, "code": line.strip()})
        return clones
