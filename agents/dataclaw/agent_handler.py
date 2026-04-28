"""A2A Handler for DataClaw - Reference Manager + FileClaw Export"""
import sys, json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
from shared.base_agent import BaseAgent
from shared.security import InputSanitizer

class DataClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("dataclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        return "\n".join(parts)

    def _export(self, fmt, data, query):
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = query.replace(" ", "_").replace(chr(92), "").replace("/", "")
        fn = f"dataclaw_{name}_{ts}.{fmt}"
        fn = InputSanitizer.sanitize_filename(fn)
        path = EXPORTS / fn
        try:
            if fmt == "json":
                path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
            elif fmt == "csv":
                import csv
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    with open(path, "w", newline="") as f:
                        w = csv.DictWriter(f, fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
                else:
                    path.write_text(str(data), encoding="utf-8")
            elif fmt == "md":
                md = f"# DataClaw: {query}\n\n"
                if isinstance(data, list):
                    for i, item in enumerate(data, 1): md += f"{i}. {item}\n"
                else: md += str(data)
                path.write_text(md, encoding="utf-8")
            else:
                path.write_text(str(data), encoding="utf-8")
            return f"Exported: {fn}"
        except Exception as e:
            return f"Export error: {e}"

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/search", "search") and query:
                chronicle = self.search_chronicle(query, limit=2000000)
                web = self.call_agent("webclaw", f"search {query}", timeout=15)
                result = f"Results for '{query}':\n"
                if chronicle:
                    result += "\n[Chronicle]\n" + "\n".join(f"  - {c.url}" for c in chronicle)
                result += f"\n[WebClaw]\n{web}"
                if not chronicle and not web.strip():
                    result = f"No results for '{query}'. Add references with /add."
            elif cmd in ("/export",) and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0]
                q = parts2[1] if len(parts2) > 1 else ""
                chronicle = self.search_chronicle(q, limit=2000000) if q else []
                web = self.call_agent("webclaw", f"search {q}", timeout=15) if q else ""
                data = {
                    "query": q,
                    "chronicle": [c.url if hasattr(c, 'url') else str(c) for c in chronicle],
                    "webclaw": web,
                    "timestamp": datetime.now().isoformat()
                }
                msg = self._export(fmt, data, q or "search")
                result = f"{msg}\n\nExported in {fmt} format."
            elif cmd in ("/add", "add") and query:
                self.learn_fact(f"dataclaw_ref: {query}")
                result = f"Reference added: {query}\nUse /list to see all references."
            elif cmd in ("/list", "list"):
                facts = self.get_facts()
                refs = [k.replace("dataclaw_ref: ","") for k in facts if "dataclaw_ref" in k]
                result = f"Local References ({len(refs)}):\n" + "\n".join(f"  - {r}" for r in refs) if refs else "No local references yet. Use /add."
            elif cmd in ("/help",):
                result = "DataClaw - Reference Manager\n  /search <query> - Chronicle + WebClaw\n  /export <json|csv|md> <query> - Export results\n  /add /list /stats"
            elif cmd in ("/stats",):
                result = f"DataClaw | Chronicle + WebClaw | Export: json/csv/md | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(query)
                result = ctx or f"Searching: {query}"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DataClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
