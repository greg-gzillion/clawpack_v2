"""Test Generator - Generate tests for CosmWasm contracts"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))
# LLMClaw handles all LLM via A2A

class TestGenerator:
    def __init__(self):
        pass  # LLMClaw via A2A

    def generate_tests(self, name: str, spec: str = "") -> dict:
        prompt = f"Generate comprehensive unit tests for CosmWasm contract '{name}' on TX.org blockchain in Rust."
        if spec: prompt += f"\n\nContract spec: {spec}"
        prompt += "\n\nInclude: instantiate tests, execute tests, query tests, error cases, migration tests. Use cosmwasm-std testing utilities."
        result = # _llm(prompt)
        if result and "Error" not in result:
            return {"success": True, "tests": result}
        return {"success": False, "error": str(result)}

    def run_tests(self, name: str) -> dict:
        return {"success": True, "command": f"cd contracts/{name} && cargo test", "output": "Run 'cargo test' in the contract directory to execute tests"}
