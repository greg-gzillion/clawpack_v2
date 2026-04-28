"""A2A Handler for DraftClaw - Technical Blueprints with FileClaw Export"""
import sys, os
from pathlib import Path
from datetime import datetime

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from shared.security import InputSanitizer
from commands.llm_enhanced import run as llm_run

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("draftclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search technical drawing {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
                # Search chronicle index
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return "\n".join(parts)

    def _call_llm(self, prompt, context=""):
        if context:
            prompt = "Reference context:\n" + context + "\n\n" + prompt
        result = llm_run(prompt)
        return result if result and not result.startswith("Error:") else "Blueprint generation failed"

    def _fileclaw_export(self, fmt, content):
        try:
            safe = content.replace(chr(10), "\n").replace('"', '\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe}", timeout=30)
            if result:
                return result
        except: pass
        # Fallback
        p = PROJECT_ROOT / "exports"; p.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = p / f"draftclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        os.startfile(str(fn))
        return f"Saved: {fn.name}"

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = ""
            try: ctx = self._gather_context(query)
            except: pass

            if cmd in ("/blueprint",) and query:
                from agents.draftclaw.commands.blueprint import run
                result = run(query)
                if result and "Error" not in str(result):
                    export = self._fileclaw_export("png", str(result))
                    result = f"{export}\n\n{str(result)}"
            elif cmd in ("/draw", "/design") and query:
                specs = self._call_llm(f"Generate technical drawing specifications with dimensions for: {query}. Include width, height, elements, layout.", ctx)
                from agents.draftclaw.commands.blueprint import run
                result = run(specs)
                export = self._fileclaw_export("png", str(result))
                result = f"{export}\n\n{specs}"
            elif cmd == "/export" and args:
                parts2 = args.split(maxsplit=1)
                if len(parts2) == 2:
                    result = self._fileclaw_export(parts2[0], parts2[1])
                else:
                    result = "Usage: /export <format> <content>"
            elif cmd == "/help":
                result = "DraftClaw - Technical Blueprints\n  /blueprint <specs> - Generate PIL blueprint + auto-save PNG\n  /draw <description> - AI-generated technical drawing\n  /export <fmt> <content> - Export via FileClaw (21 formats)\n  Formats: pdf, docx, png, jpg, svg, zip, json, csv, yaml, html, md, txt..."
            elif cmd == "/stats":
                result = f"DraftClaw | PIL Blueprints | FileClaw + WebClaw + LLMClaw | Interactions: {self.state.get('interactions', 0)}"
            else:
                specs = self._call_llm(f"Technical drawing specifications: {query}", ctx)
                result = f"Specs generated. Use /blueprint to render.\n\n{specs}"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DraftClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
