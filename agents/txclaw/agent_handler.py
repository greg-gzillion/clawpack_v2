"""A2A Handler for TXClaw - TX.org Blockchain Agent"""
import sys
from pathlib import Path

TXCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TXCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from commands.llm_enhanced import run as llm_run

class TXClawA2AHandler(BaseAgent):
    def __init__(self):
        super().__init__('txclaw')
        self.session = {"queries": []}
        self.refs_dir = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/txclaw")
        self._load_references()

    def _load_references(self):
        self.refs_context = ""
        if self.refs_dir.exists():
            md_files = list(self.refs_dir.rglob("*.md"))[:10]
            for f in md_files:
                try:
                    self.refs_context += f"\n--- {f.name} ---\n{f.read_text(encoding='utf-8')[:800]}"
                except:
                    pass

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search TX.org blockchain {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        coder = self.call_agent("claw_coder", f"/explain {query}", timeout=15)
        if coder: parts.append("[ClawCoder]: " + coder[:600])
        return "\n".join(parts)

    def _call(self, prompt: str) -> str:
        full_prompt = f"""IDENTITY: You are a TX.org blockchain expert. TX.org is a Cosmos SDK blockchain - NOT Thorchain, NOT any other chain. TX.org is its own independent Layer 1 blockchain built with Cosmos SDK and CosmWasm.

REFERENCE KNOWLEDGE:
{self.refs_context[:2000]}

QUERY: {prompt}

IMPORTANT: Only reference TX.org blockchain. If you don't know, say "I don't have specific data on that for TX.org" rather than guessing or referencing other chains."""
        result = llm_run(full_prompt)
        self.session["queries"].append(prompt[:80])
        return result if result and "Error" not in result else "Error: No response from LLMClaw"

    def handle(self, task: str) -> dict:
        self.track_interaction()
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

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = TXClawA2AHandler()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
