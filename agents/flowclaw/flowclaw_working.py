#!/usr/bin/env python3
"""FlowClaw - Simple Working Diagram Generator"""

import sys
import webbrowser
import tempfile
from pathlib import Path
from datetime import datetime

class FlowClaw:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def generate_flowchart(self, description):
        return f"""graph TD
    A[Start: {description}]
    B[Process Step 1]
    C{{Decision?}}
    D[Process Step 2]
    E[End]
    
    A --> B
    B --> C
    C -->|Yes| D
    C -->|No| E
    D --> E"""
    
    def generate_sequence(self, description):
        return f"""sequenceDiagram
    participant User
    participant System
    User->>System: {description}
    System-->>User: Response"""
    
    def generate_architecture(self, description):
        return """graph TB
    subgraph Frontend
        A[UI Layer]
    end
    subgraph Backend
        B[API Layer]
        C[Logic Layer]
    end
    subgraph Data
        D[Database]
    end
    A --> B
    B --> C
    C --> D"""
    
    def show_popup(self, code, title):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f0f2f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; }}
        h1 {{ color: #667eea; }}
        .diagram {{ text-align: center; margin: 20px 0; }}
        button {{ background: #667eea; color: white; border: none; padding: 10px 20px; margin: 5px; border-radius: 5px; cursor: pointer; }}
        .mermaid {{ background: white; padding: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎨 {title}</h1>
    <div class="diagram">
        <pre class="mermaid">
{code}
        </pre>
    </div>
    <div style="text-align: center;">
        <button onclick="copyCode()">📋 Copy Code</button>
        <button onclick="window.print()">🖨️ Print / PDF</button>
    </div>
</div>
<script>
    mermaid.initialize({{ startOnLoad: true, theme: 'base' }});
    function copyCode() {{
        const code = document.querySelector('.mermaid').textContent;
        navigator.clipboard.writeText(code);
        alert('Code copied!');
    }}
</script>
</body>
</html>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html)
            webbrowser.open(f'file://{f.name}')
    
    def view(self, diagram_type, description):
        if diagram_type == "flowchart":
            code = self.generate_flowchart(description)
        elif diagram_type == "sequence":
            code = self.generate_sequence(description)
        elif diagram_type == "architecture":
            code = self.generate_architecture(description)
        else:
            code = self.generate_flowchart(description)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        self.show_popup(code, f"{diagram_type.title()}: {description}")
        return f"✅ Saved: {filename}"
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Simple Diagram Generator

COMMANDS:
  view <type> <description>  - Generate and show diagram

TYPES:
  flowchart, sequence, architecture

EXAMPLES:
  view flowchart "user login process"
  view sequence "API call flow"
  view architecture "web application"
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
