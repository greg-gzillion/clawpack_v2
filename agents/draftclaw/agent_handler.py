"""A2A Handler for DraftClaw - Technical Blueprint Generator with PIL"""
import sys
from pathlib import Path

DRAFTCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))

from shared.base_agent import BaseAgent

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('draftclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/blueprint", "blueprint") and query:
                from commands.blueprint import run
                result = run(query)
            elif cmd in ("/help",):
                result = "DraftClaw - Technical Blueprints\n  /blueprint 800x600 floor plan\n  /blueprint 1200x800 garage workshop\n  /stats"
            elif cmd in ("/stats",):
                result = f"DraftClaw | PIL Blueprint Generator | Grid/Border/Title Block | Interactions: {self.state.get('interactions', 0)}"
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Technical drawing specifications for: {query}").get("result","")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DraftClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
