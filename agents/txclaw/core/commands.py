"""TX Blockchain Specific Commands"""

import sys
from pathlib import Path

# Add the root directory to path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from core.agent import TXclawAgent

class TXCommands:
    """TX blockchain command handlers"""
    
    def __init__(self, agent: TXclawAgent):
        self.agent = agent
    
    def transaction(self, tx_hash: str) -> str:
        """Analyze a TX blockchain transaction"""
        prompt = f"Analyze TX blockchain transaction: {tx_hash}. Include sender, receiver, amount, gas fees, status, and confirmations. TX.org is the blockchain."
        return self.agent._call(prompt)
    
    def block(self, block_height: str) -> str:
        """Get TX block information"""
        prompt = f"Get information about TX blockchain block {block_height}. Include block hash, timestamp, transaction count, miner, and block reward."
        return self.agent._call(prompt)
    
    def address(self, address: str) -> str:
        """Analyze TX blockchain address"""
        prompt = f"Analyze TX blockchain address: {address}. Include balance, transaction history, token holdings, and staking info."
        return self.agent._call(prompt)
    
    def token(self, token_id: str) -> str:
        """Get TX token information"""
        prompt = f"Get information about TX blockchain token: {token_id}. Include supply, holders, market cap, and transfer history."
        return self.agent._call(prompt)
    
    def validator(self, validator_addr: str) -> str:
        """Get TX validator information"""
        prompt = f"Get information about TX blockchain validator: {validator_addr}. Include staking amount, commission, uptime, and rewards."
        return self.agent._call(prompt)
    
    def staking(self) -> str:
        """Get TX staking information"""
        prompt = "Get TX blockchain staking information. Include APR, total staked, validator count, and unstaking period."
        return self.agent._call(prompt)
    
    def gas(self) -> str:
        """Get current TX gas fees"""
        prompt = "Get current TX blockchain gas fees. Include low, average, and high priority prices in TX tokens and USD."
        return self.agent._call(prompt)
    
    def mempool(self) -> str:
        """Get TX mempool status"""
        prompt = "Get TX blockchain mempool status. Include pending transactions count and gas price distribution."
        return self.agent._call(prompt)
    
    def smart_contract(self, contract_addr: str) -> str:
        """Analyze TX smart contract"""
        prompt = f"Analyze TX blockchain smart contract at {contract_addr}. Include contract type, functions, verification status, and security score."
        return self.agent._call(prompt)
    
    def ecosystem(self) -> str:
        """Get TX ecosystem overview"""
        prompt = "Get TX blockchain ecosystem overview. Include TVL, active addresses, daily transactions, and major dApps on TX.org."
        return self.agent._call(prompt)
    
    def governance(self, proposal_id: str = None) -> str:
        """Get TX governance information"""
        if proposal_id:
            prompt = f"Get information about TX blockchain governance proposal {proposal_id}. Include status, votes, and description."
        else:
            prompt = "Get list of active TX blockchain governance proposals from TX.org."
        return self.agent._call(prompt)
    
    def network_stats(self) -> str:
        """Get TX network statistics"""
        prompt = "Get TX blockchain network statistics. Include block height, TPS, node count, and network health."
        return self.agent._call(prompt)
