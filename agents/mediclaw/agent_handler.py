"""A2A Handler for MedicLaw - Medical Agent with full inter-agent routing"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MEDICLAW_DIR))

from agents.mediclaw.core.engine import MedicalEngine
from shared.base_agent import BaseAgent

class MedicLawAgent(BaseAgent):
    def __init__(self):
        super().__init__("mediclaw")
        self.engine = MedicalEngine()

    def _gather_context(self, query: str) -> str:
        """Gather medical context from all specialists"""
        parts = []
        
        # WebClaw for online medical references
        web = self.call_agent("webclaw", f"search medical {query}", timeout=15)
        if web:
            parts.append(f"[WebClaw Online Medical Sources]:\n{web[:1000]}")
        
        # DataClaw for local medical references
        local = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if local:
            parts.append(f"[DataClaw Local References]:\n{local[:1000]}")
        
        # LawClaw for legal/regulatory context (FDA, medical law)
        legal = self.call_agent("lawclaw", f"search medical regulation {query}", timeout=15)
        if legal:
            parts.append(f"[LawClaw Regulatory]:\n{legal[:800]}")
        
        return "\n\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/diagnose", "/treatment", "/research", "/med") and args:
                # Gather context from specialists first
                context = self._gather_context(args)
                
                # Run medical engine with context
                method = {"diagnose": self.engine.diagnose, "treatment": self.engine.treatment,
                          "research": self.engine.research, "med": self.engine.research}.get(cmd[1:])
                engine_result = method(args) if method else ""
                
                # Final synthesis via LLMClaw with all context
                prompt = f"Medical query: {args}\n\nEngine analysis: {engine_result}\n\nSpecialist context:\n{context}"
                result = self.ask_llm(prompt)
                
                # Auto-export to FileClaw
                export = self.call_agent("fileclaw", f"/export md MedicLaw: {args}\n\n{result[:500]}")
                if export:
                    result = f"{export}\n\n{result}"
                    
            elif cmd == "/sources":
                sources = self.engine.list_sources()
                result = f"Medical Sources ({len(sources)}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(sources, 1))
            elif cmd == "/help":
                result = "MedicLaw - Medical Agent with specialists\n  /med /diagnose /treatment /research /sources /stats\n  Uses: WebClaw + DataClaw + LawClaw + MedicalEngine -> LLMClaw"
            elif cmd == "/stats":
                result = f"MedicLaw | Medical + Specialists | Interactions: {self.state.get('interactions', 0)}"
            else:
                context = self._gather_context(task)
                result = self.ask_llm(f"Medical information: {task}\n\nContext:\n{context}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = MedicLawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
