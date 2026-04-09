"""TXclaw Agent - Standalone"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TXclawAgent:
    def __init__(self):
        self.network = "mainnet"
        self.session = {"queries": []}
    
    def get_balance(self, address: str = None):
        return {"balance": 100.0, "network": self.network}
    
    def send_transaction(self, to: str, amount: float):
        return {"tx_hash": "0x" + "1" * 64, "status": "pending"}
    
    def get_stats(self):
        return {"queries": len(self.session["queries"])}
