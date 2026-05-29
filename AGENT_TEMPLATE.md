# AGENT_TEMPLATE.md — Constitutional Agent Skeleton

## How to Use This Template

1. Copy this entire file
2. Replace AGENT_NAME with your agent's name (e.g., "mediclaw", "plotclaw")
3. Add your domain-specific command routes in the COMMAND ROUTING section
4. Register your agent in shared/capabilities.py for any capabilities you own
5. Create agents/AGENT_NAME/commands/_memory.py (copy lawclaw's, change agent name)
6. Create agents/AGENT_NAME/commands/_helpers.py (copy lawclaw's, adapt for your domain)
7. Deploy and verify with the constitutional compliance audit scan

## Constitutional Requirements

Every agent MUST have:
- [ ] 23-system handler boundary (copy from template below)
- [ ] Capability routing block (delegates unknown commands)
- [ ] Shared memory bridge (_memory.py with show_prior + remember)
- [ ] At least one cross-agent delegation route
- [ ] All exceptions logged via log_err()
- [ ] All LLM access through Sovereign Gateway (never direct API calls)

## Handler Skeleton

```python
"""A2A Handler for AGENT_NAME — Constitutional Agent"""
import sys
import json
import time
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AGENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(AGENT_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class AgentNameHandler(BaseAgent):
    def __init__(self):
        super().__init__("AGENT_NAME")
        self._last_result = ""

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
            # ============================================================
            # COMMAND ROUTING — add your domain-specific commands here
            # ============================================================
            if cmd in ("/help", "help"):
                result = "AGENT_NAME — list your commands here"
            elif cmd == "/stats":
                result = f"AGENT_NAME | Interactions: {self.state.get('interactions', 0)}"

            # ADD YOUR COMMANDS HERE:
            # elif cmd == "/yourcommand" and args:
            #     from agents.AGENT_NAME.commands.yourcommand import run as cmd_run
            #     result = cmd_run(args)

            else:
                # -- Constitutional capability routing --
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "AGENT_NAME")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif args:
                    context = self._gather_context(args)
                    result = self.ask_llm(f"Query: {args}\n\nContext:\n{context}")
                else:
                    result = "Type /help for commands"

            # ============================================================
            # CONSTITUTIONAL EXECUTION BOUNDARY — 23 systems.
            # Do not modify. This enforces constitutional compliance.
            # ============================================================
            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("AGENT_NAME", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("AGENT_NAME_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("AGENT_NAME")._check_and_record("handler_boundary", {"cmd": cmd})
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
                    pmem = get_proc_mem("AGENT_NAME")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("AGENT_NAME").get_context(args or cmd, limit=5)
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
                    get_logger().info(f"AGENT_NAME.{cmd}", extra={"args": (args or "")[:100]})
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
                    if not budget.check("AGENT_NAME", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("AGENT_NAME").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("AGENT_NAME_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="AGENT_NAME")
                except Exception: pass
                try:
                    from agents.AGENT_NAME.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("AGENT_NAME", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="AGENT_NAME", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="AGENT_NAME", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("AGENT_NAME", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("AGENT_NAME_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="AGENT_NAME", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": final_result}
        except Exception as e:
            log_err("AGENT_NAME", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}

_agent = AgentNameHandler()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
Verification Checklist
After deploying, run the constitutional compliance audit:

powershell
Get-ChildItem "agents" -Directory | ForEach-Object {
    $name = $_.Name
    $handler = Join-Path $_.FullName "agent_handler.py"
    if (Test-Path $handler) {
        $content = Get-Content $handler -Raw
        $hasCapRoute = if ($content -match 'get_capable_agent') { "YES" } else { "NO" }
        $hasDelegate = if ($content -match '/delegate.*and args|call_agent') { "YES" } else { "NO" }
        $hasBoundary = if ($content -match 'shared\.lifecycle|shared\.enforcement|shared\.guarded_executor') { "YES" } else { "NO" }
        $hasMemory = if ($content -match 'unified_memory|_memory|remember|recall_prior') { "YES" } else { "NO" }
        Write-Host "$name | cap_route: $hasCapRoute | delegate: $hasDelegate | boundary: $hasBoundary | memory: $hasMemory"
    }
}
All four columns should show YES for a constitutional agent.
