#!/usr/bin/env python3
"""FlowClaw - Standalone Diagram Generator (No Internet Needed)"""

import sys
import webbrowser
import tempfile
from pathlib import Path
from datetime import datetime

class FlowClawStandalone:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def generate_flowchart(self, description):
        return f"""graph TD
    A[Start: {description}]
    B[Process]
    C{{Decision}}
    D[End]
    A --> B --> C
    C -->|Yes| D
    C -->|No| B"""
    
    def generate_sequence(self, description):
        return f"""sequenceDiagram
    participant User
    participant System
    User->>System: {description}
    System-->>User: Response"""
    
    def generate_architecture(self, description):
        return """graph TB
    A[Frontend] --> B[Backend] --> C[Database]"""
    
    def show_diagram(self, code, title):
        """Show diagram using pure text with link to view online"""
        html = f"""<!DOCTYPE html>
<html>
<head><title>{title} - FlowClaw</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
.container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 12px; padding: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
h1 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
pre {{ background: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; overflow-x: auto; font-family: 'Courier New', monospace; }}
button {{ background: #667eea; color: white; border: none; padding: 10px 20px; margin: 10px 5px; border-radius: 6px; cursor: pointer; font-size: 14px; }}
button:hover {{ background: #5a67d8; transform: translateY(-1px); }}
.view-link {{ display: inline-block; background: #28a745; color: white; padding: 10px 20px; margin: 10px 5px; border-radius: 6px; text-decoration: none; }}
.view-link:hover {{ background: #218838; }}
.footer {{ margin-top: 20px; padding-top: 15px; border-top: 1px solid #e0e0e0; text-align: center; color: #666; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
    <h1>🎨 {title}</h1>
    <h3>Mermaid Diagram Code:</h3>
    <pre id="codeBlock">{code}</pre>
    
    <div style="text-align: center;">
        <button onclick="copyCode()">📋 Copy Code</button>
        <button onclick="downloadFile()">💾 Download .mmd</button>
        <a href="https://mermaid.live" target="_blank" class="view-link">🔗 View Diagram on Mermaid Live</a>
    </div>
    
    <div class="footer">
        <strong>Instructions:</strong><br>
        1. Click "Copy Code" to copy the diagram code<br>
        2. Click "View Diagram on Mermaid Live"<br>
        3. Paste the code (Ctrl+V) to see your diagram rendered<br>
        4. You can also save as PNG, SVG, or PDF from there
    </div>
</div>
<script>
function copyCode() {{
    const code = document.getElementById('codeBlock').textContent;
    navigator.clipboard.writeText(code);
    alert('✅ Code copied! Now go to mermaid.live and paste (Ctrl+V)');
}}
function downloadFile() {{
    const code = document.getElementById('codeBlock').textContent;
    const blob = new Blob([code], {{type: 'text/plain'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flowclaw_diagram.mmd';
    a.click();
    URL.revokeObjectURL(url);
    alert('✅ File downloaded!');
}}
</script>
</body>
</html>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        
        webbrowser.open(f'file://{temp_path}')
        return temp_path
    
    def view(self, diagram_type, description):
        generators = {
            'flowchart': self.generate_flowchart,
            'sequence': self.generate_sequence,
            'architecture': self.generate_architecture
        }
        
        generator = generators.get(diagram_type, self.generate_flowchart)
        code = generator(description)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        self.show_diagram(code, f"{diagram_type.title()}: {description}")
        return f"✅ Saved: {filename}\n📋 Code copied to popup - paste at mermaid.live to view"
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Standalone Diagram Generator

COMMAND:
  view <type> <description>

TYPES:
  flowchart, sequence, architecture

EXAMPLES:
  view flowchart "user login process"
  view sequence "API call flow"
  view architecture "web app with database"

HOW IT WORKS:
  1. Generates Mermaid diagram code
  2. Opens popup with code
  3. Copy code and paste at mermaid.live
  4. See your beautiful diagram!
"""

def main():
    agent = FlowClawStandalone()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
