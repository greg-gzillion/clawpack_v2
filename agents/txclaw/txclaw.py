#!/usr/bin/env python3
"""TXClaw - Modular Blockchain Development Assistant"""

import sys
from pathlib import Path

# Add clawpack_v2 to path
CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

# Now import modules
from modules.ai.assistant import TXAIAssistant
from modules.contracts.generator import ContractGenerator
from modules.tests.generator import TestGenerator
from modules.deploy.handler import DeployHandler
from modules.network.handler import NetworkHandler
from modules.references.handler import ReferenceHandler

class TXClaw:
    def __init__(self, project_path=None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.ai = TXAIAssistant()
        self.contracts = ContractGenerator(self.ai, self.project_path)
        self.tests = TestGenerator(self.ai, self.project_path)
        self.deploy = DeployHandler(self.project_path)
        self.network = NetworkHandler(self.project_path)
        self.references = ReferenceHandler(self.ai)
    
    def create(self, name, contract_type="cosmwasm"):
        """Create a new smart contract"""
        if contract_type == "cosmwasm":
            return self.contracts.generate_cosmwasm(name)
        return {'error': f'Unknown type: {contract_type}'}
    
    def test(self, contract_name):
        """Generate and run tests"""
        result = self.tests.generate_tests(contract_name)
        if result.get('success'):
            return self.tests.run_tests(contract_name)
        return result
    
    def deploy(self, contract_name, network="testnet"):
        """Deploy contract to network"""
        build = self.deploy.build_wasm(contract_name)
        if not build.get('success'):
            return build
        return self.deploy.deploy_to_tx(contract_name, network)
    
    def search(self, query):
        """Search chronicle for references"""
        results = self.references.search(query)
        return self.references.format_references(results)
    
    def docs(self, topic):
        """Get documentation links - uses search"""
        # Use search to find docs
        results = self.references.search(topic, 5)
        if not results:
            # Try with common prefixes
            for prefix in ["cosmwasm", "tx.org", "rust"]:
                results = self.references.search(f"{prefix} {topic}", 3)
                if results:
                    break
        
        if not results:
            return f"No documentation found for '{topic}'. Try: search {topic}"
        
        output = f"📚 Documentation for '{topic}':\n"
        for i, ref in enumerate(results[:5], 1):
            output += f"{i}. {ref['url']}\n"
        return output
    
    def networks(self):
        """List available networks"""
        nets = self.network.list_networks()
        return "🌐 Available Networks:\n" + "\n".join(f"  • {n}" for n in nets)
    
    def setup(self):
        """Setup test environment"""
        return self.network.setup_test_env()
    
    def status(self):
        """Show TXClaw status"""
        llm_status = "✅" if self.ai.is_available() else "❌"
        chronicle_status = "✅" if self.ai.chronicle else "❌"
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                        TXCLAW STATUS                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🤖 LLM: {llm_status} Connected                                          ║
║  📚 Chronicle: {chronicle_status} Connected                       ║
║  📁 Project: {self.project_path}                                    ║
║  📦 Contracts: {len(self.contracts.list_contracts())}                                   ║
║  🌐 Networks: {len(self.network.list_networks())}                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════════╗
║                    TXCLAW - Blockchain Assistant                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    create <name>           - Create a CosmWasm contract         ║
║    test <contract>         - Generate and run tests             ║
║    deploy <contract>       - Deploy to testnet                  ║
║    search <query>          - Search chronicle for resources     ║
║    docs <topic>            - Get documentation links            ║
║    networks                - List available networks            ║
║    setup                   - Setup local test environment       ║
║    status                  - Show TXClaw status                 ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    python txclaw.py create my_auction                           ║
║    python txclaw.py search "cosmwasm"                           ║
║    python txclaw.py docs "auction"                              ║
║    python txclaw.py status                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""

def main():
    agent = TXClaw()
    
    if len(sys.argv) < 2:
        print(agent.help())
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "create" and args:
        result = agent.create(args[0])
        if result.get('success'):
            print(f"✅ Contract created at: {result['path']}")
        else:
            print(f"❌ {result.get('error', 'Creation failed')}")
    
    elif cmd == "test" and args:
        result = agent.test(args[0])
        if result.get('success'):
            print("✅ Tests passed!")
            if result.get('output'):
                print(result['output'][:500])
        else:
            print(f"❌ Tests failed: {result.get('error', 'Unknown error')}")
    
    elif cmd == "deploy" and args:
        network = args[1] if len(args) > 1 else "testnet"
        result = agent.deploy(args[0], network)
        print(f"📦 Deployment result: {result}")
    
    elif cmd == "search" and args:
        print(agent.search(' '.join(args)))
    
    elif cmd == "docs" and args:
        print(agent.docs(' '.join(args)))
    
    elif cmd == "networks":
        print(agent.networks())
    
    elif cmd == "setup":
        print(agent.setup())
    
    elif cmd == "status":
        print(agent.status())
    
    else:
        print(agent.help())

if __name__ == "__main__":
    main()
