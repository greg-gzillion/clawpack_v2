"""A2A Handler for MedicLaw - Medical references via WebClaw + LLMClaw"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MEDICLAW_DIR))

# Use full path to avoid circular import issues
from agents.mediclaw.core.engine import MedicalEngine
from shared.base_agent import BaseAgent

class MedicLawAgent(BaseAgent):
    def __init__(self):
        super().__init__('mediclaw')
        self.engine = MedicalEngine()

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "/diagnose" and args:
                result = self.engine.diagnose(args)
            elif cmd == "/treatment" and args:
                result = self.engine.treatment(args)
            elif cmd == "/research" and args:
                result = self.engine.research(args)
            elif cmd == "/med" and args:
                result = self.engine.research(args)
            elif cmd == "/sources":
                sources = self.engine.list_sources()
                result = f"Medical Sources ({len(sources)}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(sources, 1))
            elif cmd == "/help":
                result = "MedicLaw - Medical Reference Agent\n  /med /diagnose /treatment /research /sources /stats"
            elif cmd == "/stats":
                result = f"MedicLaw | Medical References | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.smart_ask(f"Medical information: {task}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = MedicLawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
