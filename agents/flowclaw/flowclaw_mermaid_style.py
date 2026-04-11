#!/usr/bin/env python3
"""FlowClaw - Uses Official Mermaid Syntax"""

import sys
import webbrowser
import base64
from pathlib import Path
from datetime import datetime

class FlowClawMermaid:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def generate_flowchart(self, description):
        # Using Mermaid's proven syntax format
        return f"""flowchart TD
    A[{description}] -->|Action| B(Process)
    B --> C{{Decision}}
    C -->|Option 1| D[Result 1]
    C -->|Option 2| E[Result 2]
    C -->|Option 3| F[Result 3]
    D --> G[End]
    E --> G
    F --> G"""
    
    def generate_login_flow(self):
        return """flowchart TD
    A[User Login] -->|Enter credentials| B{Valid?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Error]
    D --> A"""
    
    def view(self, diagram_type, description):
        if diagram_type == "login":
            code = self.generate_login_flow()
        else:
            code = self.generate_flowchart(description)
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        # Open mermaid.live with the code
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.live/edit#base64:{encoded}"
        webbrowser.open(url)
        
        return f"""✅ Diagram opened in browser!
📁 Also saved to: {filename}
🌐 Mermaid Live should show your diagram automatically
"""
    
    def process(self, cmd, *args):
        if cmd == "view":
            diagram_type = args[0] if args else "flowchart"
            description = ' '.join(args[1:]) if len(args) > 1 else "Start"
            return self.view(diagram_type, description)
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Using Official Mermaid Syntax

COMMAND:
  python flowclaw_mermaid_style.py view [type] [description]

TYPES:
  flowchart - Generic flowchart
  login     - Login flow example

EXAMPLES:
  python flowclaw_mermaid_style.py view flowchart "Christmas Shopping"
  python flowclaw_mermaid_style.py view login

This uses the EXACT same syntax as the working Mermaid sample!
"""

def main():
    agent = FlowClawMermaid()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
