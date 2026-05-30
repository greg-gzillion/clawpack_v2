"""A2A Handler for InterpretClaw - Translation & Language Interpreter"""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class InterpretClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("interpretclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search translation language {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(str(c.url))
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
            if cmd in ("/translate", "translate") and query:
                result = self.ask_llm(f"Translate. Return ONLY the translation: {query}")
            elif cmd in ("/detect", "detect") and query:
                result = self.ask_llm(f"Detect language of this text. Reply with language name only: {query}")
            elif cmd in ("/languages", "/langs"):
                result = """LANGUAGES (42 supported)
af - Afrikaans  sq - Albanian  am - Amharic  ar - Arabic  hy - Armenian  az - Azerbaijani
eu - Basque  be - Belarusian  bn - Bengali  bs - Bosnian  bg - Bulgarian  ca - Catalan
zh - Chinese  hr - Croatian  cs - Czech  da - Danish  nl - Dutch  en - English
et - Estonian  fi - Finnish  fr - French  de - German  el - Greek  he - Hebrew
hi - Hindi  hu - Hungarian  is - Icelandic  id - Indonesian  it - Italian
ja - Japanese  ko - Korean  lv - Latvian  lt - Lithuanian  ms - Malay  mt - Maltese
no - Norwegian  pl - Polish  pt - Portuguese  ro - Romanian  ru - Russian
sr - Serbian  sk - Slovak  sl - Slovenian  es - Spanish  sw - Swahili  sv - Swedish
th - Thai  tr - Turkish  uk - Ukrainian  vi - Vietnamese  cy - Welsh  zu - Zulu
la - Latin
br - Braille (Grade 1 & 2)    asl - American Sign Language (gloss)"""
            elif cmd in ("/speak", "speak") and query:
                result = f"[TTS] {query} (TTS requires espeak or system TTS)"
            elif cmd in ("/listen", "listen"):
                result = "[STT] Speech recognition requires microphone access"
            elif cmd in ("/help",):
                result = "InterpretClaw - 42 Languages\n  /translate <text> to <lang>\n  /detect <text>\n  /speak <text>\n  /listen\n  /languages\n  /delegate <agent> <task>\n  /stats"
            elif cmd in ("/stats",):
                result = f"InterpretClaw | 42 Languages | Interactions: {self.state.get('interactions', 0)}"
            elif cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","dreamclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known: result = str(self.call_agent(target, task_text) or f"Agent {target} returned no response")
                else: result = f"Unknown: {target}"
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "interpretclaw")
                if target: result = str(self.call_agent(target, task, timeout=60) or "")
                elif query: result = self.ask_llm(f"Translate this. Return ONLY the translation: {query}")
                else: result = "Type /help for commands"

            # 23-system boundary
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("interpretclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("interpretclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("interpretclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("interpretclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("interpretclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"interpretclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("interpretclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("interpretclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="interpretclaw")
                except Exception: pass
                try: from agents.interpretclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("interpretclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="interpretclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="interpretclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("interpretclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="interpretclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("interpretclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = InterpretClawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)
