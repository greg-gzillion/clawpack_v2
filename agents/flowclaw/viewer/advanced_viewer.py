"""Advanced popup viewer"""
import webbrowser
import tempfile

class AdvancedViewer:
    @staticmethod
    def show(code: str, title: str) -> str:
        html = f'''<!DOCTYPE html>
<html>
<head><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
body{{margin:0;padding:20px;background:linear-gradient(135deg,#667eea,#764ba2);font-family:Arial}}
.container{{max-width:1200px;margin:0 auto;background:white;border-radius:16px;overflow:hidden}}
.header{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:20px}}
.diagram{{padding:30px;text-align:center;background:#f8f9fa}}
button{{padding:10px 20px;margin:5px;border:none;border-radius:8px;cursor:pointer;background:#667eea;color:white}}
.mermaid{{background:white;padding:20px;border-radius:8px;display:inline-block}}
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
mermaid.initialize({{startOnLoad:true,theme:'base'}});
function copyCode(){{navigator.clipboard.writeText(document.querySelector('.mermaid').textContent);alert('Copied!');}}
</script>
</body>
</html>'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            webbrowser.open(f'file://{f.name}')
            return f.name
