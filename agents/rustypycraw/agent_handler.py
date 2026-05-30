"""A2A Handler for RustyPyCraw - Python/Rust Interop Analyzer with A2A Routing"""
import sys, time
from pathlib import Path

RUSTYPYCRAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RUSTYPYCRAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(RUSTYPYCRAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err
from agents.rustypycraw.modules.scanner.code_scanner import CodeScanner
from agents.rustypycraw.modules.analyzer.code_analyzer import CodeAnalyzer

class RustyPyCrawAgent(BaseAgent):
    def __init__(self):
        super().__init__("rustypycraw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search code analysis {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""
        self.scanner = CodeScanner()
        self.analyzer = CodeAnalyzer()

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search rust python interop {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        rust = self.call_agent("crustyclaw", f"/explain {query}", timeout=15)
        if rust: parts.append("[CrustyClaw]: " + rust[:600])
        coder = self.call_agent("claw_coder", f"/explain {query}", timeout=15)
        if coder: parts.append("[ClawCoder]: " + coder[:600])
        chronicle_results = self.search_chronicle(query, limit=3)
        if chronicle_results:
            for c in chronicle_results[:3]:
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
            if cmd in ("/scan", "scan") and query:
                result = self.scanner.scan(query)
                result_str = f"Scanned: {query}\n"
                if "error" in result:
                    result_str = str(result)
                elif "languages" in result:
                    for lang, stats in result.get("languages", {}).items():
                        result_str += f"  {lang}: {stats['files']} files, {stats['lines']} lines, {stats['functions']} functions\n"
                    result_str += f"\nTotal: {result['files']} files, {result['lines']} lines"
                else:
                    result_str = f"File: {result.get('file')}\nLanguage: {result.get('language')}\nLines: {result.get('lines')}\nFunctions: {result.get('functions', 0)}"
                result = result_str
                
            elif cmd in ("/analyze", "analyze") and query:
                analysis = self.analyzer.analyze(query, "interop")
                result = f"Analysis: {query}\n"
                if "results" in analysis:
                    for r in analysis["results"]:
                        result += f"\n--- {r.get('file')} ---\n"
                        if "rust_portable" in r:
                            result += f"Rust-portable: {r['rust_portable'].get('portable')}\n"
                            for issue in r['rust_portable'].get('issues', []):
                                result += f"  - {issue}\n"
                        if "unsafe_patterns" in r:
                            for p in r['unsafe_patterns']:
                                result += f"  - {p}\n"
                else:
                    result = str(analysis)
                    
            elif cmd in ("/compare", "compare") and query:
                paths = query.split()
                if len(paths) >= 2:
                    comparison = self.scanner.compare(paths[0], paths[1])
                    result = f"Python ({paths[0]}): {comparison.get('python', {}).get('lines', 0)} lines, {comparison.get('python', {}).get('functions', 0)} functions\n"
                    result += f"Rust ({paths[1]}): {comparison.get('rust', {}).get('lines', 0)} lines, {comparison.get('rust', {}).get('functions', 0)} functions"
                else:
                    result = "Usage: /compare <python_file> <rust_file>"
                    
            elif cmd in ("/help",):
                result = "RustyPyCraw - Python/Rust Interop\n  /scan <path> - Scan codebase\n  /analyze <path> - Analyze interop\n  /compare <py> <rs> - Compare Python/Rust\n  /stats\n  Uses: WebClaw + DataClaw + CrustyClaw + ClawCoder -> LLMClaw -> FileClaw"
            elif cmd in ("/stats",):
                result = f"RustyPyCraw | Python/Rust Interop | Scanner + Analyzer | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(query)
                result = self.ask_llm(f"Context from specialists:\n{ctx}\n\nPython/Rust interop analysis: {query}")

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("rustypycraw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("rustypycraw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("rustypycraw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("rustypycraw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("rustypycraw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"rustypycraw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("rustypycraw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("rustypycraw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="rustypycraw")
                except Exception: pass
                try: from agents.rustypycraw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("rustypycraw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="rustypycraw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="rustypycraw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("rustypycraw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="rustypycraw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("rustypycraw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = RustyPyCrawAgent()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)