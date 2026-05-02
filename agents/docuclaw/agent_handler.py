"""A2A Handler for DocuClaw - Document Generator with A2A routing"""
import sys, os
from pathlib import Path
from datetime import datetime

DOCUCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCUCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
TEMPLATES_DIR = DOCUCLAW_DIR / "templates"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCUCLAW_DIR))

from shared.base_agent import BaseAgent
from modules.viewer import view_document
from modules.validator import validate_claims, generate_trust_footer

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("docuclaw")

    def _list_exports(self, filter_ext=None):
        """List exported files, newest first."""
        if not EXPORTS.exists():
            return "No exports found."
        files = sorted(EXPORTS.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
        if filter_ext:
            files = [f for f in files if f.suffix == f".{filter_ext}"]
        if not files:
            return "No exports found."
        lines = []
        for f in files[:20]:
            size = f.stat().st_size
            ts = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"  {f.name} ({size:,} bytes) - {ts}")
        return "\n".join(lines)

    def _list_templates(self, category=None):
        """List available templates."""
        if not TEMPLATES_DIR.exists():
            return "No templates found."
        categories = {}
        for d in TEMPLATES_DIR.iterdir():
            if d.is_dir():
                files = list(d.glob("*"))
                if files:
                    categories[d.name] = [f.stem.replace("_", " ").title() for f in files]
        
        if category and category in categories:
            return f"Templates: {category}\n" + "\n".join(f"  - {t}" for t in categories[category])
        
        result = ["Available Template Categories:"]
        for cat, temps in sorted(categories.items()):
            result.append(f"\n  {cat}/ ({len(temps)} templates)")
            for t in temps[:5]:
                result.append(f"    - {t}")
        return "\n".join(result)

    def _to_table(self, content, fmt):
        """Convert markdown content to tabular format for spreadsheet exports"""
        if fmt in ("xlsx", "csv"):
            lines = content.split('\n')
            rows = [{"Section": "Content", "Text": content}]
            current_section = "Header"
            current_text = ""
            for line in lines:
                if line.startswith("# "):
                    if current_text.strip():
                        rows.append({"Section": current_section, "Text": current_text.strip()})
                    current_section = line.replace("# ", "").strip()
                    current_text = ""
                elif line.strip():
                    current_text += line + " "
            if current_text.strip():
                rows.append({"Section": current_section, "Text": current_text.strip()})
            import json
            return json.dumps(rows)
        return content

    def _fileclaw_export(self, fmt, content):
        """Delegate to FileClaw for all format exports"""
        try:
            if fmt == "pdf":
                content = content.encode("latin-1", errors="replace").decode("latin-1")
            content = self._to_table(content, fmt)
            safe_content = content.replace('\n', '\\n').replace('"', '\\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe_content}")
            if result:
                return result
        except:
            pass
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"docuclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved locally: {fn.name}"

    def _fileclaw_import(self, filepath):
        """Import file via FileClaw or read directly"""
        try:
            safe_path = filepath.replace("\\", "/")
            result = self.call_agent("fileclaw", f"/import {safe_path}")
            if result:
                return result
        except:
            pass
        try:
            return Path(filepath).read_text(encoding="utf-8", errors="replace")
        except:
            return None

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Document generation
            if cmd in ("/create", "/letter", "/report", "/memo", "/resume", "/proposal") and query:
                doc_type = cmd.replace("/", "")
                parts2 = query.rsplit(" ", 1)
                fmt = parts2[-1] if len(parts2) > 1 and parts2[-1] in (
                    "pdf","docx","html","md","txt","json","csv","yaml","xml","rtf","pptx","xlsx"
                ) else "md"
                if fmt == parts2[-1] and len(parts2) > 1:
                    query = parts2[0]
                
                content = self.ask_llm(
                    f"Create a professional {doc_type} in Markdown format. Include proper formatting, headings, and structure. Include specific sources, URLs, and citations where possible.\n\nTopic: {query}"
                )
                validation = validate_claims(content)
                if validation["claim_count"] > 0:
                    content += generate_trust_footer(validation)
                export_result = self._fileclaw_export(fmt, content)
                result = f"{export_result}\n\n{content}"

            # List exports
            elif cmd in ("/exports", "/list") and args:
                result = self._list_exports(args)
            elif cmd in ("/exports", "/list"):
                result = self._list_exports()

            # List templates
            elif cmd in ("/templates", "/template"):
                category = args if args else None
                result = self._list_templates(category)

            # Use a template
            elif cmd == "/usetemplate" and args:
                parts2 = args.split(maxsplit=1)
                cat = parts2[0]
                name = parts2[1] if len(parts2) > 1 else ""
                template_path = TEMPLATES_DIR / cat / f"{name}.md" if name else None
                if template_path and template_path.exists():
                    content = template_path.read_text(encoding="utf-8")
                    result = f"Template loaded: {cat}/{name}\n\n{content}"
                else:
                    result = f"Template not found: {cat}/{name}\n\n" + self._list_templates(cat)

            # Import file
            elif cmd == "/import" and args:
                content = self._fileclaw_import(args)
                if content:
                    result = f"Imported: {args}\n\n{content}"
                else:
                    result = f"File not found: {args}\n\nTry /list to see available files"

            # Export content
            elif cmd == "/export" and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0]
                content = parts2[1] if len(parts2) > 1 else ""
                if content:
                    result = self._fileclaw_export(fmt, content)
                else:
                    result = "Usage: /export pdf <content>"

            # Convert file between formats
            elif cmd == "/convert" and args:
                parts2 = args.split(maxsplit=2)
                if len(parts2) >= 2:
                    target_fmt = parts2[0]
                    filepath = parts2[1]
                    p = PROJECT_ROOT / "exports" / filepath
                    if not p.exists():
                        p = Path(filepath)
                    if p.exists():
                        content = p.read_text(encoding="utf-8", errors="replace")
                    else:
                        content = None
                    if content:
                        export_result = self._fileclaw_export(target_fmt, content)
                        view_document(content, title=f"Converted: {Path(filepath).name}")
                        result = f"Converted {filepath} to {target_fmt}:\n{export_result}"
                    else:
                        result = f"Cannot read: {filepath}"
                else:
                    result = "Usage: /convert pdf README.md"

            # Combine multiple files
            elif cmd == "/combine" and args:
                files = args.split()
                combined = []
                for f in files:
                    content = self._fileclaw_import(f)
                    if content:
                        combined.append(f"---\n## From: {f}\n\n{content}")
                    else:
                        combined.append(f"---\n## From: {f}\n\n[Could not read file]")
                
                full_content = "\n\n".join(combined)
                export_result = self._fileclaw_export("md", full_content)
                result = f"Combined {len(files)} files:\n{export_result}\n\n{full_content[:1000]}..."

            # Translate via InterpretClaw
            elif cmd == "/translate" and args:
                parts2 = args.split(maxsplit=1)
                lang = parts2[0]
                text = parts2[1] if len(parts2) > 1 else ""
                if text:
                    translated = self.call_agent("interpretclaw", f"/translate {text} to {lang}")
                    if translated:
                        clean = translated.replace("Exported:", "").strip()
                        export_fn = self._fileclaw_export("md", clean)
                        view_document(clean, title=f"Translation - {lang}")
                        result = f"Translated to {lang}: {export_fn}\n\n{clean}"
                    else:
                        result = "Translation failed"
                else:
                    result = "Usage: /translate fr <text>"

            # Help
            elif cmd == "/help":
                result = """DocuClaw - Universal Document Generator
  CREATE:     /create /letter /report /memo /resume /proposal
  IMPORT:     /import <filepath>
  EXPORT:     /export <format> <content>
  CONVERT:    /convert <format> <filepath>
  COMBINE:    /combine <file1> <file2> ...
  TRANSLATE:  /translate <lang> <text>
  TEMPLATES:  /templates [category]  |  /usetemplate <cat> <name>
  LIST:       /list [format]

  Formats (21): pdf, docx, rtf, md, html, txt, xlsx, pptx,
                json, csv, yaml, toml, xml, ini,
                png, jpg, bmp, gif, tiff, webp, svg, zip"""

            elif cmd == "/stats":
                result = f"DocuClaw | 21 Formats | FileClaw + InterpretClaw | Interactions: {self.state.get('interactions', 0)}"

            # Fallback: any text becomes a document
            elif query:
                content = self.ask_llm(f"Create a well-formatted Markdown document:\n\n{query}")
                export_result = self._fileclaw_export("md", content)
                result = f"{export_result}\n\n{content}"
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DocuClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)