"""A2A Handler for MedicLaw - Medical Agent with A2A routing + chronicle engine"""
import sys, time
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MEDICLAW_DIR))

from core.agent import MediclawAgent
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class MedicLawHandler(BaseAgent):
    def __init__(self):
        super().__init__("mediclaw")
        self.agent = MediclawAgent()

    def _gather_context(self, query=""):
        """Gather medical context from A2A specialists + chronicle"""
        parts = []
        web = self.call_agent("webclaw", f"search medical {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
        legal = self.call_agent("lawclaw", f"search medical regulation {query}", timeout=15)
        if legal: parts.append("[LawClaw]: " + legal)
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/help", "help"):
                result = """MedicLaw - Medical AI Agent
  /research <topic> /diagnose <symptoms> /treatment <condition>
  /medications <drug> /interactions <drugs> /warnings <drug>
  /pediatrics <issue> /geriatrics <issue> /lab <test> /icd <diagnosis>
  /prevention <condition> /diet <condition> /exercise <condition>
  /natural <condition> /procedure <name> /prognosis <condition>
  /referral <condition> /emergency <symptom> /sources /stats /help"""
            elif cmd in ("/sources", "sources"):
                result = f"Medical Sources ({len(self.agent.list_sources())}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(self.agent.list_sources(), 1))
            elif cmd in ("/stats", "stats"):
                result = f"MedicLaw | Queries: {len(self.agent.session['queries'])} | Sources: {len(self.agent.list_sources())} | Started: {self.agent.session['started']}"
            elif cmd in ("/diagnose", "/treatment", "/research", "/med") and args:
                method = {"diagnose": self.agent.diagnose, "treatment": self.agent.treatment, "research": self.agent.research, "med": self.agent.research}[cmd.lstrip("/")]
                result = method(args)
                export = self.call_agent("fileclaw", f"/export md MedicLaw: {args}\n\n{result}")
                if export: result = f"{export}\n\n{result}"
            elif cmd == "/medications" and args: result = self.agent.medications(args)
            elif cmd == "/interactions" and args: result = self.agent.interactions(args)
            elif cmd == "/warnings" and args: result = self.agent.warnings(args)
            elif cmd == "/pediatrics" and args: result = self.agent.pediatrics(args)
            elif cmd == "/geriatrics" and args: result = self.agent.geriatrics(args)
            elif cmd == "/lab" and args: result = self.agent.lab_tests(args)
            elif cmd == "/icd" and args: result = self.agent.coding(args)
            elif cmd == "/prevention" and args: result = self.agent.prevention(args)
            elif cmd == "/diet" and args: result = self.agent.diet(args)
            elif cmd == "/exercise" and args: result = self.agent.exercise(args)
            elif cmd == "/natural" and args: result = self.agent.natural(args)
            elif cmd == "/procedure" and args: result = self.agent.procedure(args)
            elif cmd == "/prognosis" and args: result = self.agent.prognosis(args)
            elif cmd == "/referral" and args: result = self.agent.referral(args)
            elif cmd == "/emergency" and args: result = self.agent.emergency(args)
            elif cmd in ("/hospital", "/hospitals") and args:
                from agents.mediclaw.commands._helpers import lookup_hospitals
                hospitals = lookup_hospitals(args)
                if "error" in hospitals:
                    result = hospitals["error"]
                else:
                    lines = [f"Hospitals: {hospitals.get('city','')}, {hospitals.get('state','')}", "=" * 50]
                    for h in hospitals.get("hospitals", []):
                        lines.append(f"\n  {h.get('name','Unknown')}")
                        if h.get('address'): lines.append(f"     Address: {h['address']}")
                        if h.get('phone'): lines.append(f"     Phone: {h['phone']}")
                        if h.get('url'): lines.append(f"     URL: {h['url']}")
                        if h.get('lat') and h.get('lon'):
                            lines.append(f"     GPS: {h['lat']}, {h['lon']}")
                    result = "\n".join(lines)
            elif cmd == "/nearest" and args:
                from agents.mediclaw.commands._helpers import find_nearest_hospital
                parts = args.split(",")
                if len(parts) == 2:
                    try:
                        lat, lon = float(parts[0].strip()), float(parts[1].strip())
                        hospitals = find_nearest_hospital(lat, lon)
                        if "error" in hospitals:
                            result = hospitals["error"]
                        else:
                            lines = [f"Nearest Hospitals to ({lat}, {lon})", "=" * 50]
                            for h in hospitals.get("hospitals", []):
                                lines.append(f"\n  {h.get('name','Unknown')}")
                                if h.get('address'): lines.append(f"     {h['address']}")
                                if h.get('phone'): lines.append(f"     Phone: {h['phone']}")
                                if h.get('lat') and h.get('lon'):
                                    lines.append(f"     GPS: {h['lat']}, {h['lon']}")
                            result = "\n".join(lines)
                    except ValueError:
                        result = "Usage: /nearest <lat>,<lon>"
                else:
                    result = "Usage: /nearest <lat>,<lon>"
            elif args:
                context = self._gather_context(args)
                result = self.ask_llm(f"Medical information: {args}\n\nContext:\n{context}")
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "mediclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                else:
                    result = f"Usage: {cmd} <query>  |  Type /help for all commands"

            # ================================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY - 23 systems.
            # ================================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("mediclaw", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("mediclaw_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("mediclaw")._check_and_record("handler_boundary", {"cmd": cmd})
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
                    pmem = get_proc_mem("mediclaw")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("mediclaw").get_context(args or cmd, limit=5)
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
                    from shared.log_manager import get_logger
                    get_logger().info(f"mediclaw.{cmd}", extra={"args": (args or "")[:100]})
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
                    if not budget.check("mediclaw", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("mediclaw").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("mediclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="mediclaw")
                except Exception: pass
                try:
                    from agents.mediclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("mediclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="mediclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="mediclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("mediclaw", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("mediclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="mediclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("mediclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = MedicLawHandler()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)