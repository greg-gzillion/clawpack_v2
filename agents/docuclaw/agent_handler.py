"""A2A Handler for DocuClaw v5 - Constitutional Document Agent with A2A routing"""
import sys, os, json
from pathlib import Path
from datetime import datetime

DOCUCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCUCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
TEMPLATES_DIR = DOCUCLAW_DIR / "templates"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCUCLAW_DIR))

from shared.base_agent import BaseAgent

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("docuclaw")

    def _list_exports(self, filter_ext=None):
        if not EXPORTS.exists(): return "No exports found."
        files = sorted(EXPORTS.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
        if filter_ext: files = [f for f in files if f.suffix == f".{filter_ext}"]
        if not files: return "No exports found."
        lines = []
        for f in files[:20]:
            size = f.stat().st_size; ts = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"  {f.name} ({size:,} bytes) - {ts}")
        return "\n".join(lines)

    def _list_templates(self, category=None):
        if not TEMPLATES_DIR.exists(): return "No templates found."
        categories = {}
        for d in TEMPLATES_DIR.iterdir():
            if d.is_dir():
                files = list(d.glob("*"))
                if files: categories[d.name] = [f.stem.replace("_"," ").title() for f in files]
        if category and category in categories: return f"Templates: {category}\n" + "\n".join(f"  - {t}" for t in categories[category])
        result = ["Available Template Categories:"]
        for cat, temps in sorted(categories.items()):
            result.append(f"\n  {cat}/ ({len(temps)} templates)")
            for t in temps[:5]: result.append(f"    - {t}")
        return "\n".join(result)

    def _fileclaw_export(self, fmt, content):
        try:
            if fmt=="pdf": content = content.encode("latin-1", errors="replace").decode("latin-1")
            result = self.call_agent("fileclaw", f"/export {fmt} {content.replace(chr(10),'\\n').replace('"','\\"')[:3000]}")
            if result: return result
        except: pass
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S"); fn = EXPORTS/f"docuclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved locally: {fn.name}"

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "DocuClaw v5 - Constitutional Document Agent\n  CREATE: /create /letter /report /memo /resume /proposal\n  IMPORT: /import <file>  EXPORT: /export <fmt> <content>\n  CONVERT: /convert <fmt> <file>  COMBINE: /combine <files>\n  TRANSLATE: /translate <lang> <text>  TEMPLATES: /templates\n  SHARED: /shared read|write  DELEGATE: /delegate <agent> <task>\n  FORMATS: pdf,docx,rtf,md,html,txt,xlsx,pptx,json,csv,yaml,toml,xml,ini,png,jpg,bmp,gif,tiff,webp,svg,zip\n  /stats"
                return {"status":"success","result":result}

            if cmd in ("/stats",): return {"status":"success","result":f"DocuClaw v5 | 21 Formats | Interactions: {self.state.get('interactions',0)}"}

            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","interpretclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            # Document generation
            if cmd in ("/create","/letter","/report","/memo","/resume","/proposal") and query:
                doc_type = cmd.replace("/","")
                parts2 = query.rsplit(" ",1)
                fmt = parts2[-1] if len(parts2)>1 and parts2[-1] in ("pdf","docx","html","md","txt","json","csv","yaml","xml","rtf","pptx","xlsx") else "md"
                if fmt==parts2[-1] and len(parts2)>1: query = parts2[0]
                content = self.ask_llm(f"Create a professional {doc_type} in Markdown format. Include proper formatting, headings, and structure.\n\nTopic: {query}")
                export_result = self._fileclaw_export(fmt, content)
                result = f"{export_result}\n\n{content}"
            elif cmd in ("/exports","/list") and args: result = self._list_exports(args)
            elif cmd in ("/exports","/list"): result = self._list_exports()
            elif cmd in ("/templates","/template"):
                result = self._list_templates(args if args else None)
            elif cmd=="/usetemplate" and args:
                parts2 = args.split(maxsplit=1); cat = parts2[0]
                name = parts2[1] if len(parts2)>1 else ""
                template_path = TEMPLATES_DIR/cat/f"{name}.md" if name else None
                result = f"Template loaded: {cat}/{name}\n\n{template_path.read_text(encoding='utf-8')}" if template_path and template_path.exists() else f"Template not found: {cat}/{name}"
            elif cmd=="/import" and args:
                try:
                    content = Path(args).read_text(encoding="utf-8", errors="replace")
                    result = f"Imported: {args}\n\n{content}"
                except: result = f"File not found: {args}"
            elif cmd=="/export" and args:
                parts2 = args.split(maxsplit=1); fmt = parts2[0]; content = parts2[1] if len(parts2)>1 else ""
                result = self._fileclaw_export(fmt, content) if content else "Usage: /export pdf <content>"
            elif cmd=="/convert" and args:
                parts2 = args.split(maxsplit=2)
                if len(parts2)>=2:
                    target_fmt = parts2[0]; filepath = parts2[1]
                    try:
                        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
                        export_result = self._fileclaw_export(target_fmt, content)
                        result = f"Converted {filepath} to {target_fmt}:\n{export_result}"
                    except: result = f"Cannot read: {filepath}"
                else: result = "Usage: /convert pdf README.md"
            elif cmd=="/combine" and args:
                files = args.split(); combined = []
                for f in files:
                    try: combined.append(f"---\n## From: {f}\n\n{Path(f).read_text(encoding='utf-8', errors='replace')}")
                    except: combined.append(f"---\n## From: {f}\n\n[Could not read]")
                full_content = "\n\n".join(combined)
                export_result = self._fileclaw_export("md", full_content)
                result = f"Combined {len(files)} files:\n{export_result}\n\n{full_content[:1000]}..."
            elif cmd=="/translate" and args:
                parts2 = args.split(maxsplit=1); lang = parts2[0]
                text = parts2[1] if len(parts2)>1 else ""
                if text:
                    translated = self.call_agent("interpretclaw", f"/translate {text} to {lang}")
                    result = f"Translated to {lang}:\n{translated}" if translated else "Translation failed"
                else: result = "Usage: /translate fr <text>"
            elif query:
                content = self.ask_llm(f"Create a well-formatted Markdown document:\n\n{query}")
                export_result = self._fileclaw_export("md", content)
                result = f"{export_result}\n\n{content}"
            else: result = "Type /help for commands"

            from data_io import write_shared
            write_shared("docuclaw_latest", {"command":cmd,"query":query})

            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query","")
            content = self.ask_llm(f"Create a well-formatted Markdown document:\n\n{query}")
            return {"status":"success","result":content}
        except Exception as e: return {"status":"error","result":str(e)}

_agent = DocuClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
