"""High-resolution diagram renderer"""
import subprocess
import tempfile
from pathlib import Path
import base64

class HighResRenderer:
    """Render diagrams at high resolution (300+ DPI)"""
    
    @staticmethod
    def render_to_png(mermaid_code: str, output_path: Path, scale: int = 3) -> bool:
        """Render to high-res PNG using mermaid-cli or browser"""
        try:
            # Try using mermaid-cli if available
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_code)
                mmd_file = f.name
            
            # Attempt to use mmdc (mermaid-cli)
            result = subprocess.run(
                ['mmdc', '-i', mmd_file, '-o', str(output_path), '-s', str(scale)],
                capture_output=True
            )
            Path(mmd_file).unlink()
            
            if result.returncode == 0:
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def generate_html_with_zoom(mermaid_code: str, title: str) -> str:
        """Generate HTML with high-quality rendering and zoom controls"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} - FlowClaw High Resolution</title>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 35px;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 5px; }}
        .controls {{
            padding: 20px 35px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .zoom-control {{
            display: flex;
            align-items: center;
            gap: 10px;
            background: white;
            padding: 8px 15px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        button {{
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
            font-size: 14px;
        }}
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5a67d8; transform: translateY(-1px); }
        .btn-success { background: #28a745; color: white; }
        .btn-success:hover { background: #218838; transform: translateY(-1px); }
        .btn-secondary { background: #6c757d; color: white; }
        .btn-secondary:hover { background: #5a6268; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-info { background: #17a2b8; color: white; }
        .diagram-container {{
            padding: 40px;
            background: #f8f9fa;
            min-height: 600px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: auto;
            position: relative;
        }}
        .diagram-wrapper {{
            transition: transform 0.3s ease;
            transform-origin: center center;
        }}
        .mermaid {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            display: inline-block;
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
        .resolution-select {{
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #ddd;
            font-size: 14px;
        }}
        .footer {{
            padding: 15px 35px;
            background: #f8f9fa;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎨 {title}</h1>
        <p>High-Resolution Diagram | Generated by FlowClaw AI</p>
    </div>
    <div class="controls">
        <div class="zoom-control">
            <span>🔍 Zoom:</span>
            <button onclick="zoomOut()">−</button>
            <span id="zoomLevel">100%</span>
            <button onclick="zoomIn()">+</button>
            <button onclick="resetZoom()">Reset</button>
        </div>
        <div class="zoom-control">
            <span>📐 Scale:</span>
            <select id="scaleSelect" class="resolution-select">
                <option value="1">1x (Standard)</option>
                <option value="2" selected>2x (High)</option>
                <option value="3">3x (Ultra)</option>
                <option value="4">4x (Print)</option>
            </select>
        </div>
        <button class="btn-primary" onclick="copyCode()">📋 Copy Mermaid Code</button>
        <button class="btn-success" onclick="saveAsPNG()">📸 Save PNG (High-Res)</button>
        <button class="btn-info" onclick="saveAsSVG()">🎯 Save as SVG</button>
        <button class="btn-secondary" onclick="downloadMMD()">💾 Download .mmd</button>
    </div>
    <div class="diagram-container" id="diagramContainer">
        <div class="diagram-wrapper" id="diagramWrapper">
            <pre class="mermaid" id="diagram">
{mermaid_code}
            </pre>
        </div>
    </div>
    <div class="footer">
        💡 Tip: Use 2x-4x scale for print quality | Right-click on diagram → Save as SVG for vector format
    </div>
</div>
<div class="status" id="status">Ready</div>

<script>
let currentZoom = 1;
const diagramWrapper = document.getElementById('diagramWrapper');

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
        'fontSize': '16px',
        'fontFamily': 'Arial, sans-serif'
    }},
    flowchart: {{ useMaxWidth: false, htmlLabels: true, curve: 'basis' }},
    securityLevel: 'loose'
}});

function updateZoom() {{
    diagramWrapper.style.transform = `scale(${{currentZoom}})`;
    document.getElementById('zoomLevel').innerText = Math.round(currentZoom * 100) + '%';
}}

function zoomIn() {{ currentZoom = Math.min(currentZoom + 0.1, 3); updateZoom(); }}
function zoomOut() {{ currentZoom = Math.max(currentZoom - 0.1, 0.5); updateZoom(); }}
function resetZoom() {{ currentZoom = 1; updateZoom(); }}

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

async function saveAsSVG() {{
    const svg = document.querySelector('#diagram svg');
    if (!svg) {{ showStatus('⚠️ Wait for render', true); return; }}
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], {{type: 'image/svg+xml'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'flowclaw_diagram.svg';
    a.click();
    URL.revokeObjectURL(url);
    showStatus('✅ SVG saved!');
}}

async function saveAsPNG() {{
    const scale = parseInt(document.getElementById('scaleSelect').value);
    showStatus('📸 Rendering high-resolution PNG...');
    
    const svg = document.querySelector('#diagram svg');
    if (!svg) {{ showStatus('⚠️ Please wait for diagram to render', true); return; }}
    
    // Get original dimensions
    const originalWidth = svg.clientWidth || 800;
    const originalHeight = svg.clientHeight || 600;
    
    // Scale up for high resolution
    const canvas = document.createElement('canvas');
    canvas.width = originalWidth * scale;
    canvas.height = originalHeight * scale;
    const ctx = canvas.getContext('2d');
    
    // Enable high-quality rendering
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    
    const data = new XMLSerializer().serializeToString(svg);
    const img = new Image();
    
    img.onload = () => {{
        // Scale context for high resolution
        ctx.scale(scale, scale);
        ctx.drawImage(img, 0, 0, originalWidth, originalHeight);
        
        // Download
        const png = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = png;
        a.download = `flowclaw_diagram_{scale}x.png`;
        a.click();
        showStatus(`✅ PNG saved at ${scale}x resolution!`);
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

// Handle rendering errors
setTimeout(() => {{
    const svg = document.querySelector('#diagram svg');
    if (!svg) {{
        document.getElementById('diagramContainer').innerHTML = '<div style="text-align:center;padding:40px;color:#dc3545;">⚠️ Diagram rendering error. Check console for details.</div>';
    }}
}}, 3000);
</script>
</body>
</html>'''
    
    @staticmethod
    def create_high_res_viewer(mermaid_code: str, title: str) -> str:
        """Create high-resolution viewer HTML file"""
        html_content = HighResRenderer.generate_html_with_zoom(mermaid_code, title)
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(html_content)
        temp_file.close()
        
        return temp_file.name
