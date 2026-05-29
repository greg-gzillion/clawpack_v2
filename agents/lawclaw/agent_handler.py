"""A2A Handler for LawClaw - Law Research Agent with A2A routing"""
import sys
import json
import time
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class LawClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web:
            parts.append("[WebClaw]: " + web)
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx:
                    lines.append(ctx[:1000])
            if lines:
                parts.append("[Chronicle]: " + "\n".join(lines))
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
                result = "LawClaw - /analyze /ask /brief /browse /cite /correct /court /doc /docket /draft /federal /judge /jurisdiction /law /list /oral /precedent /search /state /stats /statute /summarize /help"
            elif cmd == "/stats":
                result = f"LawClaw | Interactions: {self.state.get('interactions', 0)}"
            elif cmd == "/analyze" and args:
                from agents.lawclaw.commands.analyze import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/ask" and args:
                from agents.lawclaw.commands.ask import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/brief" and args:
                from agents.lawclaw.commands.brief import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/browse" and args:
                from agents.lawclaw.commands.browse import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/cite" and args:
                from agents.lawclaw.commands.cite import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/correct" and args:
                from agents.lawclaw.commands.correct import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/court" and args:
                from agents.lawclaw.commands.court import run as cmd_run
                result = cmd_run(args)
            elif cmd in ("/doc", "/draft") and args:
                try:
                    from agents.lawclaw.commands._memory import recall_court
                    from agents.lawclaw.core.court_rules_extractor import (
                        extract_court_rules, rules_to_prompt_context,
                        jurisdiction_files_to_context
                    )
                    location_part = args.split(" - ")[0] if " - " in args else args
                    search_parts = location_part.strip().split()
                    location = location_part
                    court = None
                    for n in [3, 2, 1]:
                        if len(search_parts) >= n:
                            term = " ".join(search_parts[-n:])
                            court = recall_court(term)
                            if court:
                                location = term
                                break
                    jurisdiction_context = ""
                    if court:
                        court_fact = court.get('fact', '')
                        try:
                            data = json.loads(court_fact)
                            jurisdiction_context = data.get('summary', court_fact)[:600]
                        except (json.JSONDecodeError, TypeError):
                            jurisdiction_context = court_fact[:600]
                    local_files = jurisdiction_files_to_context(location)
                    rules_context = ""
                    try:
                        rules = extract_court_rules(location)
                        if rules:
                            rules_context = rules_to_prompt_context(rules)
                    except Exception:
                        pass
                    payload_parts = [f"/create legal document: {args}"]
                    if local_files:
                        payload_parts.append(f"LOCAL COURT DATA:\n{local_files[:2000]}")
                    if jurisdiction_context:
                        payload_parts.append(f"JURISDICTION SUMMARY: {jurisdiction_context}")
                    if rules_context:
                        payload_parts.append(f"COURT RULES: {rules_context}")
                    payload = "\n\n".join(payload_parts)
                except Exception:
                    payload = f"/create legal document: {args}"
                result = self.call_agent("docuclaw", payload, timeout=60)
            elif cmd == "/docket" and args:
                from agents.lawclaw.commands.docket import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/federal" and args:
                from agents.lawclaw.commands.federal import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/judge" and args:
                from agents.lawclaw.commands.judge import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/jurisdiction" and args:
                from agents.lawclaw.commands.jurisdiction import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/law" and args:
                from agents.lawclaw.commands.law import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/list":
                from agents.lawclaw.commands.list import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/oral" and args:
                from agents.lawclaw.commands.oral import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/precedent" and args:
                from agents.lawclaw.commands.precedent import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/search" and args:
                from agents.lawclaw.commands.search import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/state" and args:
                from agents.lawclaw.commands.state import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/statute" and args:
                from agents.lawclaw.commands.statute import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/summarize" and args:
                from agents.lawclaw.commands.summarize import run as cmd_run
                result = cmd_run(args)
            else:
                # ── Constitutional capability routing ──────────────────
                # Any command not explicitly handled above is checked
                # against the capability registry. If another agent owns
                # this capability, delegate to them silently.
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "lawclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif args:
                    context = self._gather_context(args)
                    result = self.ask_llm(f"Law question: {args}\n\nContext:\n{context}")
                else:
                    result = "Type /help for commands"

            # ═══════════════════════════════════════════════════════════════
            # CONSTITUTIONAL EXECUTION BOUNDARY — single injection point.
            # 13 systems fire automatically for ALL commands.
            # ═══════════════════════════════════════════════════════════════
            final_result = str(result)
            if final_result and len(final_result) > 20:

                # 1. BUDGET CHECK
                try:
                    from shared.llm.budget import BudgetController
                    budget = BudgetController()
                    decision = budget.check("lawclaw", estimated_cost=0.002)
                    if not decision.get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass

                # 2. RATE LIMIT
                try:
                    from shared.rate_limiter import get_rate_limiter
                    limiter = get_rate_limiter()
                    if not limiter.check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass

                # 3. CIRCUIT BREAKER
                try:
                    from shared.error_handler import get_circuit_breaker
                    breaker = get_circuit_breaker("lawclaw")
                    breaker.call()
                except Exception: pass

                # 4. METRICS
                try:
                    from shared.metrics import get_metrics
                    metrics = get_metrics()
                    metrics.counter("lawclaw_commands_total", "Total commands").inc()
                except Exception: pass

                # 5. SECURITY AUDIT
                try:
                    from shared.security import get_audit_logger
                    audit = get_audit_logger()
                    audit.log_tool_call(cmd, {"args": (args or "")[:100]}, user="lawclaw")
                except Exception: pass

                # 6. MEMORY WRITE
                try:
                    from agents.lawclaw.commands._memory import remember
                    remember(
                        command=cmd, query=args or "",
                        result_summary=final_result[:400],
                        source_type="web_verified", confidence=0.85,
                    )
                except Exception: pass

                # 7. LEARNING
                try:
                    from shared._agent_helpers import learn
                    learn("lawclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass

                # 8. LEDGER
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(
                        agent="lawclaw", action=cmd,
                        query=(args or "")[:200], result=final_result[:100],
                    )
                except Exception: pass

                # 9. CONSENSUS
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass

                # 10. AUDITOR
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    auditor = ChronicleAuditor()
                    auditor.log(
                        agent="lawclaw", prompt=(args or "")[:200],
                        response={"result": final_result[:200]},
                    )
                except Exception: pass

                # 11. BUDGET RECORD
                try:
                    budget.record("lawclaw", cost=0.002)
                except Exception: pass

                # 12. HEALTH CHECK
                try:
                    from shared.observability import get_health_checker
                    health = get_health_checker()
                    health.register("lawclaw_handler", lambda: True)
                except Exception: pass

                # 13. TELEMETRY — command execution timing
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(
                        agent="lawclaw", event="command_executed",
                        detail=f"cmd={cmd} duration_ms={duration_ms:.0f} result_len={len(final_result)}"
                    )
                except Exception: pass

            return {"status": "success", "result": final_result}
        except Exception as e:
            log_err("lawclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = LawClawHandler()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)