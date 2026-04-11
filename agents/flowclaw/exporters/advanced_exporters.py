"""Additional export formats"""
import json
from pathlib import Path
from datetime import datetime

class AdvancedExporters:
    @staticmethod
    def to_pptx(code: str, output_path: Path, title: str) -> bool:
        html = f'<!DOCTYPE html><html><head><title>{title}</title><script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script></head><body><h1>{title}</h1><pre class="mermaid">{code}</pre><script>mermaid.initialize({{startOnLoad:true}});</script></body></html>'
        output_path.with_suffix('.pptx.html').write_text(html)
        return True
    
    @staticmethod
    def to_markdown_doc(code: str, output_path: Path, title: str) -> bool:
        md = f"# {title}\n\n```mermaid\n{code}\n```\n\n**Generated:** {datetime.now()}\n"
        output_path.with_suffix('.md').write_text(md)
        return True
    
    @staticmethod
    def to_json_export(code: str, output_path: Path, title: str) -> bool:
        data = {'title': title, 'code': code, 'generated': datetime.now().isoformat()}
        output_path.with_suffix('.json').write_text(json.dumps(data, indent=2))
        return True
