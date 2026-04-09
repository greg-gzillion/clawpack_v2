"""Command Registry for TXclaw CLI"""

import sys
from pathlib import Path

# Add the root directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from core.commands import TXCommands

class CommandRegistry:
    """Registry of all available commands"""
    
    def __init__(self, commands: TXCommands):
        self.cmd = commands
        self.registry = {
            # Transaction commands
            "tx": self._tx,
            "block": self._block,
            "address": self._address,
            "token": self._token,
            # Staking commands
            "validator": self._validator,
            "staking": self._staking,
            "gas": self._gas,
            "mempool": self._mempool,
            # Contract commands
            "contract": self._contract,
            # Network commands
            "ecosystem": self._ecosystem,
            "gov": self._gov,
            "stats": self._network_stats,
        }
    
    def _tx(self, arg: str) -> str:
        if arg:
            return self.cmd.transaction(arg)
        return "Usage: /tx <transaction_hash>"
    
    def _block(self, arg: str) -> str:
        if arg:
            return self.cmd.block(arg)
        return "Usage: /block <block_height>"
    
    def _address(self, arg: str) -> str:
        if arg:
            return self.cmd.address(arg)
        return "Usage: /address <wallet_address>"
    
    def _token(self, arg: str) -> str:
        if arg:
            return self.cmd.token(arg)
        return "Usage: /token <token_id>"
    
    def _validator(self, arg: str) -> str:
        if arg:
            return self.cmd.validator(arg)
        return "Usage: /validator <validator_address>"
    
    def _staking(self, arg: str = "") -> str:
        return self.cmd.staking()
    
    def _gas(self, arg: str = "") -> str:
        return self.cmd.gas()
    
    def _mempool(self, arg: str = "") -> str:
        return self.cmd.mempool()
    
    def _contract(self, arg: str) -> str:
        if arg:
            return self.cmd.smart_contract(arg)
        return "Usage: /contract <contract_address>"
    
    def _ecosystem(self, arg: str = "") -> str:
        return self.cmd.ecosystem()
    
    def _gov(self, arg: str) -> str:
        return self.cmd.governance(arg if arg else None)
    
    def _network_stats(self, arg: str = "") -> str:
        return self.cmd.network_stats()
    
    def get_handler(self, cmd: str):
        """Get handler function for command"""
        return self.registry.get(cmd.lower())
    
    def list_commands(self) -> list:
        """List all available commands"""
        return sorted(self.registry.keys())
