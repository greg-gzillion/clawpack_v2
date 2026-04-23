"""A2A Handler for DraftClaw - Technical Drawings & Blueprints"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class DraftClawAgent(BaseAgent):
    def __init__(self): super().__init__('draftclaw')
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = self.search_web(f"technical drawing {query}", max_results=3)
            if cmd in ("/blueprint","blueprint") and query: result = self.ask_llm(f"Context: {ctx}\n\nCreate technical blueprint with dimensions, materials: {query}")
            elif cmd in ("/cad","cad") and query: result = self.ask_llm(f"Context: {ctx}\n\nCAD technical drawing with measurements: {query}")
            elif cmd in ("/floorplan","floorplan") and query: result = self.ask_llm(f"Context: {ctx}\n\nFloor plan layout with room dimensions: {query}")
            elif cmd in ("/help",): result = "DraftClaw - Technical Drawings\n  /blueprint /cad /floorplan /stats"
            elif cmd in ("/stats",): result = f"DraftClaw | Technical Drawings | Interactions: {self.state.get('interactions', 0)}"
            else: result = self.ask_llm(f"Context: {ctx}\n\nTechnical drawing expert: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = DraftClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
