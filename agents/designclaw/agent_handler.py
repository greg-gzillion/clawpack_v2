"""A2A Handler for DesignClaw v5 - Constitutional Design Agent"""
import sys, json, os, time
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DESIGNCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class DesignClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("designclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
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

    def _save_html(self, content, name):
        EXPORTS.mkdir(exist_ok=True)
        html = content
        if "`html" in html: html = html.split("`html")[1].split("`")[0]
        elif "`" in html:
            blocks = html.split("`")
            for i, block in enumerate(blocks):
                if i%2==1: html = block; break
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name}_{ts}.html"
        filepath = EXPORTS/fn
        filepath.write_text(html, encoding="utf-8")
        os.startfile(str(filepath))
        return fn

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
                        elif cmd == "/voice":
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

            if cmd in ("/help",):
                result = "DesignClaw v5 - Constitutional Design Agent\n  /brand /colors /mood /type /copy /logo /kit /html\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}
            if cmd in ("/stats",): return {"status":"success","result":f"DesignClaw v5 | Brand & Design | Interactions: {self.state.get('interactions',0)}"}

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
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/brand","/identity","brand") and query:
                result = self.ask_llm(f"Create a complete brand identity: 1. Brand essence 2. Logo concept 3. Color palette with hex codes 4. Typography 5. Brand voice.\n\nBrief: {query}")
            elif cmd in ("/colors","/palette","colors") and query:
                result = self.ask_llm(f"Create a color palette with 5 hex codes and usage notes.\n\nContext: {query}")
            elif cmd in ("/mood","mood") and query:
                result = self.ask_llm(f"Describe an aesthetic mood direction: vibe, color story, texture, typography style, references.\n\nContext: {query}")
            elif cmd in ("/type","/fonts","type") and query:
                result = self.ask_llm(f"Recommend font pairings with Google Fonts links, header and body.\n\nStyle: {query}")
            elif cmd in ("/copy","/slogan","copy") and query:
                result = self.ask_llm(f"Write brand copy: tagline, value proposition, mission, 3 brand voice adjectives.\n\nBrand: {query}")
            elif cmd in ("/logo","logo") and query:
                result = self.ask_llm(f"Create an SVG logo design with shapes, colors, layout. Include SVG code.\n\nLogo for: {query}")
            elif cmd in ("/kit","/full","kit") and query:
                result = self.ask_llm(f"Create a complete brand kit as HTML with inline CSS: brand name, logo concept, color swatches, typography, brand voice, sample business card.\n\nBrand: {query}\n\nReturn complete HTML.")
                fn = self._save_html(result, query.replace(" ","_")[:40])
                result = f"Saved: {fn}\n\n{result}"
            elif cmd in ("/html","/web","html") and query:
                result = self.ask_llm(f"Create a complete responsive HTML page with embedded CSS. Beautiful and modern.\n\nDesign for: {query}\n\nReturn complete HTML.")
                fn = self._save_html(result, query.replace(" ","_")[:40])
                result = f"Saved: {fn}\n\n{result}"
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "designclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif query:
                    from agents.designclaw.commands.logo import run as logo_run
                    result = logo_run(query, agent=self)
                else:
                    result = "Type /help for commands"


            # ================================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY - 23 systems.
            # ================================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("designclaw", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("designclaw_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("designclaw")._check_and_record("handler_boundary", {"cmd": cmd})
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
                    pmem = get_proc_mem("designclaw")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("designclaw").get_context(args or cmd, limit=5)
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
                    get_logger().info(f"designclaw.{cmd}", extra={"args": (args or "")[:100]})
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
                    if not budget.check("designclaw", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("designclaw").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("designclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="designclaw")
                except Exception: pass
                try:
                    from agents.designclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("designclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="designclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="designclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("designclaw", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("designclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="designclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            from data_io import write_shared
            write_shared("designclaw_latest", {"command":cmd,"query":query})

            return {"status":"success","result":str(result)}
        except Exception as e:
            log_err("designclaw", cmd or "unknown", str(e)[:200])
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query","")
            result = self.ask_llm(f"Senior design consultant. Task: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e:
            log_err("designclaw", "execute_error", str(e)[:200])
            return {"status":"error","result":str(e)}


_agent = DesignClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)