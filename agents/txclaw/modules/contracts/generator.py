"""Contract Generator - CosmWasm smart contract generation"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))
# LLMClaw handles all LLM via A2A

class ContractGenerator:
    def __init__(self):
        pass  # LLMClaw via A2A
        self.output_dir = Path(__file__).resolve().parent.parent.parent / "contracts"

    def generate_cosmwasm(self, name: str, spec: str = "") -> dict:
        prompt = f"Generate a complete CosmWasm smart contract named '{name}' for the TX.org blockchain in Rust."
        if spec: prompt += f"\n\nSpecification: {spec}"
        prompt += "\n\nInclude: contract.rs, msg.rs, state.rs, error.rs, lib.rs, Cargo.toml. Use best practices."
        result = # _llm(prompt)
        if result and "Error" not in result:
            return {"success": True, "path": f"contracts/{name}", "code": result}
        return {"success": False, "error": str(result)}

    def list_contracts(self) -> list:
        if self.output_dir.exists():
            return [d.name for d in self.output_dir.iterdir() if d.is_dir()]
        return []
