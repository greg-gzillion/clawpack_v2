"""TxClaw LLM Agent - Blockchain transaction analysis and crypto education"""
from .. import get_llm

class TxClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def explain_transaction(self, tx_hash: str, details: str = "") -> str:
        """Explain a blockchain transaction in simple terms"""
        prompt = f"Explain this blockchain transaction in simple, non-technical terms:\nHash: {tx_hash}\nDetails: {details}"
        return self.llm.generate(prompt, task="general").text
    
    def analyze_smart_contract(self, contract_code: str, language: str = "Solidity") -> str:
        """Analyze smart contract for risks and functionality"""
        prompt = f"Analyze this {language} smart contract for:\n1. Functionality\n2. Security risks\n3. Gas optimization\n4. Best practices\n\nCode:\n{contract_code[:2000]}"
        return self.llm.generate(prompt, task="code").text
    
    def explain_defi(self, protocol: str, action: str) -> str:
        """Explain DeFi protocols and actions"""
        prompt = f"Explain how to {action} on {protocol} in DeFi. Include risks, rewards, and step-by-step process."
        return self.llm.generate(prompt, task="general").text
    
    def compare_chains(self, chain1: str, chain2: str, criteria: str = "all") -> str:
        """Compare blockchain networks"""
        prompt = f"Compare {chain1} vs {chain2} based on {criteria} (speed, cost, security, adoption, ecosystem)."
        return self.llm.generate(prompt, task="general").text
    
    def wallet_security(self, wallet_type: str) -> str:
        """Get wallet security best practices"""
        prompt = f"Provide security best practices for {wallet_type} wallets. Include backup, recovery, and threat prevention."
        return self.llm.generate(prompt, task="general").text
    
    def explain_tokenomics(self, token: str) -> str:
        """Explain tokenomics of a cryptocurrency"""
        prompt = f"Explain the tokenomics of {token}: supply, distribution, utility, inflation, and value drivers."
        return self.llm.generate(prompt, task="general").text
    
    def nft_guide(self, topic: str) -> str:
        """Guide for NFTs (creation, buying, selling)"""
        prompt = f"Provide a guide for {topic} with NFTs. Include steps, costs, platforms, and risks."
        return self.llm.generate(prompt, task="general").text
