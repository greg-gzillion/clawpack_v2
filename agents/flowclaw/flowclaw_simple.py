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
    A[Start] --> B[Process]
    B --> C[End]"""
    
    def show_popup(self, code, title):
        # Simplified HTML with local rendering
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: monospace; margin: 20px; background: #1e1e1e; }}
        pre {{ background: #2d2d2d; color: #fff; padding: 20px; border-radius: 8px; overflow-x: auto; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #4CAF50; }}
        button {{ background: #4CAF50; color: white; border: none; padding: 10px 20px; margin: 5px; cursor: pointer; border-radius: 5px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎨 {title}</h1>
    <h3>Mermaid Diagram Code:</h3>
    <pre>{code}</pre>
    <button onclick="copyCode()">📋 Copy Code</button>
    <button onclick="downloadFile()">💾 Download .mmd</button>
    <p style="color: #aaa; margin-top: 20px;">
        💡 To view the diagram:<br>
        1. Copy the code above<br>
        2. Go to <a href="https://mermaid.live" target="_blank">https://mermaid.live</a><br>
        3. Paste the code to see your diagram
    </p>
</div>
<script>
    function copyCode() {{
        const code = document.querySelector('pre').textContent;
        navigator.clipboard.writeText(code);
        alert('Code copied! Go to mermaid.live to view');
    }}
    function downloadFile() {{
        const code = document.querySelector('pre').textContent;
        const blob = new Blob([code], {{type: 'text/plain'}});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'flowclaw_diagram.mmd';
        a.click();
        URL.revokeObjectURL(url);
        alert('File downloaded!');
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
        if diagram_type == "flowchart":
            code = self.generate_flowchart(description)
        else:
            code = self.generate_flowchart(description)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        self.show_popup(code, f"{diagram_type.title()}: {description}")
        return f"✅ Saved: {filename}\n📋 Code copied to popup - paste at https://mermaid.live to view"
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Diagram Generator

COMMAND:
  view flowchart "description"

EXAMPLE:
  view flowchart "user login process"

OUTPUT:
  - Saves .mmd file to output/
  - Opens popup with code to copy
  - Paste at https://mermaid.live to view diagram
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
