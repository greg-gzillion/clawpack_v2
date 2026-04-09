"""TXclaw - TX Blockchain agent"""

import sys
from pathlib import Path
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.agent import BaseAgent
from shared.loop import ToolSafety
from shared.memory import MemoryType


class TXclawAgent(BaseAgent):
    """TX Blockchain AI agent"""
    
    def __init__(self, project_root: Optional[Path] = None):
        super().__init__("TXclaw", project_root)
        self.network = "mainnet"
    
    def _register_tools(self):
        """Register blockchain tools"""
        self.register_tool("get_balance", self.get_balance, ToolSafety.READ_ONLY)
        self.register_tool("send_transaction", self.send_transaction, ToolSafety.DESTRUCTIVE)
        self.register_tool("get_transaction", self.get_transaction, ToolSafety.READ_ONLY)
        self.register_tool("get_block", self.get_block, ToolSafety.READ_ONLY)
        self.register_tool("get_gas_price", self.get_gas_price, ToolSafety.READ_ONLY)
        self.register_tool("switch_network", self.switch_network, ToolSafety.WRITE)
    
    def get_balance(self, address: str) -> Dict:
        """Get wallet balance for address"""
        # Placeholder - would call blockchain RPC
        return {
            "address": address,
            "balance": 100.5,
            "network": self.network,
            "currency": "TX"
        }
    
    def send_transaction(self, to: str, amount: float, token: str = "TX") -> Dict:
        """
        Send blockchain transaction.
        DESTRUCTIVE - requires explicit user confirmation.
        """
        # This would actually send a transaction
        tx_hash = f"0x{hash(f'{to}{amount}') % 10**16:016x}"
        
        # Record in memory
        self.remember(
            MemoryType.FEEDBACK,
            f"TX: {amount} {token} to {to[:8]}...",
            f"Sent {amount} {token}",
            f"To: {to}\nAmount: {amount} {token}\nHash: {tx_hash}"
        )
        
        return {
            "to": to,
            "amount": amount,
            "token": token,
            "tx_hash": tx_hash,
            "network": self.network,
            "status": "pending"
        }
    
    def get_transaction(self, tx_hash: str) -> Dict:
        """Get transaction details by hash"""
        return {
            "tx_hash": tx_hash,
            "status": "confirmed",
            "confirmations": 12,
            "network": self.network
        }
    
    def get_block(self, block_number: Optional[int] = None) -> Dict:
        """Get block information"""
        return {
            "block_number": block_number or "latest",
            "transactions": 150,
            "timestamp": "2026-04-09T00:00:00Z",
            "network": self.network
        }
    
    def get_gas_price(self) -> Dict:
        """Get current gas price"""
        return {
            "gas_price": 0.001,
            "unit": "TX",
            "network": self.network
        }
    
    def switch_network(self, network: str) -> Dict:
        """Switch between mainnet and testnet"""
        if network in ["mainnet", "testnet"]:
            self.network = network
            return {"network": network, "switched": True}
        return {"error": f"Unknown network: {network}"}


# Register the agent
from shared.agent import ClawpackAgentRegistry
ClawpackAgentRegistry.register("txclaw", TXclawAgent)
