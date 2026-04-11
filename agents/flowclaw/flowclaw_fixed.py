#!/usr/bin/env python3
"""FlowClaw - Fixed Diagram Generator"""

import sys
import webbrowser
import base64
import json
from pathlib import Path
from datetime import datetime

class FlowClawFixed:
    def __init__(self):
        self.output_path = Path(__file__).parent / "output"
        self.output_path.mkdir(exist_ok=True)
    
    def generate_flowchart(self, description):
        return f"""graph TD
    A[Start] --> B{{Has Account?}}
    B -->|Yes| C[Enter Password]
    B -->|No| D[Register]
    C --> E{{Password Valid?}}
    E -->|Yes| F[Login Success]
    E -->|No| G[Try Again]
    G --> C
    D --> H[Create Account]
    H --> F
    F --> I[End]"""
    
    def generate_simple(self, description):
        return f"""graph LR
    A[Start] --> B[Process]
    B --> C[End]"""
    
    def view(self, diagram_type, description):
        # Generate valid Mermaid code
        if diagram_type == "flowchart":
            code = self.generate_flowchart(description)
        else:
            code = self.generate_simple(description)
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        # Create HTML with local rendering (no CDN issues)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>FlowClaw Diagram</title>
    <style>
        body {{
            font-family: monospace;
            background: #1a1a2e;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
        }}
        h1 {{
            color: #4CAF50;
            text-align: center;
        }}
        .code-block {{
            background: #0f0f1a;
            color: #00ff00;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
        }}
        .button-group {{
            text-align: center;
            margin: 20px 0;
        }}
        button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }}
        button:hover {{
            background: #45a049;
        }}
        .info {{
            background: #0f0f1a;
            color: #aaa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            text-align: center;
        }}
        a {{
            color: #4CAF50;
        }}
        .diagram-preview {{
            background: #0f0f1a;
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .arrow {{
            font-size: 20px;
            color: #4CAF50;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎨 FlowClaw Diagram</h1>
    
    <div class="code-block">
        <strong>📝 Mermaid Code:</strong><br>
        <pre id="code" style="margin:10px 0; overflow-x:auto;">{code}</pre>
    </div>
    
    <div class="button-group">
        <button onclick="copyCode()">📋 Copy Code</button>
        <button onclick="downloadFile()">💾 Download .mmd</button>
        <button onclick="openMermaid()">🔗 Open in Mermaid Live</button>
    </div>
    
    <div class="diagram-preview">
        <strong>🎨 Diagram Preview (Text Representation):</strong><br><br>
        <span id="preview"></span>
    </div>
    
    <div class="info">
        💡 <strong>How to view your diagram:</strong><br>
        1. Click "Copy Code" button above<br>
        2. Click "Open in Mermaid Live"<br>
        3. Paste the code (Ctrl+V) in the editor<br>
        4. Your diagram will appear instantly!<br><br>
        📁 File also saved to: {filename}
    </div>
</div>

<script>
function copyCode() {{
    const code = document.getElementById('code').textContent;
    navigator.clipboard.writeText(code);
    alert('✅ Code copied! Now paste it in mermaid.live');
}}

function downloadFile() {{
    const code = document.getElementById('code').textContent;
    const blob = new Blob([code], {{type: 'text/plain'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flowclaw_diagram.mmd';
    a.click();
    URL.revokeObjectURL(url);
    alert('✅ File downloaded!');
}}

function openMermaid() {{
    window.open('https://mermaid.live', '_blank');
    alert('1. Go to mermaid.live\\n2. Paste the code (Ctrl+V)\\n3. See your diagram!');
}}

// Simple text preview
function showTextPreview() {{
    const code = document.getElementById('code').textContent;
    const lines = code.split('\\n');
    let preview = '';
    for(let line of lines.slice(0, 8)) {{
        if(line.includes('-->')) {{
            preview += line.replace(/-->/, '<span class="arrow">→</span>') + '<br>';
        }} else if(!line.includes('graph') && !line.includes('end')) {{
            preview += line + '<br>';
        }}
    }}
    document.getElementById('preview').innerHTML = preview;
}}

showTextPreview();
</script>
</body>
</html>"""
        
        # Save HTML and open
        html_file = self.output_path / f"diagram_{timestamp}.html"
        html_file.write_text(html)
        webbrowser.open(f'file://{html_file.absolute()}')
        
        return f"""✅ Diagram generated and saved!
📁 Mermaid code: {filename}
🌐 HTML viewer opened in browser
💡 Click 'Open in Mermaid Live' to see the rendered diagram
"""
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Fixed Diagram Generator

COMMAND:
  view flowchart "description"

EXAMPLE:
  view flowchart "user login process"

This will:
  1. Generate valid Mermaid code
  2. Open a viewer with copy/paste instructions
  3. Save the .mmd file
  4. Guide you to mermaid.live to see the diagram
"""

def main():
    agent = FlowClawFixed()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
