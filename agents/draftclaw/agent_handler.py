"""A2A Handler for DraftClaw - Technical Blueprints with FileClaw Export"""
import sys, os, requests
from pathlib import Path
from datetime import datetime

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
A2A_URL = "http://127.0.0.1:8766"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from commands.llm_enhanced import run as llm_run

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("draftclaw")

    def _call_llm(self, prompt, context=""):
        if context:
            prompt = "Reference context:\n" + context[:1500] + "\n\n" + prompt
        result = llm_run(prompt)
        return result if result and not result.startswith("Error:") else "Blueprint generation failed"

    def _fileclaw_export(self, fmt, content):
        try:
            safe = content.replace(chr(10), "\n").replace('"', '\"')
            r = requests.post(f"{A2A_URL}/v1/message/fileclaw",
                json={"task": f"/export {fmt} {safe}"}, timeout=30)
            if r.status_code == 200:
                return r.json().get("result", f"Exported as {fmt}")
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
            try: ctx = self.search_web(query, max_results=3)
            except: pass

            if cmd in ("/blueprint",) and query:
                from agents.draftclaw.commands.blueprint import run
                result = run(query)
                if result and "Error" not in str(result):
                    export = self._fileclaw_export("png", str(result))
                    result = f"{export}\n\n{str(result)[:500]}"
            elif cmd in ("/draw", "/design") and query:
                specs = self._call_llm(f"Generate technical drawing specifications with dimensions for: {query}. Include width, height, elements, layout.", ctx)
                from agents.draftclaw.commands.blueprint import run
                result = run(specs)
                export = self._fileclaw_export("png", str(result))
                result = f"{export}\n\n{specs[:500]}"
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
                result = f"Specs generated. Use /blueprint to render.\n\n{specs[:800]}"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DraftClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
