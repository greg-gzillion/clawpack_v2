"""A2A Handler for LawClaw - Law Research Agent with A2A routing"""
import sys
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent

class LawClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")

    def _gather_context(self, query=""):
        """Gather law context from A2A specialists + chronicle"""
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web:
            parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data:
            parts.append("[DataClaw]: " + data)
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
                result = "LawClaw - /court /search /ask /analyze /browse /list /federal /state /statute /case /jurisdiction /draft /help /stats"
            elif cmd == "/stats":
                result = f"LawClaw | Interactions: {self.state.get('interactions', 0)}"
            elif cmd == "/court" and args:
                context = self._gather_context(f"{args} court municipal jurisdiction police jail hospital")
                result = self.ask_llm(
                    f"What courts serve {args}? Include ALL courts, addresses, jurisdictions, phone numbers, city info, police, jails, hospitals, libraries, building permits. Use the context provided.\n\nContext:\n{context}"
                )
            elif cmd == "/search" and args:
                results = self.search_chronicle(args, limit=10)
                if results:
                    lines = []
                    for r in results:
                        ctx = r.get("context", "") if isinstance(r, dict) else str(r)
                        url = r.get("url", "")
                        lines.append(f"SOURCE: {url}\n{ctx[:1500]}")
                    result = "\n\n---\n\n".join(lines)
                else:
                    result = f"No results for: {args}"
            elif cmd == "/browse" and args:
                state = args.strip().upper()
                p = Path(f"C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/lawclaw/jurisdictions/us/{state}")
                if p.exists():
                    counties = sorted([d.name for d in p.iterdir() if d.is_dir()])
                    result = f"{state}: {len(counties)} counties\n" + "\n".join(f"  {c}" for c in counties[:50])
                else:
                    result = f"State '{state}' not found"
            elif cmd == "/list":
                p = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/lawclaw/jurisdictions/us")
                states = sorted([d.name for d in p.iterdir() if d.is_dir()])
                result = f"Available states ({len(states)}):\n" + "\n".join(f"  {s}" for s in states)
            elif args:
                context = self._gather_context(args)
                result = self.ask_llm(f"Law question: {args}\n\nContext:\n{context}")
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LawClawHandler()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)