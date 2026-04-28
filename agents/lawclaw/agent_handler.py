"""A2A Handler for LawClaw - Law Research Agent with A2A + chronicle"""
import sys
import webbrowser
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent

class LawClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/help", "help"):
                result = "LawClaw - /ask /case /statute /contract /court /open /draft /help /stats"
            elif cmd == "/stats":
                result = f"LawClaw | Interactions: {self.state.get('interactions', 0)}"
            elif cmd == "/court" and query:
                result = self.ask_llm(query)
                results = self.search_chronicle(query, limit=5)
                for c in results:
                    u = c.get('url') if isinstance(c, dict) else None
                    if u and isinstance(u, str) and u.startswith('http'):
                        webbrowser.open(u, new=2)
                        result = f"[Opened: {u}]\n\n{result}"
                        break
            elif cmd == "/open" and query:
                results = self.search_chronicle(query, limit=5)
                for c in results:
                    u = c.get('url') if isinstance(c, dict) else None
                    if u and isinstance(u, str) and u.startswith('http'):
                        webbrowser.open(u, new=2)
                        result = f"Opened: {u}"
                        break
                else:
                    result = f"No URL for: {query}"
            elif cmd in ("/ask", "/case", "/statute", "/contract") and query:
                result = self.ask_llm(query)
            elif cmd == "/draft" and query:
                result = self.call_agent("draftclaw", f"/draft {query}", timeout=30)
            elif query:
                result = self.ask_llm(query)
            else:
                result = "Type /help for commands"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LawClawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)