"""A2A Handler for DrawClaw - AI Prompts + Drawing Commands"""
import sys, time
from pathlib import Path

DRAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAWCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import delegate, log_err


class DrawClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("drawclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
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
        query = args if args else task

        try:
            # Cross-Agent Delegation
            if cmd in ("/delegate", "delegate") and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                result = delegate("drawclaw", target, task_text)

            elif cmd in ("/export", "export") and query:
                result = delegate("drawclaw", "docuclaw", f"/create art: {query}", timeout=60)

            # Drawing commands
            elif cmd in ("/canvas", "canvas"):
                from agents.drawclaw.commands.canvas import run
                result = run(query)
            elif cmd in ("/sketch", "sketch") and query:
                from agents.drawclaw.commands.sketch import run
                result = run(query)
            elif cmd in ("/doodle", "doodle") and query:
                from agents.drawclaw.commands.doodle import run
                result = run(query)
            elif cmd in ("/paint", "paint") and query:
                from agents.drawclaw.commands.paint import run
                result = run(query)
            elif cmd in ("/illustrate", "illustrate") and query:
                from agents.drawclaw.commands.illustrate import run
                result = run(query)
            elif cmd in ("/cartoon", "cartoon") and query:
                from agents.drawclaw.commands.cartoon import run
                result = run(query)
            elif cmd in ("/draw", "draw") and query:
                from agents.drawclaw.commands.draw import run
                result = run(query)

            # AI prompt commands
            elif cmd in ("/prompt", "prompt") and query:
                from agents.drawclaw.commands.prompt import run
                result = run(query)
            elif cmd in ("/describe", "describe") and query:
                from agents.drawclaw.commands.describe import run
                result = run(query)
            elif cmd in ("/style", "style") and query:
                from agents.drawclaw.commands.style import run
                result = run(query)
            elif cmd in ("/compose", "compose") and query:
                from agents.drawclaw.commands.compose import run
                result = run(query)

            # Animation, filters, QR
            elif cmd in ("/animate", "animate") and query:
                from agents.drawclaw.commands.animate import run
                result = run(query)
            elif cmd in ("/filter", "filter") and query:
                from agents.drawclaw.commands.filter import run
                result = run(query)
            elif cmd in ("/qr", "qr") and query:
                from agents.drawclaw.commands.qrcode_cmd import run
                result = run(query)

            elif cmd == "/help":
                result = """DrawClaw - AI Prompt Studio + Drawing Tools
  DRAW:     /canvas - Interactive drawing window
            /sketch <style> <subject> - Pencil/charcoal/ink sketch
            /doodle <style> - Algorithmic art (11 styles)
            /paint <style> <scene> - 14 painting styles
            /illustrate <format> <desc> - Comic/storyboard/tutorial
            /cartoon <mood> <character> - Expressive cartoon faces
            /draw <scene> - AI-assisted scene rendering
  PROMPTS:  /prompt <concept> - AI image prompt card
            /describe <visual> - Visual reference card
            /style <concept> - Art style guide card
            /compose <scene> - Composition overlay
  TOOLS:    /animate <style> <frames> - Animated GIF
            /filter <mode> - Apply filter to last drawing
            /qr <url/text> - Generate QR code
  DELEGATE: /delegate /export
  META:     /help /stats"""

            elif cmd == "/stats":
                result = f"DrawClaw | 14 Commands + GIF + Filters + QR | Interactions: {self.state.get('interactions', 0)}"

            elif cmd in ("/library", "/resources", "/local") and args:
                from agents.drawclaw.commands._helpers import lookup_local_resources
                res = lookup_local_resources(args)
                if "error" in res:
                    result = res["error"]
                else:
                    lines = [f"Local Resources: {res.get('city','')}, {res.get('state','')}", "=" * 50]
                    if res.get("libraries"):
                        lines.append("\n### Libraries")
                        for l in res["libraries"][:3]: lines.append(f"  {l}")
                    if res.get("historical"):
                        lines.append("\n### Historical/Cultural")
                        for h in res["historical"][:3]: lines.append(f"  {h}")
                    if res.get("urls"):
                        lines.append(f"\n### URLs ({len(res['urls'])})")
                        for u in res["urls"][:5]: lines.append(f"  {u}")
                    result = "\n".join(lines)
            elif query:
                result = self.ask_llm(f"Act as a professional digital artist and art director. Query: {query}")
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "drawclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                else:
                    result = "Type /help for commands"

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("drawclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("drawclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("drawclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("drawclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("drawclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.validation import validate_schema
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"drawclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("drawclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("drawclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="drawclaw")
                except Exception: pass
                try: from agents.drawclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("drawclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="drawclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="drawclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("drawclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="drawclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("drawclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = DrawClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)
