"""A2A Handler for PlotClaw - Chart Generator with matplotlib"""
import sys
from pathlib import Path

PLOTCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = PLOTCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PLOTCLAW_DIR))

from shared.base_agent import BaseAgent

class PlotClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('plotclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search chart data {query}", timeout=15)
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

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/bar", "bar") and query:
                from agents.plotclaw.commands.bar import run
                result = run(query)
            elif cmd in ("/pie", "pie") and query:
                from agents.plotclaw.commands.pie import run
                result = run(query)
            elif cmd in ("/plot", "plot") and query:
                from agents.plotclaw.commands.plot import run
                result = run(query)
            elif cmd in ("/help",):
                result = "PlotClaw - Real Charts (matplotlib)\n  /bar 10,20,15,30,25\n  /pie 15,25,35,25\n  /plot sin(x)\n  /stats"
            elif cmd in ("/stats",):
                result = f"PlotClaw | matplotlib charts | Bar/Pie/Plot | Exports to PNG | Interactions: {self.state.get('interactions', 0)}"
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Chart visualization: {query}").get("result","")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = PlotClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
