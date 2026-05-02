"""DocuClaw Viewer - Opens documents as rendered HTML in browser."""
import tempfile
import subprocess
import html as _html
from pathlib import Path

def markdown_to_html(content, title="Document"):
    """Convert markdown to styled HTML. No JS dependencies."""
    lines = content.split(chr(10))
    parts = [
        '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>' + _html.escape(title) + '</title>',
        '<style>',
        'body{font-family:Arial;margin:20px;background:#f5f6fa}',
        '.container{max-width:900px;margin:0 auto;background:white;border-radius:12px;padding:30px 40px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}',
        'h1{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:8px}',
        'h2{color:#34495e;margin-top:24px}h3{color:#555;margin-top:16px}',
        'p{line-height:1.6;color:#333}',
        'pre{background:#1e1e1e;color:#d4d4d4;padding:15px;border-radius:8px;overflow-x:auto}',
        'code{background:#f0f0f0;padding:2px 6px;border-radius:4px}',
        'table{border-collapse:collapse;width:100%;margin:15px 0}',
        'th,td{border:1px solid #ddd;padding:10px;text-align:left}',
        'th{background:#3498db;color:white}',
        'blockquote{border-left:4px solid #3498db;padding-left:15px;color:#666;margin:15px 0}',
        'hr{border:none;border-top:1px solid #ddd;margin:20px 0}',
        '</style></head><body><div class="container">'
    ]
    
    in_code = False
    for line in lines:
        escaped = _html.escape(line)
        if line.startswith('`'):
            in_code = not in_code
            parts.append('</pre>' if not in_code else '<pre>')
        elif in_code:
            parts.append(escaped)
        elif line.startswith('# '):
            parts.append('<h1>' + escaped[2:] + '</h1>')
        elif line.startswith('## '):
            parts.append('<h2>' + escaped[3:] + '</h2>')
        elif line.startswith('### '):
            parts.append('<h3>' + escaped[4:] + '</h3>')
        elif line.startswith('|'):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if all(c.replace('-','').replace(':','').strip() == '' for c in cells):
                continue
            tag = 'th' if line.strip().startswith('|') and parts[-1].endswith('</tr>') == False else 'td'
            parts.append('<tr>' + ''.join('<' + tag + '>' + c + '</' + tag + '>' for c in cells) + '</tr>')
        elif line.startswith('- ') or line.startswith('* '):
            parts.append('<li>' + escaped[2:] + '</li>')
        elif line.startswith('> '):
            parts.append('<blockquote>' + escaped[2:] + '</blockquote>')
        elif line.strip() == '---':
            parts.append('<hr>')
        elif line.strip():
            parts.append('<p>' + escaped + '</p>')
    
    parts.append('</div></body></html>')
    return chr(10).join(parts)

def open_in_browser(html_content):
    """Write HTML to temp file and open in default browser."""
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
    tmp.write(html_content)
    tmp.close()
    subprocess.Popen(['cmd','/c','start','',tmp.name], shell=True)
    return tmp.name

def view_document(content, title="Document"):
    """Convert markdown to HTML and open in browser. Returns temp file path."""
    html = markdown_to_html(content, title)
    return open_in_browser(html)

def view_file(filepath):
    """Read a file and open it in browser. Supports .md, .html, .txt."""
    path = Path(filepath)
    if not path.exists():
        return None
    text = path.read_text(encoding='utf-8', errors='replace')
    if path.suffix == '.html':
        return open_in_browser(text)
    else:
        return view_document(text, title=path.name)

__all__ = ['markdown_to_html', 'open_in_browser', 'view_document', 'view_file']
