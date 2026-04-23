"""A2A Handler for DataClaw - Local Reference Manager"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class DataClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('dataclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/search", "search") and query:
                # Search chronicle + local references
                chronicle = self.search_chronicle(query, limit=5)
                web = self.search_web(query, max_results=3)
                result = f"Results for '{query}':\n"
                if chronicle:
                    result += "\n[Chronicle]\n" + "\n".join(f"  - {c.url}" for c in chronicle)
                result += f"\n[WebClaw]\n{web[:500]}"
                if not chronicle and not web.strip():
                    result = f"No results for '{query}'. Add references with /add."
            elif cmd in ("/add", "add") and query:
                self.learn_fact(f"dataclaw_ref: {query}")
                result = f"Reference added: {query}\nLocal index will expand as you add documents."
            elif cmd in ("/list", "list"):
                facts = self.get_facts()
                refs = [k.replace('dataclaw_ref: ','') for k in facts if 'dataclaw_ref' in k]
                result = f"Local References ({len(refs)}):\n" + "\n".join(f"  - {r}" for r in refs) if refs else "No local references yet. Use /add to add."
            elif cmd in ("/help",):
                result = "DataClaw - Local Reference Manager\n  /search <query> - Search chronicle + WebClaw\n  /add <reference> - Add local reference\n  /list - List all local references\n  /stats"
            elif cmd in ("/stats",):
                result = f"DataClaw | Local Reference Manager | Chronicle + WebClaw | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.search_web(query, max_results=5) or f"Searching: {query}"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DataClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
