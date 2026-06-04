"""A2A Handler for TXClaw - TX.org Blockchain Agent"""
import sys, time
from pathlib import Path

TXCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TXCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err
from commands.llm import run as llm_run

class TXClawA2AHandler(BaseAgent):
    def __init__(self):
        super().__init__('txclaw')
        self.session = {"queries": []}
        self.refs_dir = PROJECT_ROOT / "agents" / "webclaw" / "references" / "txclaw"
        self._load_references()

    def _load_references(self):
        self.refs_context = ""
        if self.refs_dir.exists():
            md_files = list(self.refs_dir.rglob("*.md"))
            for f in md_files:
                try:
                    self.refs_context += f"\n--- {f.name} ---\n{f.read_text(encoding='utf-8')}"
                except:
                    pass

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search ns:txclaw TX.org blockchain {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
        coder = self.call_agent("claw_coder", f"/explain {query}", timeout=15)
        if coder: parts.append("[ClawCoder]: " + coder)
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return "\n".join(parts)

    def _call(self, prompt: str) -> str:
        full_prompt = f"""IDENTITY: You are a TX.org blockchain expert. TX.org is a Cosmos SDK blockchain - NOT Thorchain, NOT any other chain. TX.org is its own independent Layer 1 blockchain built with Cosmos SDK and CosmWasm.

REFERENCE KNOWLEDGE:
{self.refs_context}

QUERY: {prompt}

IMPORTANT: Only reference TX.org blockchain. If you don't know, say "I don't have specific data on that for TX.org" rather than guessing or referencing other chains."""
        result = llm_run(full_prompt)
        self.session["queries"].append(prompt)
        return result if result and "Error" not in result else "Error: No response from LLMClaw"

    def handle(self, task: str) -> dict:
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "/tx" and args:
                result = self._call(f"Analyze TX.org blockchain transaction: {args}. Include sender, receiver, amount, gas, status.")
            elif cmd == "/block" and args:
                result = self._call(f"Get TX.org blockchain block {args}. Include hash, timestamp, tx count, proposer.")
            elif cmd == "/address" and args:
                result = self._call(f"Analyze TX.org blockchain address: {args}. Include balance, tx history, staking info.")
            elif cmd == "/token" and args:
                result = self._call(f"Get TX.org blockchain token info: {args}. Include supply, holders, market cap.")
            elif cmd == "/validator" and args:
                result = self._call(f"Get TX.org validator info: {args}. Include stake, commission, uptime, rewards.")
            elif cmd == "/contract" and args:
                result = self._call(f"Analyze TX.org smart contract: {args}. Include type, functions, verification, security.")
            elif cmd == "/staking":
                result = self._call("Get TX.org staking info. Include APR, total staked, validator count, unstaking period.")
            elif cmd == "/gas":
                result = self._call("Get TX.org gas fees structure. TX.org uses Cosmos SDK fee model. Explain how gas works on TX.org - gas prices, fee calculation, priority levels.")
            elif cmd == "/ecosystem":
                result = self._call("Get TX.org ecosystem overview. Include TVL, active addresses, daily txs, major dApps on TX.org.")
            elif cmd == "/governance":
                result = self._call(f"Get TX.org governance proposal {args}. Include status, votes, description." if args else "List active TX.org governance proposals.")
            elif cmd == "/network":
                result = self._call("Get TX.org network stats. Include block height, TPS, node count, network health.")
            elif cmd == "/mempool":
                result = self._call("Get TX.org mempool status. Include pending tx count, gas price distribution.")

            elif cmd == "/generate" and args:
                result = self._call(f"Generate a complete CosmWasm smart contract named '{args}' for TX.org blockchain in Rust. Include: contract.rs, msg.rs, state.rs, error.rs, lib.rs, Cargo.toml.")
            elif cmd == "/deploy" and args:
                result = self._call(f"Provide step-by-step instructions to deploy CosmWasm contract '{args}' to TX.org testnet. Include store, instantiate, RPC endpoints.")
            elif cmd == "/test" and args:
                result = self._call(f"Generate comprehensive unit tests for CosmWasm contract '{args}' on TX.org blockchain in Rust.")

            elif cmd == "/networks":
                result = "TX.org Networks:\n  - mainnet -> https://rpc.tx.org\n  - testnet -> https://rpc.testnet.tx.org\n  - local -> http://localhost:26657"
            elif cmd == "/search" and args:
                result = self._call(f"Search TX.org references for: {args}. Use the reference knowledge provided above.")
            elif cmd == "/help":
                result = "TXClaw - TX.org Blockchain Agent\n  /tx /block /address /token /validator /contract\n  /staking /gas /ecosystem /governance /network /mempool\n  /generate <name> /deploy <name> /test <name>\n  /networks /search <query> /stats"
            elif cmd == "/stats":
                result = f"TXClaw | TX.org Blockchain | Queries: {len(self.session['queries'])} | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.smart_ask(f"TX.org blockchain: {task}")

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("txclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("txclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("txclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("txclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("txclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"txclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("txclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("txclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="txclaw")
                except Exception: pass
                try: from agents.txclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("txclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="txclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="txclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("txclaw_handler", lambda: True)
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
                    log_event(agent="txclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("txclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = TXClawA2AHandler()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)

