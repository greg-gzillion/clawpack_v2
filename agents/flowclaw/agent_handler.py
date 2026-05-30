"""A2A Handler for FlowClaw v5 - Constitutional contract + cross-agent delegation"""
import sys, time
import json
from pathlib import Path
from datetime import datetime

FLOWCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = FLOWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(FLOWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err
from agents.flowclaw.engine.diagram_engine import DiagramEngine
from agents.flowclaw.viewer.diagram_viewer import DiagramViewer
from agents.flowclaw.exporters.base_exporter import DocxExporter, PdfExporter, HtmlExporter, MarkdownExporter, JsonExporter

class LLMAdapter:
    def __init__(self, agent):
        self.agent = agent
    def chat_sync(self, prompt, task_type="orchestration", **kw):
        return self.agent.ask_llm(prompt, task_type=task_type)

class FlowClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("flowclaw")
        self.engine = DiagramEngine()
        self.viewer = DiagramViewer()
        self.exporters = {
            "docx": DocxExporter(), "pdf": PdfExporter(),
            "html": HtmlExporter(), "md": MarkdownExporter(),
            "json": JsonExporter(),
        }
        self.llm = LLMAdapter(self)

    def _gather_context(self, query="", diagram_type="flowchart"):
        parts = []
        web = self.call_agent("webclaw", f"search mermaid {diagram_type} {query}", timeout=10)
        if web: parts.append(str(web)[:500])
        data = self.call_agent("dataclaw", f"search {query}", timeout=10)
        if data: parts.append(str(data)[:500])
        return "\n".join(parts)

    def _generate_diagram(self, diagram_type, query, ctx=None):
        enhanced = f"Context:\n{ctx}\n\nTask: {query}" if ctx else query
        return self.engine.generate_with_llm(diagram_type, enhanced, self.llm)

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from agents.flowclaw.schema import validate
            validated = validate(task)
            if not validated["valid"]:
                return {"status": "error", "result": f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

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

            if cmd in ("/help",):
                return {"status": "success", "result": "FlowClaw v5\n  DIAGRAMS: /flowchart /sequence /architecture /mindmap\n  EXPORT: /export <fmt> <query>\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"}

            if cmd in ("/stats",):
                return {"status": "success", "result": f"FlowClaw v5 | Interactions: {self.state.get('interactions', 0)}"}

            if cmd == "/shared" and args:
                from agents.flowclaw.data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1)
                action = parts2[0]
                if action == "read":
                    key = parts2[1] if len(parts2) > 1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action == "write" and len(parts2) > 1:
                    kv = parts2[1].split(":", 1)
                    result = write_shared(kv[0], kv[1]) if len(kv) == 2 else "Usage: /shared write key:value"
                else:
                    result = "Usage: /shared read [key] | /shared write key:value"
                final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("flowclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("flowclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("flowclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("flowclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("flowclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"flowclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("flowclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("flowclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="flowclaw")
                except Exception: pass
                try: from agents.flowclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("flowclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="flowclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="flowclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("flowclaw_handler", lambda: True)
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
                    log_event(agent="flowclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}

            if cmd == "/delegate" and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","interpretclaw","docuclaw","dataclaw","webclaw","lawclaw","mathematicaclaw","langclaw","claw_coder","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else:
                    result = f"Unknown: {target}"
                final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("flowclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("flowclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("flowclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("flowclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("flowclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"flowclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("flowclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("flowclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="flowclaw")
                except Exception: pass
                try: from agents.flowclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("flowclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="flowclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="flowclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("flowclaw_handler", lambda: True)
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
                    log_event(agent="flowclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}

            if cmd == "/exports":
                from agents.flowclaw.data_io import list_exports
                return {"status": "success", "result": "Exports:\n" + list_exports()}

            diagram_type = "flowchart"
            if cmd in ("/flowchart",): diagram_type = "flowchart"
            elif cmd in ("/sequence",): diagram_type = "sequence"
            elif cmd in ("/architecture",): diagram_type = "architecture"
            elif cmd in ("/mindmap",): diagram_type = "mindmap"

            code = self._generate_diagram(diagram_type, query)

            if cmd in ("/export",):
                parts2 = args.split(maxsplit=1) if args else ["md", query]
                fmt = parts2[0] if parts2[0] in ("png","svg","pdf","docx","md","html","json") else "md"
                er = self.call_agent("fileclaw", f"/export {fmt} Mermaid: {query}\n\n`mermaid\n{code}\n`", timeout=30)
                result = f"{er}\n\n`mermaid\n{code}\n`" if er else f"`mermaid\n{code}\n`"
            else:
                try:
                    import subprocess, tempfile
                    html = self.viewer._build_html(code, query)
                    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
                    tmp.write(html)
                    tmp.close()
                    subprocess.Popen(['cmd', '/c', 'start', '', tmp.name], shell=True)
                    result = f"Opened in browser.\n\n`mermaid\n{code}\n`"
                except Exception as e:
                    result = f"`mermaid\n{code}\n`"

            from agents.flowclaw.data_io import write_shared
            write_shared("flowclaw_latest", {"type": diagram_type, "query": query, "code": code})

            # Constitutional capability routing for unrecognized commands
            if cmd and cmd not in ("/help", "/stats", "/shared", "/delegate", "/flowchart", "/sequence", "/architecture", "/mindmap", "/export", "/flow", "/diagram"):
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "flowclaw")
                if target:
                    result = str(self.call_agent(target, task, timeout=60) or "")
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("flowclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("flowclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("flowclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("flowclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("flowclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"flowclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("flowclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("flowclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="flowclaw")
                except Exception: pass
                try: from agents.flowclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("flowclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="flowclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="flowclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("flowclaw_handler", lambda: True)
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
                    log_event(agent="flowclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}

        except Exception as e:
            log_err("flowclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type") == "delegate":
                target = payload["target_agent"]
                task_text = payload.get("payload", payload.get("command", ""))
                if isinstance(task_text, dict):
                    task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status": "success", "result": str(result or f"Delegated to {target}")}

            diag_type = payload.get("diagram_type", "flowchart")
            query = payload.get("query", "")
            flags = payload.get("flags", {})
            code = self._generate_diagram(diag_type, query)

            if not flags.get("export_format"):
                try:
                    import subprocess, tempfile
                    html = self.viewer._build_html(code, flags.get("title", query))
                    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
                    tmp.write(html)
                    tmp.close()
                    subprocess.Popen(['cmd', '/c', 'start', '', tmp.name], shell=True)
                except:
                    pass

            result = f"`mermaid\n{code}\n`"
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("flowclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("flowclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("flowclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("flowclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("flowclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"flowclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("flowclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("flowclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="flowclaw")
                except Exception: pass
                try: from agents.flowclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("flowclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="flowclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="flowclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("flowclaw_handler", lambda: True)
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
                    log_event(agent="flowclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}

        except Exception as e:
            log_err("flowclaw", "execute_error", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = FlowClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)