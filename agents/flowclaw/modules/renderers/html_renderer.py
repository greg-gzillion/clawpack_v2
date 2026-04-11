"""HTML renderer module"""
import webbrowser
import tempfile

class HTMLRenderer:
    @staticmethod
    def render(code, title):
        html = f"""<!DOCTYPE html>
<html>
<head><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
body{{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px}}
.container{{max-width:1200px;margin:0 auto;background:white;border-radius:16px}}
.header{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:20px}}
.diagram{{padding:30px;text-align:center}}
button{{padding:10px20px;margin:5px;border:none;border-radius:8px;cursor:pointer;background:#667eea;color:white}}
.mermaid{{background:white;padding:20px;display:inline-block}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>🎨 {title}</h1></div>
<div class="diagram"><pre class="mermaid">{code}</pre></div>
<div class="diagram">
<button onclick="copyCode()">📋 Copy</button>
<button onclick="window.print()">🖨️ Print</button>
</div>
</div>
<script>
mermaid.initialize({{startOnLoad:true}});
function copyCode(){{navigator.clipboard.writeText(document.querySelector('.mermaid').textContent);alert('Copied!');}}
</script>
</body>
</html>"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html)
            webbrowser.open(f'file://{f.name}')
        return True
