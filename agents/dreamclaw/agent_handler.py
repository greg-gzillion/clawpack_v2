"""A2A Handler for DreamClaw - AI Vision & Generation"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class DreamClawAgent(BaseAgent):
    def __init__(self): super().__init__('dreamclaw')
    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search creative {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = self._gather_context(query)
            if cmd in ("/dream","dream") and query: result = self.ask_llm(f"Context: {ctx}\n\nAI image generation prompt with style, lighting, composition: {query}")
            elif cmd in ("/imagine","imagine") and query: result = self.ask_llm(f"Context: {ctx}\n\nCreative visual description for AI generation: {query}")
            elif cmd in ("/help",): result = "DreamClaw - AI Vision\n  /dream /imagine /style /stats"
            elif cmd in ("/stats",): result = f"DreamClaw | AI Vision | Interactions: {self.state.get('interactions', 0)}"
            else: result = self.ask_llm(f"Context: {ctx}\n\nAI vision expert: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = DreamClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
