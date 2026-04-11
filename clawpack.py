#!/usr/bin/env python3
"""Clawpack V2 - Modular Agent Menu System"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================================
# AGENT MODULES - Each agent handles its own commands
# ============================================================================

class AgentMenu:
    """Base class for agent menus"""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.commands = {}
    
    def show(self):
        print(f"\n{'='*50}")
        print(f"🦞 {self.name.upper()} - {self.description}")
        print(f"{'='*50}")
        for cmd, desc in self.commands.items():
            print(f"  {cmd:<25} {desc}")
        print(f"\n  {'back':<25} Return to main menu")
        print(f"  {'help':<25} Show this help")
        print(f"{'='*50}")
    
    def handle(self, cmd):
        return None  # Override in subclass

# ============================================================================
# LAWCLAW MENU
# ============================================================================
class LawClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("lawclaw", "LawClaw Research Assistant")
        self.commands = {
            "/court <ST> <loc>": "Court information",
            "/searchindex <q>": "Search law database",
            "/searchcase <case>": "AI case law analysis",
            "/citation <cite>": "Citation lookup",
            "/docket <num>": "Docket search",
        }
    
    def handle(self, cmd):
        from agents.lawclaw.lawclaw import LawClawAgent
        agent = LawClawAgent()
        return agent.handle(cmd)

# ============================================================================
# FLOWCLAW MENU
# ============================================================================
class FlowClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("flowclaw", "Diagram Generator")
        self.commands = {
            "/flowchart <desc>": "Generate flowchart",
            "/sequence <desc>": "Sequence diagram",
            "/architecture <desc>": "Architecture diagram",
            "/gantt <desc>": "Gantt chart",
            "/state <desc>": "State diagram",
        }
    
    def handle(self, cmd):
        from agents.flowclaw.flowclaw import FlowClawAgent
        agent = FlowClawAgent()
        return agent.handle(cmd)

# ============================================================================
# DOCUCLAW MENU
# ============================================================================
class DocClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("docuclaw", "Document Processor")
        self.commands = {
            "/create <type>": "Create document (letter/report/memo)",
            "/ai <topic> <type>": "AI-generated document",
            "/export <file> <fmt>": "Export to PDF/Markdown",
            "/import <file>": "Import document",
        }
    
    def handle(self, cmd):
        from agents.docuclaw.docuclaw import DocuClawAgent
        agent = DocuClawAgent()
        return agent.handle(cmd)

# ============================================================================
# MATHCLAW MENU
# ============================================================================
class MathClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("mathematicaclaw", "Mathematics & Visualization")
        self.commands = {
            "/visualize <desc>": "AI math visualization",
            "/solve <equation>": "Solve equation",
            "/plot <function>": "Plot function",
        }
    
    def handle(self, cmd):
        from agents.mathematicaclaw.mathematicaclaw import MathematicaClawAgent
        agent = MathematicaClawAgent()
        return agent.handle(cmd)

# ============================================================================
# LIBERATECLAW MENU
# ============================================================================
class LiberateClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("liberateclaw", "Model Liberation")
        self.commands = {
            "/models": "List available models",
            "/liberate <model>": "Download/liberate model",
            "/use <model> <prompt>": "Run inference",
            "/liberated": "List liberated models",
        }
    
    def handle(self, cmd):
        from agents.liberateclaw.liberateclaw import liberateclawAgent
        agent = liberateclawAgent()
        return agent.handle(cmd)

# ============================================================================
# TXCLAW MENU
# ============================================================================
class TXClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("txclaw", "Blockchain Assistant")
        self.commands = {
            "/create <name>": "Create smart contract",
            "/deploy <contract>": "Deploy to testnet",
            "/test <contract>": "Run contract tests",
        }
    
    def handle(self, cmd):
        from agents.txclaw.txclaw import TXClaw
        agent = TXClaw()
        return agent.handle(cmd)

# ============================================================================
# INTERPRETCLAW MENU
# ============================================================================
class InterpretClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("interpretclaw", "Translation & Speech")
        self.commands = {
            "/translate <text> to <lang>": "Translate text",
            "/speak <text>": "Text-to-speech",
        }
    
    def handle(self, cmd):
        from agents.interpretclaw.interpretclaw import InterpretClawAgent
        agent = InterpretClawAgent()
        return agent.handle(cmd)

# ============================================================================
# LANGCLAW MENU
# ============================================================================
class LangClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("langclaw", "Language Teacher")
        self.commands = {
            "/lesson <lang> <topic>": "Start a lesson",
            "/practice": "Practice session",
            "/vocab": "Vocabulary builder",
        }
    
    def handle(self, cmd):
        from agents.langclaw.langclaw import LangClawAgent
        agent = LangClawAgent()
        return agent.handle(cmd)

# ============================================================================
# CLAWCODER MENU
# ============================================================================
class ClawCoderMenu(AgentMenu):
    def __init__(self):
        super().__init__("claw_coder", "Code Generation")
        self.commands = {
            "/code <task> <lang>": "Generate code",
            "/analyze <file>": "Analyze code",
        }
    
    def handle(self, cmd):
        from agents.claw_coder.claw_coder import ClawCoderAgent
        agent = ClawCoderAgent()
        return agent.handle(cmd)

# ============================================================================
# DATACLAW MENU
# ============================================================================
class DataClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("dataclaw", "Data Management")
        self.commands = {
            "/add <file>": "Add reference",
            "/search <q>": "Search local data",
            "/stats": "Show statistics",
        }
    
    def handle(self, cmd):
        from agents.dataclaw.dataclaw import DataClaw
        agent = DataClaw()
        return agent.handle(cmd)

# ============================================================================
# WEBCLAW MENU
# ============================================================================
class WebClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("webclaw", "Web Search")
        self.commands = {
            "/search <q>": "Search web",
            "/index <url>": "Index URL",
        }
    
    def handle(self, cmd):
        from agents.webclaw.webclaw import WebClawAgent
        agent = WebClawAgent()
        return agent.handle(cmd)

# ============================================================================
# FILECLAW MENU
# ============================================================================
class FileClawMenu(AgentMenu):
    def __init__(self):
        super().__init__("fileclaw", "File Management")
        self.commands = {
            "/analyze <file>": "AI file analysis",
            "/convert <in> <out>": "Convert format",
            "/batch <dir> <op>": "Batch process",
            "/find <query>": "Find files",
        }
    
    def handle(self, cmd):
        from agents.fileclaw.fileclaw import FileClawAgent
        agent = FileClawAgent()
        return agent.handle(cmd)

# ============================================================================
# MAIN CLAWPACK
# ============================================================================
class Clawpack:
    def __init__(self):
        self.menus = {
            "1": ("lawclaw", LawClawMenu(), "⚖️ LawClaw Research"),
            "2": ("flowclaw", FlowClawMenu(), "📊 Diagrams"),
            "3": ("docuclaw", DocClawMenu(), "📝 Documents"),
            "4": ("mathematicaclaw", MathClawMenu(), "📐 Mathematics"),
            "5": ("liberateclaw", LiberateClawMenu(), "🔓 Model Liberation"),
            "6": ("txclaw", TXClawMenu(), "💰 Blockchain"),
            "7": ("interpretclaw", InterpretClawMenu(), "🌐 Translation"),
            "8": ("langclaw", LangClawMenu(), "📚 Language"),
            "9": ("claw_coder", ClawCoderMenu(), "💻 Code"),
            "10": ("dataclaw", DataClawMenu(), "💾 Data"),
            "11": ("webclaw", WebClawMenu(), "🌍 Web"),
            "12": ("fileclaw", FileClawMenu(), "📁 Files"),
        }
    
    def show_main_menu(self):
        print("\n" + "="*60)
        print("🦞 CLAWPACK V2 - AI Agent Ecosystem")
        print("="*60)
        for key, (name, _, desc) in self.menus.items():
            print(f"  {key}. {desc}")
        print("-"*60)
        print("  q. Quit")
        print("="*60)
    
    def run(self):
        while True:
            self.show_main_menu()
            choice = input("\n📋 Select an agent (1-12) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("Goodbye! 🦞")
                break
            
            if choice in self.menus:
                name, menu, desc = self.menus[choice]
                self.run_agent_menu(name, menu, desc)
            else:
                print("❌ Invalid choice. Please enter 1-12 or 'q'")
    
    def run_agent_menu(self, name, menu, desc):
        while True:
            menu.show()
            cmd = input(f"\n{name}> ").strip()
            
            if cmd.lower() == 'back':
                break
            elif cmd.lower() == 'help':
                continue
            elif cmd:
                result = menu.handle(cmd)
                print(f"\n{result}\n")
                input("Press Enter to continue...")

def main():
    claw = Clawpack()
    claw.run()

if __name__ == "__main__":
    main()
