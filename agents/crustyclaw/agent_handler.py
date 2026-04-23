"""A2A Handler for CrustyClaw - Rust AI Shell (BaseAgent)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class CrustyClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('crustyclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/code", "/rust") and query:
                result = self.ask_llm(f"Write clean Rust code with comments for: {query}")
            elif cmd in ("/explain") and query:
                result = self.ask_llm(f"Explain this Rust concept clearly: {query}")
            elif cmd in ("/fix", "/debug") and query:
                result = self.ask_llm(f"Fix this Rust code, return fixed code only: {query}")
            elif cmd in ("/help",):
                result = "/code <task> | /explain <concept> | /fix <code> | /stats"
            elif cmd in ("/stats",):
                result = f"CrustyClaw | BaseAgent | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Rust expert. Question: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = CrustyClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
