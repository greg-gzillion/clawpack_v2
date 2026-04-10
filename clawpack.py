#!/usr/bin/env python3
"""CLAWPACK - Modular Agent System"""
import sys
import subprocess
from pathlib import Path

# Import all route modules
sys.path.insert(0, str(Path(__file__).parent))

from routes.math_routes import MathRoutes
from routes.web_routes import WebRoutes
from routes.translation_routes import TranslationRoutes
from routes.legal_routes import LegalRoutes
from routes.medical_routes import MedicalRoutes
from routes.code_routes import CodeRoutes
from routes.data_routes import DataRoutes
from routes.document_routes import DocumentRoutes
from routes.language_routes import LanguageRoutes
from routes.blockchain_routes import BlockchainRoutes
from routes.fork_routes import ForkRoutes
from routes.voice_routes import VoiceRoutes

class Clawpack:
    def __init__(self):
        # Build command map from all routes
        self.command_map = {}
        self.help_text = ""
        
        for route in [MathRoutes, WebRoutes, TranslationRoutes, LegalRoutes,
                      MedicalRoutes, CodeRoutes, DataRoutes, DocumentRoutes,
                      LanguageRoutes, BlockchainRoutes, ForkRoutes, VoiceRoutes]:
            for cmd in route.commands:
                self.command_map[cmd] = route.agent
            self.help_text += route.get_help()
        
        # Cache agent instances
        self.agent_instances = {}
        
        print("\n" + "="*50)
        print("🦞 CLAWPACK v2 - Agentic System")
        print("="*50)
        print(self.help_text)
        print("\nType /help for all commands, /quit to exit")
    
    def get_agent_instance(self, agent_name):
        """Get or create an agent instance"""
        if agent_name in self.agent_instances:
            return self.agent_instances[agent_name]
        
        # Try to import the agent
        try:
            agent_path = Path(f"agents/{agent_name}/{agent_name}.py")
            if not agent_path.exists():
                agent_path = Path(f"agents/{agent_name}/agent.py")
            if not agent_path.exists():
                return None
            
            import importlib.util
            spec = importlib.util.spec_from_file_location(agent_name, agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the agent class
            for attr in dir(module):
                if attr.endswith('Agent') and attr != 'BaseAgent':
                    agent_class = getattr(module, attr)
                    instance = agent_class()
                    self.agent_instances[agent_name] = instance
                    return instance
        except Exception as e:
            pass
        
        return None
    
    def run(self):
        while True:
            try:
                cmd = input("\n🦞 > ").strip()
                if not cmd:
                    continue
                
                # Global commands first
                if cmd.lower() in ['/quit', 'quit', 'exit']:
                    print("Goodbye!")
                    break
                if cmd == "/help":
                    print(self.help_text)
                    continue
                if cmd == "/agents":
                    print(f"\nAgents: {', '.join([str(p.name) for p in Path('agents').iterdir() if p.is_dir()])}")
                    continue
                
                # Find which agent handles this command
                first_word = cmd.split()[0].lower() if cmd else ""
                agent_name = self.command_map.get(first_word, 'mathematicaclaw')
                
                # Get agent instance
                agent = self.get_agent_instance(agent_name)
                
                if agent and hasattr(agent, 'handle'):
                    result = agent.handle(cmd)
                    print(f"\n🦞 {result}")
                else:
                    # Fallback to subprocess
                    possible_paths = [
                        Path(f"agents/{agent_name}/{agent_name}.py"),
                        Path(f"agents/{agent_name}/agent.py"),
                    ]
                    
                    agent_path = None
                    for path in possible_paths:
                        if path.exists():
                            agent_path = path
                            break
                    
                    if agent_path:
                        result = subprocess.run(
                            [sys.executable, str(agent_path), cmd],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        if result.stdout:
                            output = result.stdout.strip()
                            lines = output.split('\n')
                            filtered = [l for l in lines if not l.startswith('🦞 Starting') 
                                       and not l.startswith('Mathematicaclaw')
                                       and 'Type' not in l]
                            if filtered:
                                print(f"\n🦞 {'\n'.join(filtered)}")
                    else:
                        print(f"\n❌ Agent '{agent_name}' not found")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    Clawpack().run()
