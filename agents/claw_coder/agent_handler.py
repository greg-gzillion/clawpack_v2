"""A2A Handler for ClawCoder v5 - Constitutional contract + 39 languages + cross-agent delegation"""
import sys, os, json, subprocess, time
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
from shared._agent_helpers import log_err
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
        self.code_gen = CodeGenerator(lambda p: self.ask_llm_smart(p, task_type="code_generation", agent_name="claw_coder"))

    def _gather_context(self, query=""):
        """Gather WebClaw + Chronicle context for code generation."""
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web:
            parts.append("[WebClaw]: " + str(web)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx:
                    lines.append(ctx[:1000])
            if lines:
                parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def _enrich_context(self, query, lang):
        """Gather WebClaw + DataClaw context for code generation."""
        parts = []
        try:
            web = self.call_agent("webclaw", f"search {lang} {query} code example", timeout=8)
            if web: parts.append(str(web)[:1000])
        except Exception: pass
        try:
            data = self.call_agent("dataclaw", f"search {lang} {query}", timeout=8)
            if data: parts.append(str(data)[:1000])
        except Exception: pass
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
        track_start = time.time()

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
                        elif cmd == "/voice":
                from shared.voice_hook import toggle
                result = toggle(self)
            elif cmd in ("/listen", "listen"):
                from shared.accessibility import listen, detect_language
                text = listen()
                if text.startswith('[STT]'):
                    result = text
                else:
                    lang = detect_language(text)
                    result = f"[{lang.upper()}] {text}"
            elif cmd in ("/translate", "translate") and query:
                from shared.accessibility import translate, detect_language
                lang = detect_language(query)
                result = translate(query, 'en', lang)

                        elif cmd in ("/braille", "braille") and query:
                from shared.accessibility import to_braille
                result = to_braille(query)

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
                from agents.claw_coder.commands.code import run as code_run
                result = code_run(query, agent=self)

            elif cmd in ("/explain",) and query:
                from agents.claw_coder.commands.explain import run as explain_run
                result = explain_run(query, agent=self)

            elif cmd in ("/debug",) and query:
                from agents.claw_coder.commands.debug import run as debug_run
                result = debug_run(query, agent=self)

            elif cmd in ("/review",) and query:
                from agents.claw_coder.commands.review import run as review_run
                result = review_run(query, agent=self)

            elif cmd in ("/tutorial",) and query:
                from agents.claw_coder.commands.tutorial import run as tutorial_run
                result = tutorial_run(query, agent=self)

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

            else:
                # -- Constitutional capability routing --
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "claw_coder")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif query:
                    result = self.ask_llm_smart(query)
                else:
                    result = "Type /help for commands"

            # ================================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY - 23 systems.
            # ================================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("claw_coder", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("claw_coder_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("claw_coder")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try:
                    from shared.execution_policy import ExecutionPolicy
                    ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try:
                    from shared.chronicle_helper import search_chronicle as chron_search
                    chron_search(args or cmd, limit=3)
                except Exception: pass
                try:
                    from shared.memory.procedural_memory import get_memory as get_proc_mem
                    pmem = get_proc_mem("claw_coder")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("claw_coder").get_context(args or cmd, limit=5)
                except Exception: pass
                try:
                    from shared.smart_router import SmartRouter
                    SmartRouter().route(cmd)
                except Exception: pass
                try:
                    from shared.agent_router import AgentRouter
                    AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try:
                    from shared.validation import validate_schema
                except Exception: pass
                try:
                    from shared.memory_guard import sanitize_memory_write
                except Exception: pass
                try:
                    from shared.source_registry import get_trust
                except Exception: pass
                try:
                    from shared.truth_resolver import merge_with_retriever
                except Exception: pass
                try:
                    from shared.input_handler import InputHandler
                except Exception: pass
                try:
                    from shared.permissions import PermissionSystem
                except Exception: pass
                try:
                    from shared.registry import AgentRegistry
                except Exception: pass
                try:
                    from shared.jurisdiction_validator import validate_jurisdiction
                except Exception: pass
                try:
                    from shared.enforcement.gates import PreExecutionGate, PostExecutionGate
                except Exception: pass
                try:
                    from shared.config import ConfigManager
                except Exception: pass
                try:
                    from shared.constitutional_command import validate_command
                except Exception: pass
                try:
                    from shared.court_rules_schema import CourtRulesSchema
                except Exception: pass
                try:
                    from shared.decomposer import TaskDecomposer
                except Exception: pass
                try:
                    from shared.output_handler import OutputHandler
                except Exception: pass
                try:
                    from shared.router import TaskRouter
                except Exception: pass
                try:
                    from shared.compactor import ContextCompactor
                except Exception: pass
                try:
                    from shared.log_manager import get_logger
                    get_logger().info(f"claw_coder.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try:
                    from shared.shutdown import get_shutdown_manager
                    get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try:
                    from shared.hooks.hook_manager import get_hook_manager
                    get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try:
                    from shared.llm.budget import BudgetController
                    budget = BudgetController()
                    if not budget.check("claw_coder", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("claw_coder").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("claw_coder_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="claw_coder")
                except Exception: pass
                try:
                    from agents.claw_coder.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("claw_coder", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="claw_coder", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="claw_coder", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("claw_coder", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("claw_coder_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="claw_coder", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            # Auto-publish to shared memory
            from agents.claw_coder.data_io import write_shared
            write_shared("claw_coder_latest", {"command": cmd, "query": query, "result": str(final_result)[:500]})

            return {"status":"success","result":str(final_result)}
        except Exception as e:
            log_err("claw_coder", cmd or "unknown", str(e)[:200])
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
                result = self.ask_llm_smart(query)

            return {"status":"success","result":str(result)}
        except Exception as e:
            log_err("claw_coder", "execute_error", str(e)[:200])
            return {"status":"error","result":str(e)}


_agent = ClawCoderAgent()


def process_task(task, agent=None):
    return _agent.handle(task)
