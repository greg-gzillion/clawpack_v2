"""Network Handler - TX.org network configuration"""
class NetworkHandler:
    def __init__(self):
        self.networks = {
            "mainnet": {"chain_id": "txorg-1", "rpc": "https://rpc.tx.org", "api": "https://api.tx.org"},
            "testnet": {"chain_id": "txorg-testnet-1", "rpc": "https://rpc.testnet.tx.org", "api": "https://api.testnet.tx.org"},
            "local": {"chain_id": "txorg-local", "rpc": "http://localhost:26657", "api": "http://localhost:1317"},
        }

    def list_networks(self) -> list:
        return list(self.networks.keys())

    def get_network(self, name: str) -> dict:
        return self.networks.get(name, self.networks["testnet"])

    def setup_test_env(self) -> str:
        return """Test environment setup for TX.org:
1. Install txclawd: git clone https://github.com/txorg/txclaw && cd txclaw && make install
2. Initialize: txclawd init test-node --chain-id txorg-local
3. Add keys: txclawd keys add test-validator
4. Start: txclawd start
5. Faucet: Request test tokens from https://faucet.testnet.tx.org"""
