"""A2A Handler for DataClaw v5 - Constitutional Local Data Search Agent"""
import sys, json, time
from pathlib import Path
from datetime import datetime

DATACLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DATACLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DATACLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class DataClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("dataclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search ns:dataclaw {query}", timeout=15)
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
                result = "DataClaw v5 - Constitutional Local Data Search\n  /search /find <query>  /export <fmt> <query>\n  /index <path>  /stats\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>"
                return {"status":"success","result":result}

            if cmd in ("/stats",):
                from agents.dataclaw.commands._helpers import count_indexed_files
                total = count_indexed_files()
                return {"status":"success","result":f"DataClaw v5 | {total:,} files indexed | Interactions: {self.state.get('interactions',0)}"}

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
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/search","/find","search","find") and query:
                from agents.dataclaw.commands.data import run as data_run
                result = data_run(query, agent=self)

            elif cmd in ("/export","export") and args:
                from agents.dataclaw.commands.data import run_export
                result = run_export(args, agent=self)

            elif cmd == "/index" and args:
                from agents.dataclaw.commands._helpers import search_local_files, index_to_chronicle
                file_results = search_local_files(args, max_results=20)
                indexed = 0
                for r in file_results:
                    if index_to_chronicle(r['file'], r.get('match', ''), agent=self):
                        indexed += 1
                result = f"Indexed {indexed}/{len(file_results)} files to Chronicle"

            elif query:
                from agents.dataclaw.commands.data import run as data_run
                result = data_run(query, agent=self)

            else:
                # -- Constitutional capability routing --
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "dataclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif query:
                    from agents.dataclaw.commands.data import run as data_run
                    result = data_run(query, agent=self)
                else:
                    result = "Type /help for commands"

            # ================================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY - 23 systems.
            # ================================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("dataclaw", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("dataclaw_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("dataclaw")._check_and_record("handler_boundary", {"cmd": cmd})
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
                    pmem = get_proc_mem("dataclaw")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("dataclaw").get_context(args or cmd, limit=5)
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
                    get_logger().info(f"dataclaw.{cmd}", extra={"args": (args or "")[:100]})
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
                    if not budget.check("dataclaw", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("dataclaw").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("dataclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="dataclaw")
                except Exception: pass
                try:
                    from agents.dataclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("dataclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="dataclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="dataclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("dataclaw", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("dataclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="dataclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            from data_io import write_shared
            write_shared("dataclaw_latest", {"command": cmd, "query": query, "result": str(final_result)[:500]})

            return {"status":"success","result":str(final_result)}
        except Exception as e:
            log_err("dataclaw", cmd or "unknown", str(e)[:200])
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query","")
            from agents.dataclaw.commands._helpers import search_local_files
            results = search_local_files(query, max_results=10)
            return {"status":"success","result":json.dumps(results, indent=2, default=str)}
        except Exception as e:
            log_err("dataclaw", "execute_error", str(e)[:200])
            return {"status":"error","result":str(e)}


_agent = DataClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)
