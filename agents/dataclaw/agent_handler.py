"""A2A Handler for DataClaw v5 - Constitutional Local Data Search Agent"""
import sys, json
from pathlib import Path
from datetime import datetime

DATACLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DATACLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DATACLAW_DIR))

from shared.base_agent import BaseAgent

SKIP_DIRS = {'node_modules','venv','__pycache__','.git','lib64'}

class DataClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("dataclaw")

    def _search_local_files(self, query, max_results=10):
        results = []
        search_paths = [PROJECT_ROOT/"docs", PROJECT_ROOT/"data", PROJECT_ROOT/"agents"/"webclaw"/"references", PROJECT_ROOT/"exports"]
        query_lower = query.lower()
        for search_path in search_paths:
            if not search_path.exists(): continue
            for file_path in search_path.rglob("*"):
                if any(skip in str(file_path).lower() for skip in SKIP_DIRS): continue
                if file_path.is_file() and file_path.suffix in ('.md','.txt','.py','.json','.csv','.yaml','.rs','.go','.js','.html'):
                    try:
                        if query_lower in file_path.name.lower():
                            results.append({"file":str(file_path.relative_to(PROJECT_ROOT)),"match":"filename","size":file_path.stat().st_size})
                        else:
                            content = file_path.read_text(encoding="utf-8", errors="ignore")
                            if query_lower in content.lower():
                                for i, line in enumerate(content.split('\n')):
                                    if query_lower in line.lower():
                                        results.append({"file":str(file_path.relative_to(PROJECT_ROOT)),"match":f"line {i+1}: {line.strip()[:200]}","size":file_path.stat().st_size})
                                        break
                    except: pass
                    if len(results)>=max_results: break
            if len(results)>=max_results: break
        return results

    def _search_data_files(self, query):
        results = []
        for data_path in [PROJECT_ROOT/"data", PROJECT_ROOT/"exports"]:
            if not data_path.exists(): continue
            for file_path in data_path.rglob("*.json"):
                if any(skip in str(file_path).lower() for skip in SKIP_DIRS): continue
                try:
                    content = json.loads(file_path.read_text(encoding="utf-8"))
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if query.lower() in str(key).lower() or query.lower() in str(value).lower():
                                results.append({"file":str(file_path.relative_to(PROJECT_ROOT)),"key":str(key),"value":str(value)[:200]})
                    elif isinstance(content, list):
                        for item in content[:50]:
                            if query.lower() in str(item).lower():
                                results.append({"file":str(file_path.relative_to(PROJECT_ROOT)),"item":str(item)[:200]})
                                break
                except: pass
                if len(results)>=10: break
        return results

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "DataClaw v5 - Constitutional Local Data Search\n  /search /find <query>  /export <fmt> <query>\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}

            if cmd in ("/stats",):
                total_files = 0
                for sp in [PROJECT_ROOT/"docs", PROJECT_ROOT/"data", PROJECT_ROOT/"agents"/"webclaw"/"references"]:
                    if sp.exists():
                        try: total_files += sum(1 for _ in sp.rglob("*") if _.is_file() and not any(skip in str(_).lower() for skip in SKIP_DIRS))
                        except: pass
                return {"status":"success","result":f"DataClaw v5 | {total_files:,} files indexed | Interactions: {self.state.get('interactions',0)}"}

            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/search","/find","search","find") and query:
                file_results = self._search_local_files(query, max_results=10)
                data_results = self._search_data_files(query)
                lines = [f"Search: {query}", "="*50]
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
                        elif 'item' in r: lines.append(f"     {r['item']}")
                if not file_results and not data_results: lines.append("\nNo local results found.")
                chronicle_results = self.search_chronicle(query, limit=5)
                if chronicle_results:
                    lines.append(f"\n### Chronicle ({len(chronicle_results)} references)")
                    for c in chronicle_results:
                        ctx = c.get('context','')[:150] if isinstance(c, dict) else str(c)[:150]
                        if ctx: lines.append(f"\n  {ctx}")
                result = "\n".join(lines)

            elif cmd in ("/export","export") and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0] if len(parts2)>1 else "json"
                data_query = parts2[1] if len(parts2)>1 else parts2[0]
                file_results = self._search_local_files(data_query, max_results=5)
                data_results = self._search_data_files(data_query)
                export_data = {"query":data_query,"files":file_results,"data":data_results,"timestamp":datetime.now().isoformat()}
                EXPORTS.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = data_query.replace(" ","_")[:40]
                if fmt=="json":
                    fn = f"dataclaw_{name}_{ts}.json"
                    (EXPORTS/fn).write_text(json.dumps(export_data, indent=2, default=str))
                elif fmt=="csv":
                    import csv
                    fn = f"dataclaw_{name}_{ts}.csv"
                    with open(EXPORTS/fn,"w",newline="") as f:
                        w=csv.writer(f); w.writerow(["Type","File","Content"])
                        for r in file_results: w.writerow(["file",r['file'],r.get('match','')])
                        for r in data_results: w.writerow(["data",r['file'],r.get('value',r.get('item',''))])
                else:
                    fn = f"dataclaw_{name}_{ts}.{fmt}"
                    (EXPORTS/fn).write_text(str(export_data))
                result = f"Exported: {fn}"

            elif query:
                file_results = self._search_local_files(query, max_results=10)
                data_results = self._search_data_files(query)
                chronicle_results = self.search_chronicle(query, limit=5)
                lines = [f"Search: {query}", "="*50]
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
                        ctx = c.get('context','')[:150] if isinstance(c, dict) else str(c)[:150]
                        if ctx: lines.append(f"\n  {ctx}")
                if not file_results and not data_results and not chronicle_results: lines.append("\nNo results found.")
                result = "\n".join(lines)
            else:
                result = "Type /help for commands"

            from data_io import write_shared
            write_shared("dataclaw_latest", {"query":query,"results_count":len(file_results) if 'file_results' in dir() else 0})

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query","")
            results = self._search_local_files(query, max_results=10)
            return {"status":"success","result":json.dumps(results, indent=2, default=str)}
        except Exception as e:
            return {"status":"error","result":str(e)}

_agent = DataClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
