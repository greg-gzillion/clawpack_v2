"""A2A Handler for DesignClaw - Brand & Design with Auto-Save HTML"""
import sys
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DESIGNCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from shared.security import InputSanitizer
from commands.llm_enhanced import run as llm_run

class DesignClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("designclaw")

    def _call_llm(self, prompt):
        result = llm_run(prompt)
        return result if result and not result.startswith("Error:") else "Design generation failed"

    def _save_html(self, content, name):
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name or 'design'}_{ts}.html"
        fn = InputSanitizer.sanitize_filename(fn)
        path = EXPORTS / fn
        html = f"<html><head><meta charset='utf-8'><title>{name or 'Design'}</title><style>body{{font-family:Arial;max-width:800px;margin:40px auto;padding:20px;background:#1a1a2e;color:#eee}}h1{{color:#4a9eff}}pre{{background:#16213e;padding:15px;border-radius:8px;white-space:pre-wrap}}</style></head><body><h1>{name or 'DesignClaw Export'}</h1><pre>{content}</pre></body></html>"
        path.write_text(html, encoding="utf-8")
        return fn

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        try:
            if cmd == "/brand" and args:
                result = self._call_llm(f"Create a complete brand identity for: {args}. Include name, logo concept, colors, typography, brand voice.")
                fn = self._save_html(result, args[:40].replace("/","").replace(" ","_"))
                result = f"Saved: {fn}\n\n?? BRAND IDENTITY\n\n{result}"
            elif cmd == "/mood" and args:
                result = self._call_llm(f"Describe a mood board direction for: {args}. Include vibe, color story, texture, imagery style.")
                fn = self._save_html(result, args[:40].replace("/","").replace(" ","_"))
                result = f"Saved: {fn}\n\n?? MOOD BOARD\n\n{result}"
            elif cmd == "/colors" and args:
                result = self._call_llm(f"Create a color palette for: {args}. Provide 4-5 hex codes with names and usage notes.")
                fn = self._save_html(result, args[:40].replace("/","").replace(" ","_"))
                result = f"Saved: {fn}\n\n?? COLOR PALETTE\n\n{result}"
            elif cmd == "/logo" and args:
                result = self._call_llm(f"Design a logo concept for: {args}. Describe the symbol, wordmark, colors, and style.")
                fn = self._save_html(result, args[:40].replace("/","").replace(" ","_"))
                result = f"Saved: {fn}\n\n? LOGO CONCEPT\n\n{result}"
            elif cmd == "/slogan" and args:
                result = self._call_llm(f"Create brand copy for: {args}. Provide tagline, value proposition, and brand voice.")
                fn = self._save_html(result, args[:40].replace("/","").replace(" ","_"))
                result = f"Saved: {fn}\n\n?? BRAND COPY\n\n{result}"
            elif cmd == "/help":
                result = "DesignClaw - Brand & Design\n  /brand /mood /colors /logo /slogan /stats\n  All results auto-saved to exports/ as HTML"
            elif cmd == "/stats":
                result = f"DesignClaw | Auto-save HTML | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.smart_ask(f"Design advice: {task}")
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DesignClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
