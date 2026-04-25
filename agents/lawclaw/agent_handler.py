"""A2A Handler for LawClaw - Law Research Agent with full inter-agent routing"""
import sys
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent

class LawClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")

    def _gather_law_context(self, query: str) -> str:
        """Gather law research context from all relevant specialists"""
        parts = []
        
        # WebClaw for case law, statutes, online legal sources
        web = self.call_agent("webclaw", f"search law {query}", timeout=15)
        if web:
            parts.append(f"[WebClaw Law Sources]:\n{web[:1000]}")
        
        # DataClaw for local legal references
        local = self.call_agent("dataclaw", f"search law {query}", timeout=15)
        if local:
            parts.append(f"[DataClaw Local References]:\n{local[:1000]}")
        
        # DraftClaw for document drafting assistance
        draft = self.call_agent("draftclaw", f"context {query}", timeout=10)
        if draft:
            parts.append(f"[DraftClaw Templates]:\n{draft[:500]}")
        
        return "\n\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/ask", "/case", "/statute", "/contract") and query:
                context = self._gather_law_context(query)
                result = self.ask_llm(f"Law research for: {query}\n\nResearch context:\n{context}")
                
                # Export via FileClaw
                export = self.call_agent("fileclaw", f"/export md LawClaw Analysis: {query}\n\n{result[:500]}")
                if export:
                    result = f"{export}\n\n{result}"
                    
            elif cmd == "/draft" and query:
                # Delegate to DraftClaw for document drafting
                draft_result = self.call_agent("draftclaw", f"/draft {query}", timeout=30)
                result = draft_result if draft_result else self.ask_llm(f"Draft law document: {query}")
                
            elif cmd == "/help":
                result = "LawClaw - Law Research Agent with specialists\n  /ask /case /statute /contract /draft /help /stats\n  Uses: WebClaw + DataClaw + DraftClaw -> LLMClaw -> FileClaw"
            elif cmd == "/stats":
                result = f"LawClaw | Law Research | Interactions: {self.state.get('interactions', 0)}"
            else:
                context = self._gather_law_context(query)
                result = self.ask_llm(f"Law research: {query}\n\nContext:\n{context}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LawClawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
