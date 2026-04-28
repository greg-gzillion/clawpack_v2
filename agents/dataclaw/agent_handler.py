"""A2A Handler for DataClaw - Local Data Search & Reference Agent"""
import sys, json
from pathlib import Path
from datetime import datetime

DATACLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DATACLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DATACLAW_DIR))

from shared.base_agent import BaseAgent

class DataClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("dataclaw")

    def _search_local_files(self, query, max_results=10):
        """Search through local files in references, docs, and data directories."""
        results = []
        search_paths = [
            PROJECT_ROOT / "docs",
            PROJECT_ROOT / "data",
            PROJECT_ROOT / "agents" / "webclaw" / "references",
            PROJECT_ROOT / "exports",
        ]
        
        query_lower = query.lower()
        for search_path in search_paths:
            if not search_path.exists():
                continue
            for file_path in search_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in ('.md', '.txt', '.py', '.json', '.csv', '.yaml', '.rs', '.go', '.js', '.html'):
                    try:
                        if query_lower in file_path.name.lower():
                            results.append({
                                "file": str(file_path.relative_to(PROJECT_ROOT)),
                                "match": "filename",
                                "size": file_path.stat().st_size
                            })
                        else:
                            content = file_path.read_text(encoding="utf-8", errors="ignore")
                            if query_lower in content.lower():
                                for i, line in enumerate(content.split('\n')):
                                    if query_lower in line.lower():
                                        results.append({
                                            "file": str(file_path.relative_to(PROJECT_ROOT)),
                                            "match": f"line {i+1}: {line.strip()[:200]}",
                                            "size": file_path.stat().st_size
                                        })
                                        break
                    except:
                        pass
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break
        
        return results

    def _search_data_files(self, query):
        """Search structured data files (JSON, CSV)."""
        results = []
        data_paths = [PROJECT_ROOT / "data", PROJECT_ROOT / "exports"]
        
        for data_path in data_paths:
            if not data_path.exists():
                continue
            for file_path in data_path.rglob("*.json"):
                try:
                    content = json.loads(file_path.read_text(encoding="utf-8"))
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if query.lower() in str(key).lower() or query.lower() in str(value).lower():
                                results.append({
                                    "file": str(file_path.relative_to(PROJECT_ROOT)),
                                    "key": str(key),
                                    "value": str(value)[:200]
                                })
                    elif isinstance(content, list):
                        for item in content[:50]:
                            if query.lower() in str(item).lower():
                                results.append({
                                    "file": str(file_path.relative_to(PROJECT_ROOT)),
                                    "item": str(item)[:200]
                                })
                                break
                except:
                    pass
                if len(results) >= 10:
                    break
        
        return results

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/search", "/find", "search", "find") and query:
                file_results = self._search_local_files(query, max_results=10)
                data_results = self._search_data_files(query)
                
                lines = []
                lines.append(f"Search: {query}")
                lines.append("=" * 50)
                
                if file_results:
                    lines.append(f"\n### Files ({len(file_results)} found)")
                    for r in file_results:
                        lines.append(f"\n  {r['file']} ({r['size']:,}B)")
                        lines.append(f"     {r['match']}")
                
                if data_results:
                    lines.append(f"\n### Data ({len(data_results)} found)")
                    for r in data_results:
                        lines.append(f"\n  {r['file']}")
                        if 'key' in r:
                            lines.append(f"     {r['key']}: {r['value']}")
                        elif 'item' in r:
                            lines.append(f"     {r['item']}")
                
                if not file_results and not data_results:
                    lines.append("\nNo local results found.")
                
                # Also check chronicle
                chronicle_results = self.search_chronicle(query, limit=5)
                if chronicle_results:
                    lines.append(f"\n### Chronicle ({len(chronicle_results)} references)")
                    for c in chronicle_results:
                        if isinstance(c, dict):
                            ctx = c.get('context', '')[:150]
                        else:
                            ctx = str(c)[:150]
                        if ctx:
                            lines.append(f"\n  {ctx}")
                
                result = "\n".join(lines)

            elif cmd in ("/export", "export") and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0] if len(parts2) > 1 else "json"
                data_query = parts2[1] if len(parts2) > 1 else parts2[0]
                
                file_results = self._search_local_files(data_query, max_results=5)
                data_results = self._search_data_files(data_query)
                
                export_data = {
                    "query": data_query,
                    "files": file_results,
                    "data": data_results,
                    "timestamp": datetime.now().isoformat()
                }
                
                EXPORTS.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = data_query.replace(" ", "_")[:40]
                
                if fmt == "json":
                    fn = f"dataclaw_{name}_{ts}.json"
                    (EXPORTS / fn).write_text(json.dumps(export_data, indent=2, default=str))
                elif fmt == "csv":
                    import csv
                    fn = f"dataclaw_{name}_{ts}.csv"
                    with open(EXPORTS / fn, "w", newline="") as f:
                        w = csv.writer(f)
                        w.writerow(["Type", "File", "Content"])
                        for r in file_results:
                            w.writerow(["file", r['file'], r.get('match', '')])
                        for r in data_results:
                            w.writerow(["data", r['file'], r.get('value', r.get('item', ''))])
                else:
                    fn = f"dataclaw_{name}_{ts}.{fmt}"
                    (EXPORTS / fn).write_text(str(export_data))
                
                result = f"Exported: {fn}"

            elif cmd in ("/stats", "stats"):
                total_files = 0
                for sp in [PROJECT_ROOT / "docs", PROJECT_ROOT / "data", PROJECT_ROOT / "agents" / "webclaw" / "references"]:
                    if sp.exists():
                        total_files += sum(1 for _ in sp.rglob("*") if _.is_file())
                
                result = f"DataClaw | Local Search | {total_files:,} files indexed | Interactions: {self.state.get('interactions', 0)}"

            elif cmd in ("/help", "help"):
                result = """DataClaw - Local Data Search & Reference Agent
  /search <query>   - Search local files and data
  /find <query>     - Same as /search
  /export <fmt> <query> - Export search results (json, csv)
  /stats            - Search statistics
  /help             - Show commands

  Searches: docs/, data/, references/, exports/
  Includes: Chronicle index, JSON data, markdown files"""

            elif query:
                file_results = self._search_local_files(query, max_results=10)
                data_results = self._search_data_files(query)
                chronicle_results = self.search_chronicle(query, limit=5)
                
                lines = [f"Search: {query}", "=" * 50]
                if file_results:
                    lines.append(f"\n### Files ({len(file_results)} found)")
                    for r in file_results:
                        lines.append(f"\n  {r['file']} ({r['size']:,}B)")
                        lines.append(f"     {r['match']}")
                if data_results:
                    lines.append(f"\n### Data ({len(data_results)} found)")
                    for r in data_results:
                        lines.append(f"\n  {r['file']}")
                        if 'key' in r: lines.append(f"     {r['key']}: {r['value']}")
                if chronicle_results:
                    lines.append(f"\n### Chronicle ({len(chronicle_results)} references)")
                    for c in chronicle_results:
                        ctx = c.get('context', '')[:150] if isinstance(c, dict) else str(c)[:150]
                        if ctx: lines.append(f"\n  {ctx}")
                if not file_results and not data_results and not chronicle_results:
                    lines.append("\nNo results found.")
                
                result = "\n".join(lines)
            else:
                result = "Type /help for commands. Usage: /search <query>"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DataClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)