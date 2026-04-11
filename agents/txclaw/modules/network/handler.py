"""Network Configuration Module for TX.org"""

import json
from pathlib import Path

class NetworkHandler:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.networks_file = self.project_path / ".txclaw" / "networks.json"
        self.networks_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_networks()
    
    def _load_networks(self):
        if self.networks_file.exists():
            self.networks = json.loads(self.networks_file.read_text())
        else:
            self.networks = {
                "testnet": {
                    "rpc": "https://rpc.testnet.tx.org",
                    "rest": "https://rest.testnet.tx.org",
                    "chain_id": "tx-testnet-1",
                    "fee_denom": "utx",
                    "gas_price": "0.025"
                },
                "mainnet": {
                    "rpc": "https://rpc.tx.org",
                    "rest": "https://rest.tx.org",
                    "chain_id": "tx-mainnet-1",
                    "fee_denom": "utx",
                    "gas_price": "0.025"
                },
                "local": {
                    "rpc": "http://localhost:26657",
                    "rest": "http://localhost:1317",
                    "chain_id": "tx-local",
                    "fee_denom": "utx",
                    "gas_price": "0.025"
                }
            }
            self.save()
    
    def save(self):
        self.networks_file.write_text(json.dumps(self.networks, indent=2))
    
    def get_network(self, name):
        return self.networks.get(name, self.networks['testnet'])
    
    def add_network(self, name, config):
        self.networks[name] = config
        self.save()
        return True
    
    def list_networks(self):
        return list(self.networks.keys())
    
    def setup_test_env(self):
        """Setup local test environment"""
        instructions = """
🔧 TX.org Test Environment Setup:

1. Install LocalTX (local blockchain):
   git clone https://github.com/tx-foundation/localtx
   cd localtx
   make install

2. Start local node:
   localtx start

3. Configure your contract to use local network:
   --network local

4. Deploy and test:
   txclaw deploy mycontract --network local
"""
        return instructions
