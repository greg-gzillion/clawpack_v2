"""A2A Handler for PlotClaw - Charts & Graphs"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class PlotClawAgent(BaseAgent):
    def __init__(self): super().__init__('plotclaw')
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = self.search_web(f"chart visualization {query}", max_results=3)
            if cmd in ("/bar","/pie","/line","/scatter") and query: result = self.ask_llm(f"Context: {ctx}\n\nChart configuration with data, labels, colors for {cmd}: {query}")
            elif cmd in ("/help",): result = "PlotClaw - Charts\n  /bar /pie /line /scatter /stats"
            elif cmd in ("/stats",): result = f"PlotClaw | Charts/Graphs | Interactions: {self.state.get('interactions', 0)}"
            else: result = self.ask_llm(f"Context: {ctx}\n\nData visualization: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = PlotClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
