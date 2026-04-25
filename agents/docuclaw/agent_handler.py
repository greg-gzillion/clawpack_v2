"""A2A Handler for DocuClaw - Document Generator via FileClaw + WebClaw + LLMClaw"""
import sys, os, requests
from pathlib import Path
from datetime import datetime

DOCUCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCUCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
A2A_URL = "http://127.0.0.1:8766"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCUCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from commands.llm_enhanced import run as llm_run

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("docuclaw")

    def _call_llm(self, prompt, context=""):
        if context:
            prompt = "Reference context:\n" + context[:1500] + "\n\n" + prompt
        result = llm_run(prompt)
        return result if result and not result.startswith("Error:") else "Document generation failed"

    def _to_table(self, content, fmt):
        # Convert markdown content to tabular format for spreadsheet exports
        if fmt in ("xlsx", "csv"):
            lines = content.split(chr(10))
            rows = [{"Section": "Content", "Text": content[:500]}]
            # Try to parse markdown sections into rows
            current_section = "Header"
            current_text = ""
            for line in lines:
                if line.startswith("# "):
                    if current_text.strip():
                        rows.append({"Section": current_section, "Text": current_text.strip()[:200]})
                    current_section = line.replace("# ", "").strip()
                    current_text = ""
                elif line.strip():
                    current_text += line + " "
            if current_text.strip():
                rows.append({"Section": current_section, "Text": current_text.strip()[:200]})
            import json
            return json.dumps(rows)
        return content

    def _fileclaw_export(self, fmt, content):
        """Delegate to FileClaw for all format exports"""
        try:
            # Strip emojis and non-latin1 chars for PDF (fpdf limitation)
            if fmt == "pdf":
                content = content.encode("latin-1", errors="replace").decode("latin-1")
            # Escape special chars for JSON-safe A2A transport
            content = self._to_table(content, fmt)
            safe_content = content.replace(chr(10), "\n").replace('"', '\"')
            r = requests.post(f"{A2A_URL}/v1/message/fileclaw",
                json={"task": f"/export {fmt} {safe_content}"}, timeout=30)
            if r.status_code == 200:
                return r.json().get("result", f"Exported as {fmt}")
        except:
            pass
        # Fallback: save directly
        from pathlib import Path
        p = PROJECT_ROOT / "exports"
        p.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = p / f"docuclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        os.startfile(str(fn))
        return f"Saved locally: {fn.name}"

    def _fileclaw_import(self, filepath):
        """Delegate to FileClaw for all format imports"""
        try:
            safe_path = filepath.replace(chr(92), "/")
            r = requests.post(f"{A2A_URL}/v1/message/fileclaw",
                json={"task": f"/import {safe_path}"}, timeout=30)
            if r.status_code == 200:
                return r.json().get("result", "")
        except:
            pass
        # Fallback: read directly
        try:
            return Path(filepath).read_text(encoding="utf-8", errors="replace")
        except:
            return f"Cannot read: {filepath}"

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = ""
            try: ctx = self.search_web(query, max_results=3)
            except: pass

            # Document generation
            if cmd in ("/create", "/letter", "/report", "/memo", "/resume", "/proposal") and query:
                doc_type = cmd.replace("/", "")
                fmt = args.split()[-1] if args.split()[-1] in ("pdf","docx","html","md","txt","json","csv","yaml","xml","rtf","pptx","xlsx") else "md"
                content = self._call_llm(f"Create a professional {doc_type} in Markdown format for: {query}", ctx)
                export_result = self._fileclaw_export(fmt, content)
                result = f"{export_result}\n\n{content[:600]}"

            # Import any file via FileClaw
            elif cmd == "/import" and args:
                content = self._fileclaw_import(args)
                result = f"Imported: {args}\n\n{content[:1000]}"

            # Export content in any format via FileClaw
            elif cmd == "/export" and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0]
                content = parts2[1] if len(parts2) > 1 else ""
                if content:
                    result = self._fileclaw_export(fmt, content)
                else:
                    result = "Usage: /export <format> <content>"

                        # Translate document via InterpretClaw
            elif cmd == "/translate" and args:
                parts2 = args.split(maxsplit=1)
                lang = parts2[0]
                text = parts2[1] if len(parts2) > 1 else ""
                if text:
                    try:
                        r = requests.post(f"{A2A_URL}/v1/message/interpretclaw",
                            json={"task": f"/translate {text} to {lang}"}, timeout=60)
                        if r.status_code == 200:
                            result = r.json().get("result", "")
                            translated = result.replace("Exported:", "").strip()
                            # Save translated version
                            fmt = "md"
                            fn = self._fileclaw_export(fmt, translated).replace("Exported: ", "")
                            result = f"Translated to {lang}: {fn}\n\n{translated[:800]}"
                        else:
                            result = f"Translation failed: {r.status_code}"
                    except Exception as e:
                        result = f"Translation error: {e}"
                else:
                    result = "Usage: /translate <lang_code> <text>\nExample: /translate es Hello world"
            elif cmd == "/help":
                result = "DocuClaw - Universal Document Generator via FileClaw\n\n  GENERATE + AUTO-SAVE:\n    /letter <topic> [format]\n    /report <topic> [format]\n    /memo <topic> [format]\n    /resume <topic> [format]\n    /proposal <topic> [format]\n    /create <topic> [format]\n\n  IMPORT (via FileClaw):\n    /import <filepath>\n\n  EXPORT (via FileClaw):\n    /export <format> <content>\n\n  SUPPORTED FORMATS (21):\n    Documents:  pdf, docx, rtf, md, html, txt\n    Office:     xlsx, pptx\n    Data:       json, csv, yaml, toml, xml, ini\n    Images:     png, jpg, bmp, gif, tiff, webp\n    Vector:     svg\n    Archive:    zip"
            elif cmd == "/stats":
                result = f"DocuClaw | FileClaw + WebClaw + LLMClaw | Interactions: {self.state.get('interactions', 0)}"
            else:
                content = self._call_llm(f"Create a document: {query}", ctx)
                export_result = self._fileclaw_export("md", content)
                result = f"{export_result}\n\n{content[:600]}"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DocuClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
