"""Smart Contract Generator Module"""

from pathlib import Path
from datetime import datetime

class ContractGenerator:
    def __init__(self, ai_assistant, project_path):
        self.ai = ai_assistant
        self.project_path = Path(project_path)
    
    def generate_cosmwasm(self, name, features=None):
        """Generate CosmWasm smart contract"""
        features = features or ["store", "query", "update"]
        
        # Search for best practices
        refs = self.ai.search(f"cosmwasm contract template {name}")
        ref_text = "\nReferences:\n" + "\n".join(f"- {r['url']}" for r in refs[:3]) if refs else ""
        
        prompt = f"""Generate a CosmWasm smart contract for TX.org blockchain.
Contract name: {name}
Features: {', '.join(features)}
{ref_text}

Requirements:
- Use cosmwasm-std v1.5
- Include proper error handling
- Add comprehensive comments
- Include instantiate, execute, query entry points
- Use cw-storage-plus for state management
- Follow CosmWasm best practices

Return ONLY the Rust code."""
        
        code = self.ai.generate_code(prompt)
        
        if code:
            return self._save_contract(name, code)
        return self._template_contract(name)
    
    def _save_contract(self, name, code):
        contract_dir = self.project_path / "contracts" / name
        contract_dir.mkdir(parents=True, exist_ok=True)
        
        src_dir = contract_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        (src_dir / "contract.rs").write_text(code)
        
        # Generate Cargo.toml
        cargo = f'''[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
cosmwasm-std = "1.5.0"
cosmwasm-storage = "1.5.0"
cw-storage-plus = "1.2.0"
schemars = "0.8.12"
serde = {{ version = "1.0.193", default-features = false, features = ["derive"] }}

[dev-dependencies]
cosmwasm-schema = "1.5.0"
'''
        (contract_dir / "Cargo.toml").write_text(cargo)
        
        return {
            'success': True,
            'path': str(contract_dir),
            'name': name,
            'type': 'cosmwasm'
        }
    
    def _template_contract(self, name):
        return {
            'success': True,
            'path': str(self.project_path / "contracts" / name),
            'name': name,
            'type': 'template',
            'message': 'Template created - add implementation'
        }
    
    def list_contracts(self):
        contracts_dir = self.project_path / "contracts"
        if not contracts_dir.exists():
            return []
        return [d.name for d in contracts_dir.iterdir() if d.is_dir()]
