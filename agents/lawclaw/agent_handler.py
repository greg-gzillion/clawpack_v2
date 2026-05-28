"""A2A Handler for LawClaw - Law Research Agent with A2A routing"""
import sys
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class LawClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web:
            parts.append("[WebClaw]: " + web)
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx:
                    lines.append(ctx[:1000])
            if lines:
                parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/help", "help"):
                result = "LawClaw - /analyze /ask /brief /browse /cite /court /docket /federal /judge /jurisdiction /law /list /oral /precedent /search /state /stats /statute /summarize /draft /help"
            elif cmd == "/stats":
                result = f"LawClaw | Interactions: {self.state.get('interactions', 0)}"
            elif cmd == "/analyze" and args:
                from agents.lawclaw.commands.analyze import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/ask" and args:
                from agents.lawclaw.commands.ask import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/brief" and args:
                from agents.lawclaw.commands.brief import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/browse" and args:
                from agents.lawclaw.commands.browse import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/cite" and args:
                from agents.lawclaw.commands.cite import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/court" and args:
                from agents.lawclaw.commands.court import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/docket" and args:
                from agents.lawclaw.commands.docket import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/federal" and args:
                from agents.lawclaw.commands.federal import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/judge" and args:
                from agents.lawclaw.commands.judge import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/jurisdiction" and args:
                from agents.lawclaw.commands.jurisdiction import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/law" and args:
                from agents.lawclaw.commands.law import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/list":
                from agents.lawclaw.commands.list import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/oral" and args:
                from agents.lawclaw.commands.oral import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/precedent" and args:
                from agents.lawclaw.commands.precedent import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/search" and args:
                from agents.lawclaw.commands.search import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/state" and args:
                from agents.lawclaw.commands.state import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/statute" and args:
                from agents.lawclaw.commands.statute import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/summarize" and args:
                from agents.lawclaw.commands.summarize import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/draft" and args:
                # Enrich delegation with jurisdiction context from shared memory
                try:
                    from agents.lawclaw.commands._memory import recall_court
                    court = recall_court(args)
                    if court:
                        payload = f"/draft {args} court={court.get('fact','')}"
                    else:
                        payload = f"/draft {args}"
                except Exception:
                    payload = f"/draft {args}"
                result = self.call_agent("draftclaw", payload, timeout=30)
            elif args:
                context = self._gather_context(args)
                result = self.ask_llm(f"Law question: {args}\n\nContext:\n{context}")
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            log_err("lawclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = LawClawHandler()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)