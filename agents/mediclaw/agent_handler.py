"""A2A Handler for MedicLaw - delegates to core.agent.MediclawAgent"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MEDICLAW_DIR))

from core.agent import MediclawAgent
from shared.base_agent import BaseAgent

class MedicLawHandler(BaseAgent):
    def __init__(self):
        super().__init__("mediclaw")
        self.agent = MediclawAgent()

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/help", "help"):
                result = """MedicLaw - Medical AI Agent
  /research <topic>      - Medical research
  /diagnose <symptoms>   - Differential diagnosis
  /treatment <condition> - Treatment guidelines
  /medications <drug>    - Drug information
  /interactions <drugs>  - Drug interactions
  /warnings <drug>       - FDA warnings
  /pediatrics <issue>    - Pediatric care
  /geriatrics <issue>    - Elderly care
  /lab <test>            - Lab test interpretation
  /icd <diagnosis>       - ICD-10 coding
  /prevention <condition>- Prevention guidelines
  /diet <condition>      - Dietary recommendations
  /exercise <condition>  - Exercise guidance
  /natural <condition>   - Natural remedies
  /procedure <name>      - Procedure information
  /prognosis <condition> - Disease prognosis
  /referral <condition>  - Specialist referral
  /emergency <symptom>   - Emergency triage
  /sources               - List medical sources
  /stats                 - Session statistics"""
            elif cmd in ("/sources", "sources"):
                result = f"Medical Sources ({len(self.agent.list_sources())}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(self.agent.list_sources(), 1))
            elif cmd in ("/stats", "stats"):
                result = f"MedicLaw | Queries: {len(self.agent.session['queries'])} | Sources: {len(self.agent.list_sources())} | Started: {self.agent.session['started']}"
            elif cmd in ("/diagnose", "/treatment", "/research", "/med") and args:
                method = {"diagnose": self.agent.diagnose, "treatment": self.agent.treatment, "research": self.agent.research, "med": self.agent.research}[cmd.lstrip("/")]
                result = method(args)
            elif cmd == "/medications" and args: result = self.agent.medications(args)
            elif cmd == "/interactions" and args: result = self.agent.interactions(args)
            elif cmd == "/warnings" and args: result = self.agent.warnings(args)
            elif cmd == "/pediatrics" and args: result = self.agent.pediatrics(args)
            elif cmd == "/geriatrics" and args: result = self.agent.geriatrics(args)
            elif cmd == "/lab" and args: result = self.agent.lab_tests(args)
            elif cmd == "/icd" and args: result = self.agent.coding(args)
            elif cmd == "/prevention" and args: result = self.agent.prevention(args)
            elif cmd == "/diet" and args: result = self.agent.diet(args)
            elif cmd == "/exercise" and args: result = self.agent.exercise(args)
            elif cmd == "/natural" and args: result = self.agent.natural(args)
            elif cmd == "/procedure" and args: result = self.agent.procedure(args)
            elif cmd == "/prognosis" and args: result = self.agent.prognosis(args)
            elif cmd == "/referral" and args: result = self.agent.referral(args)
            elif cmd == "/emergency" and args: result = self.agent.emergency(args)
            elif args:
                result = self.agent.research(args)
            else:
                result = f"Usage: {cmd} <query>  |  Type /help for all commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = MedicLawHandler()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
