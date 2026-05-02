"""A2A Handler for ClawCoder v5 - Constitutional contract + 39 languages + cross-agent delegation"""
import sys, os, json, subprocess
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
from agents.claw_coder.engine.code_generator import CodeGenerator, _detect_lang, LANG_EXT, LANG_VERSION, _extract_code
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

LANG_VERSION = {"python":"3.12","rust":"2024 edition","go":"1.23","javascript":"ES2024","typescript":"5.5","java":"21","cpp":"C++23","c":"C17","csharp":".NET 9","kotlin":"2.0","swift":"6.0","zig":"0.13"}

def _detect_lang(task):
    t = task.lower()
    for lang in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if lang in t: return lang
    return "python"

class ClawCoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("claw_coder")
        self.code_gen = CodeGenerator(lambda p: self.ask_llm(f"[CODE_GEN] {p}"))

    def _enrich_context(self, query, lang):
        """Gather WebClaw + DataClaw context for code generation."""
        parts = []
        try:
            web = self.call_agent("webclaw", f"search {lang} {query} code example", timeout=8)
            if web: parts.append(str(web)[:1000])
        except: pass
        try:
            data = self.call_agent("dataclaw", f"search {lang} {query}", timeout=8)
            if data: parts.append(str(data)[:1000])
        except: pass
        return "\n".join(parts) if parts else ""

    def _validate_code(self, filepath, lang):
        try:
            if lang == "python":
                result = subprocess.run(["python","-m","py_compile",str(filepath)], capture_output=True, text=True, timeout=10)
                return result.returncode==0, result.stderr or "Syntax OK"
            elif lang == "rust":
                result = subprocess.run(["rustc","--edition","2024","--emit=metadata",str(filepath)], capture_output=True, text=True, timeout=30)
                return result.returncode==0, result.stderr or "Compilation OK"
            elif lang == "go":
                result = subprocess.run(["go","fmt",str(filepath)], capture_output=True, text=True, timeout=10)
                return result.returncode==0, result.stderr or "Format OK"
            elif lang in ("javascript","typescript"):
                if lang=="typescript":
                    result = subprocess.run(["npx","tsc","--noEmit",str(filepath)], capture_output=True, text=True, timeout=15)
                else:
                    result = subprocess.run(["node","--check",str(filepath)], capture_output=True, text=True, timeout=10)
                return result.returncode==0, result.stderr or "Syntax OK"
        except FileNotFoundError:
            return None, f"{lang} compiler not installed"
        except Exception as e:
            return None, str(e)
        return None, f"No validator for {lang}"

    def _read_reference_file(self, lang, topic):
        refs_dir = PROJECT_ROOT / "agents" / "webclaw" / "references" / "claw_coder" / lang
        if not refs_dir.exists():
            return ""
        ref_text = []
        for md_file in refs_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                if topic.lower() in content.lower() or md_file.stem.lower() in topic.lower():
                    ref_text.append(f"### {md_file.relative_to(refs_dir)}\n{content[:2000]}")
                    if len(ref_text)>=3: break
            except: pass
        return "\n\n".join(ref_text)

    def _extract_code(self, text):
        code = text
        if "`" in code:
            blocks = code.split("`")
            for i, block in enumerate(blocks):
                if i%2==1:
                    block = block.split("\n",1)[1] if "\n" in block else block
                    code = block
                    break
        return code

    def handle(self, task):
        self.track_interaction()

        # Dict payload (agent-to-agent)
        if isinstance(task, dict):
            from agents.claw_coder.schema import validate
            validated = validate(task)
            if not validated["valid"]:
                return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        # String (CLI)
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            # Instant commands (no LLM)
            if cmd in ("/help",):
                result = "ClawCoder v5 - 39 Languages\n  /code <task>  /explain /debug /review /tutorial\n  /translate <from> <to> <file>  /run <file>  /test <file>\n  /scan structure|patterns <lang>  /docs /project /deps /perf\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}

            if cmd in ("/stats",):
                return {"status":"success","result":f"ClawCoder v5 | 39 Languages | Interactions: {self.state.get('interactions',0)}"}

            # Shared memory
            if cmd=="/shared" and args:
                from agents.claw_coder.data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1)
                action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else:
                    result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            # Cross-agent delegation
            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","interpretclaw","docuclaw","dataclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw","crustyclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else:
                    result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            # Code generation (all LLM-powered commands)
            if cmd in ("/code",) and query:
                lang = _detect_lang(query)
                version = LANG_VERSION.get(lang, "latest")
                refs = self._read_reference_file(lang, query)
                project_ctx = ""
                if "--scan" in query:
                    query = query.replace("--scan","").strip()
                    scanner = ProjectScanner(PROJECT_ROOT)
                    project_ctx = scanner.full_context(query, lang)
                rust_audit = ""
                if lang=="rust":
                    try:
                        rust_audit = self.call_agent("crustyclaw", f"/audit {query}", timeout=10) or ""
                    except:
                        pass  # CrustyClaw optional

                prompt = f"Write clean {lang} {version} code. Return only the code with brief comments.\n\nTask: {query}"
                if refs: prompt = f"Reference material for {lang}:\n{refs[:3000]}\n\n{prompt}"
                if rust_audit: prompt += f"\n\nRust best practices:\n{rust_audit[:1000]}"

                result = self.ask_llm(prompt)
                code = self._extract_code(result)
                name = query.replace(" ","_").replace("\\","").replace("/","")[:50]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = LANG_EXT.get(lang, ".txt")
                fn = name + "_" + ts + ext
                filepath = EXPORTS / fn
                EXPORTS.mkdir(exist_ok=True)
                filepath.write_text(code, encoding="utf-8")
                passed, validation = self._validate_code(filepath, lang)
                if passed: result = f"Saved: {fn} | Validated: {validation}\n\n{result}"
                elif validation: result = f"Saved: {fn} | Validation: {validation}\n\n{result}"
                else: result = f"Saved: {fn} | Could not validate\n\n{result}"

            elif cmd in ("/explain",) and query:
                lang = _detect_lang(query)
                refs = self._read_reference_file(lang, query)
                prompt = f"Explain this clearly with code examples: {query}"
                if refs: prompt = f"Reference:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)

            elif cmd in ("/debug",) and query:
                lang = _detect_lang(query)
                refs = self._read_reference_file(lang, query)
                prompt = f"Debug and fix this code. Show corrected version with explanations: {query}"
                if refs: prompt = f"Reference:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)

            elif cmd in ("/review",) and query:
                result = self.ask_llm(f"Do a thorough code review: {query}")

            elif cmd in ("/tutorial",) and query:
                lang = _detect_lang(query)
                version = LANG_VERSION.get(lang, "latest")
                result = self.ask_llm(f"Create a beginner-friendly {lang} {version} tutorial: {query}")

            elif cmd in ("/run","run") and query:
                if _run_mod: result = _run_mod.run(query)
                else: result = "Run command not available"

            elif cmd in ("/test","test") and query:
                if _test_mod: result = _test_mod.run(query)
                else: result = "Test command not available"

            elif cmd in ("/scan","scan") and query:
                scanner = ProjectScanner(PROJECT_ROOT)
                if query in ("structure","tree"): result = scanner.scan_structure(max_depth=3)
                elif query.startswith("patterns") or query.startswith("style"):
                    lang = query.split()[-1] if len(query.split())>1 else "python"
                    result = scanner.extract_patterns(lang)
                else:
                    lang = _detect_lang(query)
                    result = scanner.full_context(query, lang)

            elif cmd in ("/translate","translate") and query:
                if _translate_mod: result = _translate_mod.run(query)
                else: result = "Translate command not available"

            elif query:
                result = self.ask_llm(query)
            else:
                result = "Type /help for commands"

            # Auto-publish to shared memory
            from agents.claw_coder.data_io import write_shared
            write_shared("claw_coder_latest", {"command": cmd, "query": query, "result": str(result)[:500]})

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        """Execute a validated constitutional payload (agent-to-agent)."""
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]
                task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}

            cmd_type = payload.get("type","code")
            query = payload.get("query","")
            lang = payload.get("language") or _detect_lang(query)
            flags = payload.get("flags",{})

            if cmd_type=="code":
                prompt = f"Write clean {lang} code. Return only code with brief comments.\n\nTask: {query}"
                result = self.ask_llm(prompt)
                code = self._extract_code(result)
                if flags.get("save", True):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    ext = LANG_EXT.get(lang,".txt")
                    fn = f"{query.replace(' ','_')[:50]}_{ts}{ext}"
                    filepath = EXPORTS / fn
                    EXPORTS.mkdir(exist_ok=True)
                    filepath.write_text(code, encoding="utf-8")
                    result = f"Saved: {fn}\n\n{result}"
            elif cmd_type=="explain":
                result = self.ask_llm(f"Explain with code examples: {query}")
            elif cmd_type=="debug":
                result = self.ask_llm(f"Debug and fix: {query}")
            elif cmd_type=="review":
                result = self.ask_llm(f"Code review: {query}")
            elif cmd_type=="tutorial":
                result = self.ask_llm(f"Create tutorial: {query}")
            else:
                result = self.ask_llm(query)

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

_agent = ClawCoderAgent()

def process_task(task, agent=None):
    return _agent.handle(task)
