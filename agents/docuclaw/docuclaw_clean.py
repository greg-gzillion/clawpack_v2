#!/usr/bin/env python3
"""DocuClaw - Clean Document Processor with Media Support"""

import sys
import json
import csv
import shutil
import webbrowser
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path(__file__).parent / "output"
IMPORT_DIR = Path(__file__).parent / "imports"
EXPORT_DIR = Path(__file__).parent / "exports"
MEDIA_DIR = Path(__file__).parent / "media"

for dir_path in [OUTPUT_DIR, IMPORT_DIR, EXPORT_DIR, MEDIA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================================================
# TEMPLATES
# ============================================================================

TEMPLATES = {
    'letter': """[Date]

[Recipient Name]
[Recipient Title]
[Company Name]
[Address]

Dear [Recipient Name],

[Body of the letter]

Sincerely,

[Your Name]
[Your Title]""",

    'report': """# Report Title

## Executive Summary
[Summary]

## Introduction
[Background]

## Findings
[Results]

## Recommendations
[Actions]""",

    'memo': """TO: [Recipients]
FROM: [Your Name]
DATE: [Date]
SUBJECT: [Subject]

[Body]

Action Items:
- [ ] Item 1
- [ ] Item 2""",

    'meeting_notes': """# Meeting Notes

**Date:** [Date]
**Attendees:** [Names]

## Agenda
1. [Topic]

## Notes
[Discussion]

## Action Items
| Task | Owner | Due |
|------|-------|-----|
| [Task] | [Name] | [Date] |"""
}

# ============================================================================
# MEDIA HANDLER
# ============================================================================

class MediaHandler:
    @staticmethod
    def import_image(file_path: str) -> Dict:
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        dest = MEDIA_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
        shutil.copy2(path, dest)
        
        return {
            'type': 'image',
            'original': str(path),
            'saved': str(dest),
            'embed_md': f"![{path.stem}]({dest.name})",
            'embed_html': f'<img src="{dest.name}" style="max-width:100%">'
        }
    
    @staticmethod
    def import_csv(file_path: str) -> Dict:
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        data = []
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return {
            'type': 'csv',
            'original': str(path),
            'rows': len(data),
            'columns': list(data[0].keys()) if data else [],
            'data': data[:5]
        }
    
    @staticmethod
    def import_json(file_path: str) -> Dict:
        path = Path(file_path)
        if not path.exists():
            return {'error': f'File not found: {file_path}'}
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        return {
            'type': 'json',
            'original': str(path),
            'size': len(data) if isinstance(data, list) else 1,
            'data': data[:5] if isinstance(data, list) else data
        }

# ============================================================================
# DOCUMENT HANDLER
# ============================================================================

class DocumentHandler:
    @staticmethod
    def create_from_template(template: str, values: Dict = None) -> str:
        if template not in TEMPLATES:
            return None
        
        content = TEMPLATES[template]
        if values:
            for key, val in values.items():
                content = content.replace(f"[{key}]", val)
        
        return content
    
    @staticmethod
    def save_document(content: str, name: str) -> Path:
        filename = OUTPUT_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filename.write_text(content)
        return filename

# ============================================================================
# MAIN AGENT
# ============================================================================

class DocuClaw:
    def __init__(self):
        self.media = MediaHandler()
        self.doc = DocumentHandler()
    
    def create(self, template: str) -> str:
        if template not in TEMPLATES:
            return f"❌ Unknown template. Available: {', '.join(TEMPLATES.keys())}"
        
        print(f"\n📝 Creating '{template}' document...")
        print("Enter values (press Enter to skip):\n")
        
        # Find placeholders
        content = TEMPLATES[template]
        import re
        placeholders = set(re.findall(r'\[([^\]]+)\]', content))
        
        values = {}
        for p in placeholders:
            val = input(f"  {p}: ").strip()
            if val:
                values[p] = val
        
        final = self.doc.create_from_template(template, values)
        path = self.doc.save_document(final, template)
        
        return f"✅ Document saved: {path}"
    
    def import_media(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        suffix = path.suffix.lower()
        
        if suffix in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']:
            result = self.media.import_image(file_path)
            if 'error' in result:
                return f"❌ {result['error']}"
            return f"""✅ Image imported!
📁 Saved: {result['saved']}
📝 Markdown: {result['embed_md']}"""
        
        elif suffix == '.csv':
            result = self.media.import_csv(file_path)
            return f"""✅ CSV imported!
📊 Rows: {result['rows']}
📋 Columns: {', '.join(result['columns'])}"""
        
        elif suffix == '.json':
            result = self.media.import_json(file_path)
            return f"""✅ JSON imported!
📦 Items: {result['size']}"""
        
        else:
            return f"❌ Unsupported format: {suffix}"
    
    def export(self, file_path: str, format: str = "pdf") -> str:
        path = Path(file_path)
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        content = path.read_text()
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{path.stem}</title>
<style>body{{font-family:Arial;margin:40px;line-height:1.6}}</style>
</head>
<body>
{content.replace(chr(10), '<br>')}
<p style="margin-top:50px;font-size:10px;color:#999">Generated by DocuClaw</p>
</body>
</html>"""
        
        out_path = EXPORT_DIR / f"{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        out_path.write_text(html)
        
        if format == "pdf":
            webbrowser.open(f'file://{out_path}')
            return f"✅ HTML opened - use browser print to save as PDF"
        
        return f"✅ Exported to: {out_path}"
    
    def list_templates(self) -> str:
        return "📋 Templates:\n" + "\n".join(f"  • {t}" for t in TEMPLATES.keys())
    
    def help(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════╗
║                    DOCUCLAW - Document Processor             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  COMMANDS:                                                   ║
║    create <template>     - Create a document                ║
║    import-media <file>   - Import image/CSV/JSON            ║
║    export <file> [format] - Export to HTML/PDF              ║
║    templates             - List templates                   ║
║    help                  - This help                        ║
║                                                              ║
║  TEMPLATES: letter, report, memo, meeting_notes             ║
║                                                              ║
║  EXAMPLES:                                                   ║
║    python docuclaw.py create letter                         ║
║    python docuclaw.py import-media image.png                ║
║    python docuclaw.py import-media data.csv                 ║
║    python docuclaw.py export document.md pdf                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
    
    def process(self, cmd: str, *args):
        if cmd == "create" and args:
            return self.create(args[0])
        elif cmd == "import-media" and args:
            return self.import_media(args[0])
        elif cmd == "export" and args:
            format = args[1] if len(args) > 1 else "html"
            return self.export(args[0], format)
        elif cmd == "templates":
            return self.list_templates()
        else:
            return self.help()

def main():
    agent = DocuClaw()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    result = agent.process(sys.argv[1], *sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
