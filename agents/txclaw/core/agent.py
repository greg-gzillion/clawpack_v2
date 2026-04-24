"""TXclaw Agent - Core"""
import sys
from pathlib import Path

# Robust path to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.llm_manager import LLMManager

class TXclawAgent:
    def __init__(self):
        self.llm = LLMManager()
        self.network = "mainnet"
        self.session = {"queries": []}

    def _call(self, prompt: str) -> str:
        result = self.llm.chat_sync(prompt)
        self.session["queries"].append(prompt[:80])
        return result if result and "Error" not in result else "Error: No response from LLM"

    def get_balance(self, address: str = None):
        return {"balance": 100.0, "network": self.network}

    def send_transaction(self, to: str, amount: float):
        return {"tx_hash": "0x" + "1" * 64, "status": "pending"}

    def get_stats(self):
        return {"queries": len(self.session["queries"])}
