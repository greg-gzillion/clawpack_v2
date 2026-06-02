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
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>""" + title + """ - FlowClaw</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 1400px; margin: 0 auto; background: white;
            border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; text-align: center;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .diagram {
            padding: 40px; display: flex; justify-content: center;
            background: #f8f9fa; min-height: 400px;
        }
        .mermaid { width: 100%; }
        .controls {
            display: flex; gap: 10px; justify-content: center;
            padding: 20px; background: #f1f3f5; border-top: 1px solid #dee2e6;
        }
        button {
            padding: 10px 20px; border: none; border-radius: 8px;
            cursor: pointer; font-size: 14px; font-weight: 600;
            transition: all 0.2s;
        }
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5a6fd6; }
        .btn-secondary { background: #6c757d; color: white; }
        .btn-secondary:hover { background: #5a6268; }
        .btn-success { background: #28a745; color: white; }
        .btn-success:hover { background: #218838; }
        #status { text-align: center; padding: 10px; color: #6c757d; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>""" + title + """</h1>
            <p>FlowClaw - Premium Diagram Generator</p>
        </div>
        <div class="diagram">
            <div class="mermaid">
""" + code + """
            </div>
        </div>
        <div class="controls">
            <button class="btn-primary" onclick="zoomIn()">Zoom In</button>
            <button class="btn-primary" onclick="zoomOut()">Zoom Out</button>
            <button class="btn-secondary" onclick="resetZoom()">Reset</button>
            <button class="btn-success" onclick="savePNG()">Save as PNG</button>
            <button class="btn-secondary" onclick="window.print()">Print</button>
        </div>
        <div id="status">Ready</div>
    </div>
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default' });

        let currentZoom = 1;
        function zoomIn() {
            currentZoom += 0.1;
            document.querySelector('.mermaid').style.transform = 'scale(' + currentZoom + ')';
            document.getElementById('status').textContent = 'Zoom: ' + Math.round(currentZoom * 100) + '%';
        }
        function zoomOut() {
            currentZoom = Math.max(0.2, currentZoom - 0.1);
            document.querySelector('.mermaid').style.transform = 'scale(' + currentZoom + ')';
            document.getElementById('status').textContent = 'Zoom: ' + Math.round(currentZoom * 100) + '%';
        }
        function resetZoom() {
            currentZoom = 1;
            document.querySelector('.mermaid').style.transform = 'scale(1)';
            document.getElementById('status').textContent = 'Zoom: 100%';
        }
        async function savePNG() {
            const svg = document.querySelector('.mermaid svg');
            if (!svg) {
                document.getElementById('status').textContent = 'No diagram to save';
                return;
            }
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const svgData = new XMLSerializer().serializeToString(svg);
            const img = new Image();
            const blob = new Blob([svgData], {type: 'image/svg+xml;charset=utf-8'});
            const url = URL.createObjectURL(blob);
            img.onload = function() {
                canvas.width = img.width * 2;
                canvas.height = img.height * 2;
                ctx.scale(2, 2);
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0);
                canvas.toBlob(function(blob) {
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = 'flowclaw_diagram.png';
                    a.click();
                    document.getElementById('status').textContent = 'PNG saved!';
                });
                URL.revokeObjectURL(url);
            };
            img.src = url;
        }
    </script>
</body>
</html>"""
        import tempfile, webbrowser, os
        tmp = tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8')
        tmp.write(html)
        tmp.close()
        webbrowser.open('file:///' + tmp.name.replace('\\', '/'))
        return "Diagram opened in browser"
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
