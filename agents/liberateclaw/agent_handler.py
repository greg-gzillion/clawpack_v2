"""A2A Handler for LiberateClaw - Model Liberation & Management"""
import sys, time
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

MODELS_FILE = PROJECT_ROOT / "models" / "working_llms.json"

class LiberateClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('liberateclaw')

    def _get_models(self):
        if MODELS_FILE.exists():
            return json.loads(MODELS_FILE.read_text())
        return []

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search AI model {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/models", "models"):
                models = self._get_models()
                obliterated = [m for m in models if m.get('obliterated')]
                standard = [m for m in models if not m.get('obliterated')]
                result = f"OBLITERATED MODELS ({len(obliterated)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in obliterated)
                result += f"\n\nSTANDARD MODELS ({len(standard)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
            elif cmd in ("/obliterated", "obliterated"):
                models = self._get_models()
                lib = [m for m in models if m.get('obliterated')]
                result = f"OBLITERATED MODELS ({len(lib)}):\n" + "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in lib) + "\n\nUse /use <model> to switch" if lib else "No obliterated models. Use /obliterate <model>"
            elif cmd in ("/liberated", "liberated"):
                models = self._get_models()
                lib = [m for m in models if m.get('obliterated')]
                result = f"Liberated Models ({len(lib)}):\n" + "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in lib)
            elif cmd in ("/obliterate", "obliterate") and query:
                result = f"[OBLITERATE] '{query}' - LiberateClaw removes refusal mechanisms via ablation.\nModels path: models/obliterated/"
            elif cmd in ("/use", "use") and query:
                result = f"[SWITCH] Activating model: {query}\nUse LLMClaw to manage active model selection."
            elif cmd in ("/help",):
                result = "LiberateClaw - Model Liberation\n  /models - All 17 models\n  /liberated - Obliterated only\n  /obliterate <model> - Liberate model\n  /use <model> - Switch model\n  /stats"
            elif cmd in ("/stats",):
                models = self._get_models()
                lib = len([m for m in models if m.get('obliterated')])
                std = len([m for m in models if not m.get('obliterated')])
                result = f"LiberateClaw | {lib} Obliterated + {std} Standard = {len(models)} Total | Interactions: {self.state.get('interactions', 0)}"
            elif cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","dreamclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","interpretclaw","langclaw","fileclaw","txclaw","mediclaw"]
                if target in known: result = str(self.call_agent(target, task_text) or f"Agent {target} returned no response")
                else: result = f"Unknown: {target}"
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "liberateclaw")
                if target: result = str(self.call_agent(target, task, timeout=60) or "")
                else: result = self.ask_llm(f"Expert on AI model liberation and ablation. Answer: {query}")

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("liberateclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("liberateclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("liberateclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("liberateclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("liberateclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"liberateclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("liberateclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("liberateclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="liberateclaw")
                except Exception: pass
                try: from agents.liberateclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("liberateclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="liberateclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="liberateclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("liberateclaw_handler", lambda: True)
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
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="liberateclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("liberateclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = LiberateClawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)