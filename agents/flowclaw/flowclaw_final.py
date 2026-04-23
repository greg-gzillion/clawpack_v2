#!/usr/bin/env python3
"""FlowClaw - Finally Working!"""

import sys
import webbrowser
import base64
from pathlib import Path
from datetime import datetime

class FlowClawFinal:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def generate_diagram(self, title, steps):
        """Generate a clean working diagram"""
        nodes = []
        connections = []
        
        for i, step in enumerate(steps):
            nodes.append(f"    {chr(65+i)}[{step}]")
            if i > 0:
                connections.append(f"    {chr(65+i-1)} --> {chr(65+i)}")
        
        return f"""flowchart TD
{chr(10).join(nodes)}
{chr(10).join(connections)}"""
    
    def login_diagram(self):
        return """flowchart TD
    A[Start] --> B[Enter Email]
    B --> C[Enter Password]
    C --> D{Valid?}
    D -->|Yes| E[Login Success]
    D -->|No| F[Show Error]
    F --> B
    E --> G[Dashboard]"""
    
    def decision_diagram(self):
        return """flowchart TD
    A[Question] --> B{Decision}
    B -->|Option 1| C[Outcome 1]
    B -->|Option 2| D[Outcome 2]
    B -->|Option 3| E[Outcome 3]"""
    
    def view(self, diagram_type, description=""):
        if diagram_type == "login":
            code = self.login_diagram()
        elif diagram_type == "decision":
            code = self.decision_diagram()
        else:
            # Custom flowchart
            steps = description.split(",") if description else ["Start", "Process", "Decision", "End"]
            code = self.generate_diagram(description or "Flow", steps)
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        # Open in mermaid.live
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.live/edit#base64:{encoded}"
        webbrowser.open(url)
        
        return f"""✅ Working diagram opened in browser!
📁 Saved: {filename}
🌐 Mermaid Live should show your diagram

Code:
{code}...
"""
    
    def process(self, cmd, *args):
        if cmd == "view":
            diagram_type = args[0] if args else "flowchart"
            description = ' '.join(args[1:]) if len(args) > 1 else ""
            return self.view(diagram_type, description)
        return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - FINALLY WORKING!

COMMANDS:
  view login                    - Show login flowchart
  view decision                 - Show decision flowchart  
  view flowchart "Step1,Step2"  - Custom flowchart

EXAMPLES:
  python flowclaw_final.py view login
  python flowclaw_final.py view decision
  python flowclaw_final.py view flowchart "Start,Process,End"

The diagram will open in your browser automatically!
"""

def main():
    agent = FlowClawFinal()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
