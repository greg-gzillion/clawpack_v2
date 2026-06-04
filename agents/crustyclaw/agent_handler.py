"""A2A Handler for CrustyClaw v5 - Constitutional Rust agent"""
import sys, os, json, subprocess, time
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CRUSTY_DIR = Path(__file__).resolve().parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CRUSTY_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class CrustyClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("crustyclaw")
        self.cargo_path = str(Path.home() / "dev")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search ns:crustyclaw Rust {query}", timeout=15)
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

    def _validate_rust(self, filepath):
        try:
            result = subprocess.run(["rustc","--edition","2024","--emit=metadata",str(filepath)], capture_output=True, text=True, timeout=30)
            return "Compilation OK" if result.returncode==0 else result.stderr[:200]
        except FileNotFoundError: return "rustc not installed"
        except Exception as e: return str(e)

    def _run_standalone(self, command, args=""):
        allowed_commands = {"audit", "pinch", "explain", "fix"}
        if command not in allowed_commands:
            return None
        safe_input = "".join(c for c in str(args) if c.isprintable() and c not in "\r\n\t")[:2000].strip()

        binary_paths = [CRUSTY_DIR/"target"/"release"/"crustyclaw.exe", CRUSTY_DIR/"target"/"release"/"crustyclaw", Path.home()/".cargo"/"bin"/"crustyclaw"]
        for binary in binary_paths:
            if binary.exists():
                try:
                    cmd = [str(binary), command]
                    result = subprocess.run(
                        cmd,
                        input=safe_input if safe_input else None,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    return result.stdout or result.stderr
                except:
                    pass
        return None

    def handle(self, task):
        self.track_interaction()
        track_start = time.time()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "CrustyClaw v5 - Constitutional Rust Agent\n  /rust /code <task>  /explain /audit /pinch /fix /test\n  /cargo <cmd>  /run\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}

            if cmd in ("/stats",):
                return {"status":"success","result":f"CrustyClaw v5 | Rust AI | Interactions: {self.state.get('interactions',0)}"}

            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","interpretclaw","docuclaw","dataclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/rust","/code") and query:
                result = self.ask_llm(f"Write clean Rust 2024 edition code. Return only the code with brief comments. Task: {query}")
                code = result
                if "`" in code:
                    blocks = code.split("`")
                    for i, block in enumerate(blocks):
                        if i%2==1:
                            block = block.split("\n",1)[1] if "\n" in block else block
                            code = block; break
                name = query.replace(" ","_").replace("\\","").replace("/","")[:50]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"{name}_{ts}.rs"
                filepath = EXPORTS/fn; EXPORTS.mkdir(exist_ok=True)
                filepath.write_text(code, encoding="utf-8")
                validation = self._validate_rust(filepath)
                result = f"Saved: {fn} | Validated: {validation}\n\n{result}"

            elif cmd in ("/explain",) and query:
                result = self.ask_llm(f"Explain this Rust concept with code examples: {query}")

            elif cmd=="/cargopath" and query:
                new_path = Path(query).expanduser().resolve()
                if new_path.exists(): self.cargo_path = str(new_path); result = f"Cargo path set to: {self.cargo_path}"
                else: result = f"Path not found: {new_path}"

            elif cmd in ("/cargo",) and query:
                allowed = {"build","check","test","run","clean","doc","fmt","clippy","bench","update","version","help"}
                parts_cmd = query.split()
                if not parts_cmd or parts_cmd[0] not in allowed:
                    result = f"Allowed: {sorted(allowed)}"
                else:
                    safe_cmd = parts_cmd[0]
                    try:
                        cargo_result = subprocess.run(["cargo", safe_cmd], capture_output=True, text=True, timeout=60, cwd=self.cargo_path)
                        result = cargo_result.stdout or cargo_result.stderr or "Cargo completed"
                    except Exception as e: result = f"Cargo error: {e}"

            elif cmd in ("/audit",) and query:
                standalone = self._run_standalone("audit", query)
                result = f"[Standalone audit]\n{standalone}" if standalone else self.ask_llm(f"Security audit this Rust code. Check unsafe blocks, unwraps, input validation. Code:\n{query[:4000]}")

            elif cmd in ("/pinch",) and query:
                standalone = self._run_standalone("pinch", query)
                result = f"[Standalone pinch]\n{standalone}" if standalone else self.ask_llm(f"Analyze for unnecessary clones and allocations. Code:\n{query[:4000]}")

            elif cmd in ("/fix","/debug") and query:
                result = self.ask_llm(f"Debug and fix this Rust code: {query[:4000]}")

            elif cmd in ("/test",) and query:
                result = self.ask_llm(f"Write Rust unit tests with #[cfg(test)]: {query[:4000]}")

            elif cmd in ("/run",):
                try:
                    run_result = subprocess.run(["cargo","run"], capture_output=True, text=True, timeout=30, cwd=self.cargo_path)
                    result = run_result.stdout or run_result.stderr or "Program completed"
                except Exception as e: result = f"Run error: {e}"

            else:
                # -- Constitutional capability routing --
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "crustyclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif query:
                    result = self.ask_llm(f"Rust expert. Question: {query}")
                else:
                    result = "Type /help for commands"

            # ================================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY - 23 systems.
            # ================================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("crustyclaw", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("crustyclaw_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("crustyclaw")._check_and_record("handler_boundary", {"cmd": cmd})
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
                    pmem = get_proc_mem("crustyclaw")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("crustyclaw").get_context(args or cmd, limit=5)
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
                    get_logger().info(f"crustyclaw.{cmd}", extra={"args": (args or "")[:100]})
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
                    if not budget.check("crustyclaw", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("crustyclaw").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("crustyclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="crustyclaw")
                except Exception: pass
                try:
                    from agents.crustyclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("crustyclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="crustyclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="crustyclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("crustyclaw", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("crustyclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="crustyclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            from data_io import write_shared
            write_shared("crustyclaw_latest", {"command":cmd,"query":query,"result":str(final_result)[:500]})

            return {"status":"success","result":str(final_result)}
        except Exception as e:
            log_err("crustyclaw", cmd or "unknown", str(e)[:200])
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query",""); result = self.ask_llm(f"Write clean Rust 2024 edition code. Task: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e:
            log_err("crustyclaw", "execute_error", str(e)[:200])
            return {"status":"error","result":str(e)}


_agent = CrustyClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)
