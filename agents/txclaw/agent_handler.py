"""A2A Handler for TXClaw - TX Blockchain via WebClaw + Chronicle"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from shared.base_agent import BaseAgent

class TXClawAgent(BaseAgent):
    def __init__(self): super().__init__('txclaw')
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = self.search_web(f"TX blockchain {query}", max_results=3)
            chronicle = self.search_chronicle(query, limit=3)
            refs = "\n".join([c.url for c in chronicle]) if chronicle else ""
            if cmd in ("/tx","/block","/address","/token","/validator","/contract") and query: 
                result = self.ask_llm(f"TX.org blockchain expert. Context: {ctx}\nRefs: {refs}\n\n{cmd}: {query}")
            elif cmd in ("/staking","/gas","/ecosystem","/governance","/network"):
                result = self.ask_llm(f"TX.org {cmd}. Context: {ctx}\nRefs: {refs}")
            elif cmd in ("/help",): result = "TXClaw - TX.org Blockchain\n  /tx /block /address /token /validator /contract /staking /gas /ecosystem /governance /network /stats"
            elif cmd in ("/stats",): result = f"TXClaw | TX Blockchain | WebClaw + Chronicle | Interactions: {self.state.get('interactions', 0)}"
            else: result = self.ask_llm(f"TX.org blockchain expert. Context: {ctx}\nRefs: {refs}\n\n{query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}
_agent = TXClawAgent()
def process_task(task: str, agent: str = None): return _agent.handle(task)
