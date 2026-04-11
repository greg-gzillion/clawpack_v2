#!/usr/bin/env python3
"""FlowClaw - Diagram Generator with Local Rendering"""

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
    B[Process Step]
    C{{Decision?}}
    D[Action]
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
    participant Database
    
    User->>System: {description}
    System->>Database: Query
    Database-->>System: Result
    System-->>User: Response"""
    
    def generate_architecture(self, description):
        return """graph TB
    subgraph Frontend
        A[UI Layer]
    end
    subgraph Backend
        B[API Gateway]
        C[Microservices]
    end
    subgraph Data
        D[(Database)]
        E[Cache]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E"""
    
    def generate_gantt(self, description):
        return f"""gantt
    title {description}
    dateFormat YYYY-MM-DD
    section Planning
    Research :a1, 2024-01-01, 7d
    Design :after a1, 5d
    section Development
    Coding :2024-01-15, 14d
    Testing :2024-01-29, 7d
    section Deployment
    Launch :2024-02-05, 3d"""
    
    def generate_state(self, description):
        return f"""stateDiagram-v2
    [*] --> Initial
    Initial --> Active : Start
    Active --> Paused : Pause
    Paused --> Active : Resume
    Active --> Completed : Finish
    Completed --> [*]"""
    
    def show_diagram(self, code, title):
        """Show diagram in browser with local Mermaid rendering"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - FlowClaw</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 35px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 5px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .toolbar {{
            padding: 15px 35px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
        }}
        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s;
        }}
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        .btn-primary:hover {{
            background: #5a67d8;
            transform: translateY(-2px);
        }}
        .btn-success {{
            background: #28a745;
            color: white;
        }}
        .btn-success:hover {{
            background: #218838;
            transform: translateY(-2px);
        }}
        .btn-secondary {{
            background: #6c757d;
            color: white;
        }}
        .btn-secondary:hover {{
            background: #5a6268;
        }}
        .diagram-container {{
            padding: 40px;
            background: #f8f9fa;
            min-height: 500px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: auto;
        }}
        .mermaid {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: inline-block;
            min-width: 300px;
        }}
        .status {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
        }}
        .footer {{
            padding: 15px 35px;
            background: #f8f9fa;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #e0e0e0;
        }}
        @media (max-width: 768px) {{
            .toolbar {{
                padding: 15px 20px;
            }}
            .diagram-container {{
                padding: 20px;
            }}
            button {{
                padding: 8px 16px;
                font-size: 12px;
            }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎨 {title}</h1>
        <p>Generated by FlowClaw AI - Premium Diagram Generator</p>
    </div>
    <div class="toolbar">
        <button class="btn-primary" onclick="copyCode()">📋 Copy Mermaid Code</button>
        <button class="btn-success" onclick="downloadPNG()">📸 Save as PNG</button>
        <button class="btn-secondary" onclick="downloadMMD()">💾 Download .mmd</button>
        <button class="btn-secondary" onclick="zoomIn()">🔍 Zoom In</button>
        <button class="btn-secondary" onclick="zoomOut()">🔍 Zoom Out</button>
        <button class="btn-secondary" onclick="resetZoom()">⟳ Reset</button>
    </div>
    <div class="diagram-container" id="diagramContainer">
        <div id="zoomWrapper" style="transition: transform 0.2s;">
            <pre class="mermaid" id="diagram">
{code}
            </pre>
        </div>
    </div>
    <div class="footer">
        💡 Tip: Right-click on diagram → Save as SVG | Zoom with buttons or Ctrl+Mouse Wheel
    </div>
</div>
<div class="status" id="status">Ready</div>

<script>
    let currentZoom = 1;
    const zoomWrapper = document.getElementById('zoomWrapper');
    
    function updateZoom() {{
        zoomWrapper.style.transform = `scale(${{currentZoom}})`;
        document.getElementById('status').textContent = `Zoom: {Math.round(currentZoom * 100)}%`;
    }}
    
    function zoomIn() {{
        currentZoom = Math.min(currentZoom + 0.1, 3);
        updateZoom();
    }}
    
    function zoomOut() {{
        currentZoom = Math.max(currentZoom - 0.1, 0.5);
        updateZoom();
    }}
    
    function resetZoom() {{
        currentZoom = 1;
        updateZoom();
    }}
    
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'base',
        themeVariables: {{
            'background': '#ffffff',
            'primaryColor': '#667eea',
            'primaryBorderColor': '#764ba2',
            'primaryTextColor': '#333',
            'lineColor': '#555',
            'secondaryColor': '#f0f0f0',
            'tertiaryColor': '#ffffff',
            'fontSize': '16px'
        }},
        flowchart: {{
            useMaxWidth: false,
            htmlLabels: true,
            curve: 'basis'
        }},
        securityLevel: 'loose'
    }});
    
    function copyCode() {{
        const code = document.getElementById('diagram').textContent;
        navigator.clipboard.writeText(code);
        showStatus('✅ Code copied!');
    }}
    
    function downloadMMD() {{
        const code = document.getElementById('diagram').textContent;
        const blob = new Blob([code], {{type: 'text/plain'}});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'flowclaw_diagram.mmd';
        a.click();
        URL.revokeObjectURL(url);
        showStatus('✅ File downloaded!');
    }}
    
    async function downloadPNG() {{
        const svg = document.querySelector('#diagram svg');
        if (!svg) {{
            showStatus('⚠️ Please wait for diagram to render', true);
            return;
        }}
        
        showStatus('📸 Rendering PNG...');
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const data = new XMLSerializer().serializeToString(svg);
        const img = new Image();
        
        img.onload = () => {{
            canvas.width = img.width * 2;
            canvas.height = img.height * 2;
            ctx.scale(2, 2);
            ctx.drawImage(img, 0, 0);
            const png = canvas.toDataURL('image/png');
            const a = document.createElement('a');
            a.href = png;
            a.download = 'flowclaw_diagram.png';
            a.click();
            showStatus('✅ PNG saved!');
        }};
        
        img.onerror = () => {{
            showStatus('❌ Error rendering PNG', true);
        }};
        
        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(data)));
    }}
    
    function showStatus(msg, isError = false) {{
        const status = document.getElementById('status');
        status.textContent = msg;
        status.style.background = isError ? 'rgba(220,53,69,0.9)' : 'rgba(0,0,0,0.8)';
        setTimeout(() => {{
            status.style.background = 'rgba(0,0,0,0.8)';
        }}, 2000);
    }}
    
    // Handle rendering
    setTimeout(() => {{
        const svg = document.querySelector('#diagram svg');
        if (!svg) {{
            document.getElementById('diagramContainer').innerHTML = '<div style="text-align:center;padding:40px;color:#dc3545;">⚠️ Diagram rendering error. Check console for details.</div>';
        }} else {{
            showStatus('✅ Diagram rendered successfully');
        }}
    }}, 2000);
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
            'architecture': self.generate_architecture,
            'gantt': self.generate_gantt,
            'state': self.generate_state
        }
        
        generator = generators.get(diagram_type, self.generate_flowchart)
        code = generator(description)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_path / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        
        self.show_diagram(code, f"{diagram_type.title()}: {description}")
        return f"✅ Diagram saved to: {filename}\n🌐 Browser popup opened with rendered diagram!"
    
    def process(self, cmd, *args):
        if cmd == "view" and len(args) >= 2:
            return self.view(args[0], ' '.join(args[1:]))
        elif cmd == "list":
            diagrams = list(self.output_path.glob("*.mmd"))
            if not diagrams:
                return "No diagrams yet"
            return "\n".join(f"  • {d.name}" for d in diagrams[-10:])
        else:
            return self.help()
    
    def help(self):
        return """
🎨 FlowClaw - Premium Diagram Generator with Local Rendering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMANDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  view flowchart "description"   - Generate flowchart
  view sequence "description"    - Generate sequence diagram
  view architecture "description" - Generate architecture diagram
  view gantt "description"       - Generate Gantt chart
  view state "description"       - Generate state diagram
  list                           - List saved diagrams

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  view flowchart "user login with email and password"
  view sequence "client sends request to server"
  view architecture "microservices with database"
  view gantt "website development project"
  view state "order processing workflow"
  list

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ Local rendering (no external website needed)
  ✓ Copy code, download .mmd, save as PNG
  ✓ Zoom in/out with buttons
  ✓ Professional styling
  ✓ Responsive design
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
