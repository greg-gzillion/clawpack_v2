"""A2A Handler for ClawCoder - 39 Languages Full Stack with compiler validation"""
import sys, os, subprocess
from pathlib import Path
from datetime import datetime
from agents.claw_coder.engine.scanner import ProjectScanner

CODER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODER_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CODER_DIR))
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))
from shared.base_agent import BaseAgent
import importlib.util

def _load_mod(name):
    path = CODER_DIR / "commands" / f"{name}.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_run_mod = _load_mod("run")
_test_mod = _load_mod("test")
_translate_mod = _load_mod("translate")

LANG_EXT = {"python":".py","rust":".rs","go":".go","javascript":".js","typescript":".ts","java":".java","c":".c","cpp":".cpp","csharp":".cs","ruby":".rb","php":".php","swift":".swift","kotlin":".kt","scala":".scala","r":".r","julia":".jl","lua":".lua","perl":".pl","haskell":".hs","clojure":".clj","elixir":".ex","erlang":".erl","dart":".dart","bash":".sh","powershell":".ps1","sql":".sql","html":".html","css":".css","yaml":".yaml","json":".json","xml":".xml","assembly":".asm","fortran":".f90","cobol":".cbl","groovy":".groovy","nim":".nim","zig":".zig","matlab":".m","makefile":".mk"}

# Language-specific version/compiler info
LANG_VERSION = {
    "python": "3.12",
    "rust": "2024 edition",
    "go": "1.23",
    "javascript": "ES2024",
    "typescript": "5.5",
    "java": "21",
    "cpp": "C++23",
    "c": "C17",
    "csharp": ".NET 9",
    "kotlin": "2.0",
    "swift": "6.0",
    "zig": "0.13",
}

def _detect_lang(task):
    t = task.lower()
    for lang in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if lang in t: return lang
    return "python"

class ClawCoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("claw_coder")

    def _validate_code(self, filepath, lang):
        """Run compiler/linter on generated code. Returns (passed, output)."""
        try:
            if lang == "python":
                result = subprocess.run(["python", "-m", "py_compile", str(filepath)], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0, result.stderr or "Syntax OK"
            elif lang == "rust":
                # Check if cargo is available
                result = subprocess.run(["rustc", "--edition", "2024", "--emit=metadata", str(filepath)],
                                      capture_output=True, text=True, timeout=30)
                return result.returncode == 0, result.stderr or "Compilation OK"
            elif lang == "go":
                result = subprocess.run(["go", "fmt", str(filepath)],
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0, result.stderr or "Format OK"
            elif lang in ("javascript", "typescript"):
                # Node syntax check
                if lang == "typescript":
                    result = subprocess.run(["npx", "tsc", "--noEmit", str(filepath)],
                                          capture_output=True, text=True, timeout=15)
                else:
                    result = subprocess.run(["node", "--check", str(filepath)],
                                          capture_output=True, text=True, timeout=10)
                return result.returncode == 0, result.stderr or "Syntax OK"
        except FileNotFoundError:
            return None, f"{lang} compiler not installed"
        except Exception as e:
            return None, str(e)
        return None, f"No validator for {lang}"

    def _read_reference_file(self, lang, topic):
        """Read full reference files for the language if they exist."""
        refs_dir = PROJECT_ROOT / "agents" / "webclaw" / "references" / "claw_coder" / lang
        if not refs_dir.exists():
            return ""
        
        ref_text = []
        for md_file in refs_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                # Only include if relevant to topic
                if topic.lower() in content.lower() or md_file.stem.lower() in topic.lower():
                    ref_text.append(f"### {md_file.relative_to(refs_dir)}\n{content[:2000]}")
                    if len(ref_text) >= 3:
                        break
            except:
                pass
        return "\n\n".join(ref_text)

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/code",) and query:
                lang = _detect_lang(query)
                version = LANG_VERSION.get(lang, "latest")
                
                # Read full reference files for this language
                refs = self._read_reference_file(lang, query)
                # Scan project context if --scan flag
                project_ctx = ""
                if "--scan" in query:
                    query = query.replace("--scan", "").strip()
                    scanner = ProjectScanner(PROJECT_ROOT)
                    project_ctx = scanner.full_context(query, lang)
                # Call CrustyClaw for Rust code
                rust_audit = ""
                if lang == "rust":
                    rust_audit = self.call_agent("crustyclaw", f"/audit {query}", timeout=15) or ""
                
                prompt = f"Write clean {lang} {version} code. Return only the code with brief comments.\n\nTask: {query}"
                if refs:
                    prompt = f"Reference material for {lang}:\n{refs[:3000]}\n\n{prompt}"
                if rust_audit:
                    prompt += f"\n\nRust best practices:\n{rust_audit[:1000]}"
                
                result = self.ask_llm(prompt)
                
                # Save and validate
                # Extract code from markdown blocks
                code = result
                if "```" in code:
                    blocks = code.split("```")
                    for i, block in enumerate(blocks):
                        if i % 2 == 1:
                            block = block.split("\n", 1)[1] if "\n" in block else block
                            code = block
                            break
                
                name = query.replace(" ", "_").replace("\\", "").replace("/", "")[:50]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = LANG_EXT.get(lang, ".txt")
                fn = name + "_" + ts + ext
                filepath = EXPORTS / fn
                EXPORTS.mkdir(exist_ok=True)
                filepath.write_text(code, encoding="utf-8")
                
                # Validate
                passed, validation = self._validate_code(filepath, lang)
                if passed:
                    result = f"Saved: {fn} | Validated: {validation}\n\n{result}"
                elif validation:
                    result = f"Saved: {fn} | Validation: {validation}\n\n{result}"
                else:
                    result = f"Saved: {fn} | Could not validate ({lang} compiler not found)\n\n{result}"
                    
            elif cmd in ("/explain",) and query:
                lang = _detect_lang(query)
                refs = self._read_reference_file(lang, query)
                prompt = f"Explain this clearly with code examples: {query}"
                if refs:
                    prompt = f"Reference:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)
                
            elif cmd in ("/debug",) and query:
                lang = _detect_lang(query)
                refs = self._read_reference_file(lang, query)
                prompt = f"Debug and fix this code. Show the corrected version with explanations: {query}"
                if refs:
                    prompt = f"Reference:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)
                
            elif cmd in ("/review",) and query:
                result = self.ask_llm(f"Do a thorough code review. Point out bugs, style issues, performance problems, and improvements: {query}")
                
            elif cmd in ("/tutorial",) and query:
                lang = _detect_lang(query)
                version = LANG_VERSION.get(lang, "latest")
                result = self.ask_llm(f"Create a beginner-friendly {lang} {version} tutorial with code examples: {query}")
                
            elif cmd in ("/run", "run") and query:
                if _run_mod:
                    result = _run_mod.run(query)
                else:
                    result = "Run command not available. Create commands/run.py"
            elif cmd in ("/test", "test") and query:
                if _test_mod:
                    result = _test_mod.run(query)
                else:
                    result = "Test command not available. Create commands/test.py"
            elif cmd in ("/scan", "scan") and query:
                scanner = ProjectScanner(PROJECT_ROOT)
                if query in ("structure", "tree"):
                    result = scanner.scan_structure(max_depth=3)
                elif query.startswith("patterns") or query.startswith("style"):
                    lang = query.split()[-1] if len(query.split()) > 1 else "python"
                    result = scanner.extract_patterns(lang)
                else:
                    lang = _detect_lang(query)
                    result = scanner.full_context(query, lang)   
            elif cmd == "/help":
                result = """ClawCoder - 39 Languages with Compiler Validation
  /code <lang> <task>         - Generate + validate + auto-save
  /translate <from> <to> <file> - Translate code between languages
  /scan structure             - Show project tree
  /scan patterns <lang>      - Extract coding patterns
  /docs <lang> <file>        - Generate documentation
  /project <lang> <fw> <name> - Scaffold project
  /deps <lang> <pkgs>        - Generate dependency file
  /perf <lang> <file>        - Performance analysis
  /run <lang> <file>         - Execute code
  /test <lang> <file>        - Run tests
  /explain /debug /review /tutorial /find
  /help /stats"""
                
            elif cmd == "/stats":
                result = f"ClawCoder | 39 Languages | Compiler Validation | Interactions: {self.state.get('interactions', 0)}"
            
            elif cmd in ("/translate", "translate") and query:
                if _translate_mod:
                    result = _translate_mod.run(query)
                else:
                    result = "Translate command not available."
                
            elif query:
                result = self.ask_llm(query)
            else:
                result = "Type /help for commands. Or just ask a programming question."
                
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = ClawCoderAgent()
def process_task(task, agent=None):
    return _agent.handle(task)