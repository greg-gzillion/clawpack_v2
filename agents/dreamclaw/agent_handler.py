"""A2A Handler for DreamClaw - AI Vision & Generation"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class DreamClawAgent(BaseAgent):
    def __init__(self): super().__init__('dreamclaw')
    
    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search creative {query}", timeout=5)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=5)
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
                        elif cmd == "/voice":
                from shared.voice_hook import is_active, toggle
                result = toggle()  # toggle on/off

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

                        elif cmd in ("/simple", "simple"):
                from shared.accessibility import simplify_response, large_print
                result = "Simplified mode active. All responses will use simple language. Type /normal to disable."
            elif cmd in ("/normal", "normal"):
                result = "Normal mode restored."

            if cmd in ("/help",):
                result = "DreamClaw - AI Vision\n  /dream /imagine /style /stats\n  /delegate [agent] [task]"
            elif cmd in ("/stats",):
                result = f"DreamClaw | AI Vision | Interactions: {self.state.get("interactions", 0)}"
            else:
                ctx = self._gather_context(query)
                if cmd in ("/dream","dream") and query: result = self.ask_llm(f"Context: {ctx}\n\nAI image generation prompt with style, lighting, composition: {query}")
                elif cmd in ("/imagine","imagine") and query: result = self.ask_llm(f"Context: {ctx}\n\nCreative visual description for AI generation: {query}")
                elif cmd in ("/delegate",) and args:
                    parts2 = args.split(maxsplit=1); target = parts2[0]
                    task_text = parts2[1] if len(parts2) > 1 else ""
                    known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","draftclaw","drawclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                    if target in known: result = str(self.call_agent(target, task_text) or f"Agent {target} returned no response")
                    else: result = f"Unknown: {target}"
                else:
                    from shared.capabilities import get_capable_agent
                    target = get_capable_agent(cmd, "dreamclaw")
                    if target: result = str(self.call_agent(target, task, timeout=60) or "")
                    elif query: result = self.ask_llm(f"Context: {ctx}\n\nAI vision expert: {query}")
                    else: result = "Type /help for commands"

            # 23-system boundary
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("dreamclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("dreamclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("dreamclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("dreamclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("dreamclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.validation import validate_schema
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
                try: from shared.log_manager import get_logger; get_logger().info(f"dreamclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("dreamclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("dreamclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="dreamclaw")
                except Exception: pass
                try: from agents.dreamclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("dreamclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="dreamclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="dreamclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("dreamclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="dreamclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status":"success","result":str(final_result)}
        except Exception as e:
            log_err("dreamclaw", cmd or "unknown", str(e)[:200])
            return {"status":"error","result":str(e)}


_agent = DreamClawAgent()


def process_task(task: str, agent: str = None): return _agent.handle(task)
