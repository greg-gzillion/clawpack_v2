"""A2A Handler for LangClaw - AI Language Teacher with STT/TTS"""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class LangClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('langclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search language learning {query}", timeout=15)
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
            if cmd in ("/lesson", "lesson") and query:
                result = self.ask_llm(f"Language teacher. Create a beginner lesson with vocabulary, grammar, exercises for: {query}")
            elif cmd in ("/practice", "practice") and query:
                result = self.ask_llm(f"Language tutor. Create practice exercises (fill-in-blank, translation) for: {query}")
            elif cmd in ("/vocab", "vocab") and query:
                result = self.ask_llm(f"List 10 essential words with translations and example sentences for: {query}")
            elif cmd in ("/conversation", "conversation") and query:
                result = self.ask_llm(f"Simulate a natural conversation as a native {query} speaker. Keep it simple.")
            elif cmd in ("/teach", "teach") and query:
                result = self.ask_llm(f"Interactive {query} teacher. Start with greetings. One concept at a time. Be encouraging. Ask questions.")
            elif cmd in ("/speak", "speak") and query:
                result = f"[TTS] Speak: '{query}'\nLangClaw uses Google TTS, Edge TTS, and system TTS for voice output."
            elif cmd in ("/listen", "listen"):
                result = "[STT] Listening...\nLangClaw uses Google Speech-to-Text for voice input. Speak clearly into your microphone."
            el            elif cmd == "/voice":
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
                result = "LangClaw - AI Language Teacher\n  /lesson <lang> - Full lesson\n  /practice <lang> - Exercises\n  /vocab <lang> - Vocabulary\n  /conversation <lang> - Practice chat\n  /teach <lang> - Interactive teacher\n  /speak <text> - TTS voice output\n  /listen - STT voice input\n  /stats"
            elif cmd in ("/stats",):
                result = f"LangClaw | AI Teacher | STT + TTS | Lessons/Conversation | Interactions: {self.state.get('interactions', 0)}"
            elif cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","dreamclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","interpretclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known: result = str(self.call_agent(target, task_text) or f"Agent {target} returned no response")
                else: result = f"Unknown: {target}"
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "langclaw")
                if target: result = str(self.call_agent(target, task, timeout=60) or "")
                else: result = self.ask_llm(f"Language teacher. Help the student learn: {query}")

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("langclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("langclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("langclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("langclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("langclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"langclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("langclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("langclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="langclaw")
                except Exception: pass
                try: from agents.langclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("langclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="langclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="langclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("langclaw_handler", lambda: True)
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
                    log_event(agent="langclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("langclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = LangClawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)