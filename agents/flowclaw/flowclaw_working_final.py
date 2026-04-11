#!/usr/bin/env python3
"""FlowClaw - Fully Working Version"""

import sys
import webbrowser
import urllib.parse
from pathlib import Path
from datetime import datetime

class FlowClaw:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def get_diagram_code(self, template, description=""):
        diagrams = {
            'login': '''flowchart TD
    A[Start] --> B[Enter Email]
    B --> C[Enter Password]
    C --> D{Valid Credentials?}
    D -->|Yes| E[Login Success]
    D -->|No| F[Show Error]
    F --> B
    E --> G[Dashboard]''',
            
            'decision': '''flowchart TD
    A[Start] --> B{Make Decision}
    B -->|Option A| C[Path A]
    B -->|Option B| D[Path B]
    B -->|Option C| E[Path C]
    C --> F[End]
    D --> F
    E --> F''',
            
            'process': f'''flowchart TD
    A[Start: {description if description else "Process"}] 
    A --> B[Step 1]
    B --> C{{Decision?}}
    C -->|Yes| D[Step 2]
    C -->|No| E[Alternative]
    D --> F[Complete]
    E --> F
    F --> G[End]''',
            
            'user_flow': '''flowchart LR
    A[Landing Page] --> B{Logged In?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Login Page]
    D --> E[Register]
    E --> C'''
        }
        
        return diagrams.get(template, diagrams['process'])
    
    def view(self, template, description=""):
        code = self.get_diagram_code(template, description)
        
        # Save locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{template}_{timestamp}.mmd"
        filename.write_text(code)
        
        # Open mermaid.live with code in URL (simple method)
        encoded = urllib.parse.quote(code)
        url = f"https://mermaid.live/edit#pako:{encoded}"
        
        # Alternative: Just open mermaid.live and let user paste
        webbrowser.open("https://mermaid.live")
        
        return f"""
╔══════════════════════════════════════════════════════════╗
║  🎨 FLOWCLAW - DIAGRAM GENERATED SUCCESSFULLY!          ║
╠══════════════════════════════════════════════════════════╣
║  📁 File saved: {filename}                               ║
║  🌐 Browser opened to: https://mermaid.live             ║
║                                                          ║
║  📋 NEXT STEPS:                                          ║
║  1. Copy the code below                                 ║
║  2. Paste it into mermaid.live                          ║
║  3. See your beautiful diagram!                         ║
╠══════════════════════════════════════════════════════════╣
║  CODE TO COPY:                                          ║
╚══════════════════════════════════════════════════════════╝

{code}

╔══════════════════════════════════════════════════════════╗
║  💡 TIP: Click in the mermaid.live editor,              ║
║         press Ctrl+A then Ctrl+V to paste!              ║
╚══════════════════════════════════════════════════════════╝
"""
    
    def process(self, cmd, *args):
        if cmd == "view":
            template = args[0] if args else "process"
            description = ' '.join(args[1:]) if len(args) > 1 else ""
            return self.view(template, description)
        return self.help()
    
    def help(self):
        return """
🎨 FLOWCLAW - Fully Working Diagram Generator

COMMANDS:
  view login                  - Login flow diagram
  view decision               - Decision tree diagram
  view process "description"  - Process flow diagram
  view user_flow              - User journey diagram

EXAMPLES:
  python flowclaw_working_final.py view login
  python flowclaw_working_final.py view process "User Registration"
  python flowclaw_working_final.py view decision

The diagram code will be displayed - just copy and paste into mermaid.live!
"""

def main():
    agent = FlowClaw()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
