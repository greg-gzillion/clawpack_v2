"""A2A Handler for RustyPyCraw - Code Crawler & Analyzer"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class RustyPyCrawAgent(BaseAgent):
    def __init__(self): super().__init__('rustypycraw')
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = self.search_web(f"code analysis {query}", max_results=3)
            if cmd in ("/crawl","/scan","/analyze") and query: result = self.ask_llm(f"Context: {ctx}\n\nCode analysis for {cmd}: {query}")
            elif cmd in ("/help",): result = "RustyPyCraw - Code Crawler\n  /crawl /scan /analyze /stats"
            elif cmd in ("/stats",): result = f"RustyPyCraw | Code Analysis | Interactions: {self.state.get('interactions', 0)}"
            else: result = self.ask_llm(f"Context: {ctx}\n\nCode expert: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = RustyPyCrawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
