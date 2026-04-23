"""A2A Handler for DesignClaw - Brand & Design Generator"""
import sys, os
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
EXPORTS = PROJECT_ROOT / "exports"

from shared.base_agent import BaseAgent

class DesignClawAgent(BaseAgent):
    def __init__(self): super().__init__('designclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/brand", "/mood", "/colors", "/logo", "/slogan") and query:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Create {cmd.replace('/','')} design concept: {query}").get("result","")
                filename = f"{cmd.replace('/','')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                html = f"<html><head><title>{cmd} - {query[:50]}</title><style>body{{font-family:Arial;max-width:800px;margin:40px auto;padding:20px;background:#1a1a2e;color:#eee}}h1{{color:#4a9eff}}pre{{background:#16213e;padding:15px;border-radius:8px}}</style></head><body><h1>{cmd}: {query[:60]}</h1><pre>{result}</pre></body></html>"
                path = EXPORTS / filename
                path.write_text(html, encoding='utf-8')
                os.startfile(str(path))
                result = f"Design saved: {filename}\nOpening..."
            elif cmd in ("/help",): result = "DesignClaw - Design Generator\n  /brand /mood /colors /logo /slogan /stats"
            elif cmd in ("/stats",): result = f"DesignClaw | Designs to exports/ | Interactions: {self.state.get('interactions', 0)}"
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Design concept: {query}").get("result","")

            return {"status": "success", "result": str(result)}
        except Exception as e: return {"status": "error", "result": str(e)}

_agent = DesignClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
