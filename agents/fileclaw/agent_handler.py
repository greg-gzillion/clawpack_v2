"""A2A Handler for FileClaw - File Analysis & Organization"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class FileClawAgent(BaseAgent):
    def __init__(self): super().__init__('fileclaw')
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/find","find") and query:
                result = self.search_web(query, max_results=5)
            elif cmd in ("/analyze","/organize") and query:
                ctx = self.search_web(f"file {query}", max_results=3)
                result = self.ask_llm(f"Context: {ctx}\nFile analysis: {query}")
            elif cmd in ("/help",): result = "FileClaw\n  /find /analyze /organize /stats"
            elif cmd in ("/stats",): result = f"FileClaw | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self.search_web(query, max_results=3)
                result = self.ask_llm(f"Context: {ctx}\nFile analysis: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = FileClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
