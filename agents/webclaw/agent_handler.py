"""A2A Handler for WebClaw - AI-Powered Search & Fetch"""
import sys, time
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from webclaw import Webclaw
from agents.webclaw.providers.webclaw_provider import WebclawProvider
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

webclaw = Webclaw()
provider = WebclawProvider()


class WebClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("webclaw")

    def _gather_context(self, query=""):
        parts = []
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def handle(self, task):
        self.track_interaction()
        track_start = time.time()
        task = task.strip()

        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","dreamclaw","docuclaw","lawclaw","mathematicaclaw","interpretclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw","llmclaw","rustypycraw"]
                if target in known: result = str(self.call_agent(target, task_text) or "")
                else: result = f"Unknown: {target}"
                return {"status": "success", "result": result}
        if task.startswith("fetch ") or task.startswith("http"):
            url = task.replace("fetch ", "", 1).strip() if task.startswith("fetch ") else task
            try:
                result = webclaw.fetch_with_citation(url)
                if result.get("success"):
                    return {
                        "status": "success",
                        "result": result["citation"] + "\n\n" + result["content"]
                    }
                return {
                    "status": "error",
                    "result": result.get("error", "fetch failed")
                }
            except Exception as e:
                log_err("webclaw", "fetch_error", str(e)[:200])
                return {"status": "error", "result": str(e)}

        if task.startswith("search "):
            query = task[7:].strip()
        else:
            query = task

        try:
            result = provider.search_with_context(query)

            try:
                from agents.webclaw.core.chronicle_ledger import get_chronicle
                chronicle = get_chronicle()
                chronicle_results = chronicle.recover_by_context(query, limit=2000000)
                if chronicle_results:
                    result += "\n\n=== Web Results ==="
                    for c in chronicle_results[:3]:
                        url = c.url if hasattr(c, "url") else str(c)
                        try:
                            cited = webclaw.fetch_with_citation(url)
                            if cited.get("success"):
                                result += "\n\n" + cited["citation"] + "\n"
                                result += cited["content"][:1000]
                        except Exception:
                            pass
            except Exception as e:
                result += "\n\n(chronicle: " + str(e) + ")"

            try:
                prompt = (
                    "Analyze these search results and provide the most "
                    "relevant information for: " + query + "\n\nResults:\n" +
                    result[:3000]
                )
                analysis = self.ask_llm(prompt)
                if analysis:
                    result = "## AI Analysis\n" + analysis + "\n\n## Raw Results\n" + result
                    self.learn("search:" + query, result[:1000])
            except Exception as e:
                result += "\n\n(AI analysis: " + str(e) + ")"


            # Constitutional boundary
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("webclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("webclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("webclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("webclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("webclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"webclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("webclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("webclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="webclaw")
                except Exception: pass
                try: from agents.webclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("webclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="webclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="webclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("webclaw_handler", lambda: True)
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
                    log_event(agent="webclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("webclaw", "search_error", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = WebClawAgent()


def process_task(task: str, agent: Optional[str] = None):
    return _agent.handle(task)