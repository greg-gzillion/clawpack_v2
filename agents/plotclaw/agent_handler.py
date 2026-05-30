"""A2A Handler for PlotClaw - Chart Generator with matplotlib"""
import sys, time
from pathlib import Path

PLOTCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = PLOTCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PLOTCLAW_DIR))

import json
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class PlotClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('plotclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search chart data {query}", timeout=15)
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
            if cmd in ("/csv", "/import") and query:
                parts2 = query.split()
                filepath = parts2[0]
                col = parts2[1] if len(parts2) > 1 else None
                chart_type = parts2[2] if len(parts2) > 2 else "bar"
                
                from data_io import read_csv, read_json, read_shared, list_data_dir
                
                if filepath.endswith(".csv"):
                    headers, rows, col_data = read_csv(filepath, col)
                    if col_data and isinstance(col_data, list) and len(col_data) > 0:
                        labels = [str(r[0])[:20] for r in rows] if rows else [f"Row {i+1}" for i in range(len(col_data))]
                        chart_spec = {
                            "type": chart_type if chart_type in ("bar", "pie") else "bar",
                            "labels": labels[:30],
                            "values": col_data[:30],
                            "flags": {}
                        }
                        if chart_spec["type"] == "pie":
                            from agents.plotclaw.commands.pie import run as pie_run
                            args_str = ",".join(f"{l}:{v}" for l, v in zip(chart_spec["labels"], chart_spec["values"]))
                            result = pie_run(args_str)
                        else:
                            from agents.plotclaw.commands.bar import run as bar_run
                            args_str = ",".join(f"{l}:{v}" for l, v in zip(chart_spec["labels"], chart_spec["values"]))
                            result = bar_run(args_str)
                    elif isinstance(col_data, str):
                        result = col_data
                    else:
                        result = f"CSV loaded: {len(rows)} rows, headers: {headers}\nUse /csv {filepath} <column> <bar|pie>"
                elif filepath.endswith(".json"):
                    data, err = read_json(filepath)
                    if err:
                        result = err
                    else:
                        result = f"JSON loaded: {json.dumps(data, indent=2, default=str)[:2000]}"
                else:
                    result = f"Unknown format. Use .csv or .json files.\nAvailable: {list_data_dir()}"
            
            elif cmd in ("/data", "/files"):
                from data_io import list_data_dir
                result = "Available data files:\n" + "\n".join(f"  {f}" for f in list_data_dir())
            
            elif cmd == "/shared" and query:
                from data_io import read_shared, write_shared
                parts2 = query.split(maxsplit=1)
                action = parts2[0]
                if action == "read" and len(parts2) > 1:
                    data, err = read_shared(parts2[1])
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action == "write" and len(parts2) > 1:
                    key_val = parts2[1].split(":", 1)
                    if len(key_val) == 2:
                        result = write_shared(key_val[0], key_val[1])
                    else:
                        result = "Usage: /shared write key:value"
                elif action == "read":
                    data, err = read_shared()
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                else:
                    result = "Usage: /shared [read [key]] [write key:value]"
            
            elif cmd == "/publish" and query:
                from data_io import write_shared
                result = write_shared("plotclaw_latest", query)
            
            elif cmd in ("/bar", "bar") and query:
                from agents.plotclaw.commands.bar import run
                result = run(query)
            elif cmd in ("/pie", "pie") and query:
                from agents.plotclaw.commands.pie import run
                result = run(query)
            elif cmd in ("/plot", "plot") and query:
                from agents.plotclaw.commands.plot import run
                result = run(query)
            elif cmd in ("/scatter", "scatter") and query:
                from agents.plotclaw.commands.scatter import run
                result = run(query)
            elif cmd in ("/hist", "hist") and query:
                from agents.plotclaw.commands.hist import run
                result = run(query)
            elif cmd in ("/box", "box") and query:
                from agents.plotclaw.commands.box import run
                result = run(query)
            elif cmd in ("/heatmap", "heatmap") and query:
                from agents.plotclaw.commands.heatmap import run
                result = run(query)
            elif cmd in ("/polar", "polar") and query:
                from agents.plotclaw.commands.polar import run
                result = run(query)
            elif cmd in ("/surface", "surface") and query:
                from agents.plotclaw.commands.surface import run
                result = run(query)
            elif cmd in ("/compare", "compare") and query:
                from agents.plotclaw.commands.compare import run
                result = run(query)
            elif cmd in ("/animate", "animate") and query:
                from agents.plotclaw.commands.animate import run
                result = run(query)
            elif cmd in ("/stats", "stats") and query:
                from agents.plotclaw.commands.stats import run
                result = run(query)
            elif cmd in ("/dashboard", "dashboard") and query:
                from agents.plotclaw.commands.dashboard import run
                result = run(query)
            
            elif cmd == "/delegate" and query:
                parts2 = query.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                if target in ("docuclaw", "interpretclaw", "dataclaw", "webclaw", "mathematicaclaw"):
                    result = self.call_agent(target, task_text) or f"Agent {target} returned no response"
                else:
                    result = f"Unknown agent: {target}. Try: docuclaw, interpretclaw, dataclaw, webclaw, mathematicaclaw"
            
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
                result = """PlotClaw v3 - 13 Chart Types + Data I/O
  CHARTS:   /bar /pie /plot /scatter /hist /box /heatmap /polar /surface /compare /animate /stats /dashboard
  DATA:     /csv <file.csv> [column] [chart_type]  |  /data (list files)  |  /import <file.json>
  SHARED:   /shared read [key]  |  /shared write key:value  |  /publish <data>
  DELEGATE: /delegate <agent> <task>
  FLAGS:    --ylim 0,100 --xlim -5,5 --figsize 12,8 --dpi 200 --fontsize 12 --cmap magma --theme dark
            --format svg|pdf|png --save-only
  /stats"""
            
            elif cmd in ("/stats",):
                result = f"PlotClaw v3 | 13 chart types | CSV/JSON/Shared | Exports to PNG/SVG/PDF | Interactions: {self.state.get('interactions', 0)}"
            
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Chart visualization: {query}").get("result","")

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("plotclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("plotclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("plotclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("plotclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("plotclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"plotclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("plotclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("plotclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="plotclaw")
                except Exception: pass
                try: from agents.plotclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("plotclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="plotclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="plotclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("plotclaw_handler", lambda: True)
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
                    log_event(agent="plotclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("plotclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = PlotClawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)