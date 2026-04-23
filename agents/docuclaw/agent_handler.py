"""A2A Handler for DocuClaw - Document Generator"""
import sys, os
from pathlib import Path
from datetime import datetime

DOCUCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = DOCUCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCUCLAW_DIR))

from shared.base_agent import BaseAgent
EXPORTS = PROJECT_ROOT / "exports"

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('docuclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/create", "/letter", "/report", "/memo") and query:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Create a professional {cmd.replace('/','')} in Markdown format: {query}").get("result","")
                # Save to exports
                filename = f"{cmd.replace('/','')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                path = EXPORTS / filename
                path.write_text(result, encoding='utf-8')
                os.startfile(str(path))
                result = f"Document saved: {filename}\nOpening...\n\n{result[:500]}"
            elif cmd in ("/help",):
                result = "DocuClaw - Document Generator\n  /create /letter /report /memo /resume /stats"
            elif cmd in ("/stats",):
                result = f"DocuClaw | Documents to exports/ | Interactions: {self.state.get('interactions', 0)}"
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Create document: {query}").get("result","")
                filename = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                (EXPORTS / filename).write_text(result, encoding='utf-8')
                os.startfile(str(EXPORTS / filename))

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DocuClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
