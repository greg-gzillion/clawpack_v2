"""A2A Handler for PlotClaw - Chart Generator with matplotlib"""
import sys
from pathlib import Path

PLOTCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = PLOTCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PLOTCLAW_DIR))

from shared.base_agent import BaseAgent

class PlotClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('plotclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search chart data {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
                # Search chronicle index
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # --- CSV/JSON import ---
            if cmd in ("/csv", "/import") and query:
                parts2 = query.split()
                filepath = parts2[0]
                col = parts2[1] if len(parts2) > 1 else None
                chart_type = parts2[2] if len(parts2) > 2 else "bar"
                
                from data_io import read_csv, read_json, read_shared, list_data_dir
                
                if filepath.endswith(".csv"):
                    headers, rows, col_data = read_csv(filepath, col)
                    if col_data and isinstance(col_data, list):
                        # Got numeric column - route to bar chart
                        labels = [str(r[0])[:20] for r in rows] if rows else [f"Row {i+1}" for i in range(len(col_data))]
                        from commands.bar import run as bar_run
                        label_str = ",".join(labels[:20])
                        val_str = ",".join(str(v) for v in col_data[:20])
                        result = bar_run(f"{label_str}:{val_str} {''.join(f' --{k} {v}' if v!=True else f' --{k}' for k,v in self._extra_flags.items()) if hasattr(self,'_extra_flags') else ''}")
                    elif isinstance(col_data, str):
                        result = col_data  # Error message
                    else:
                        result = f"CSV loaded: {len(rows)} rows, headers: {headers}\nUse /csv {filepath} <column> <chart_type>"
                elif filepath.endswith(".json"):
                    data, err = read_json(filepath)
                    if err:
                        result = err
                    else:
                        result = f"JSON loaded: {json.dumps(data, indent=2, default=str)[:2000]}"
                else:
                    result = f"Unknown format. Use .csv or .json files.\nAvailable: {list_data_dir()}"
            
            # --- List data files ---
            elif cmd in ("/data", "/files") and not query:
                from data_io import list_data_dir
                result = "Available data files:\n" + "\n".join(f"  {f}" for f in list_data_dir())
            
            # --- Shared memory ---
            elif cmd == "/shared" and query:
                from data_io import read_shared, write_shared
                parts2 = query.split(maxsplit=1)
                action = parts2[0]
                if action == "read" and len(parts2) > 1:
                    data, err = read_shared(parts2[1])
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action == "write" and len(parts2) > 1:
                    key_val = parts2[1].split(":", 1)
                    if len(key_val) == 2:
                        result = write_shared(key_val[0], key_val[1])
                    else:
                        result = "Usage: /shared write key:value"
                elif action == "read":
                    data, err = read_shared()
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                else:
                    result = "Usage: /shared [read [key]] [write key:value]"
            
            # --- Export last chart to shared ---
            elif cmd == "/publish" and query:
                from data_io import write_shared
                result = write_shared("plotclaw_latest", query)
            
            # --- Chart commands (all support universal flags) ---
            elif cmd in ("/bar", "bar") and query:
                from commands.bar import run
                result = run(query)
            elif cmd in ("/pie", "pie") and query:
                from commands.pie import run
                result = run(query)
            elif cmd in ("/plot", "plot") and query:
                from commands.plot import run
                result = run(query)
            elif cmd in ("/scatter", "scatter") and query:
                from commands.scatter import run
                result = run(query)
            elif cmd in ("/hist", "hist") and query:
                from commands.hist import run
                result = run(query)
            elif cmd in ("/box", "box") and query:
                from commands.box import run
                result = run(query)
            elif cmd in ("/heatmap", "heatmap") and query:
                from commands.heatmap import run
                result = run(query)
            elif cmd in ("/polar", "polar") and query:
                from commands.polar import run
                result = run(query)
            elif cmd in ("/surface", "surface") and query:
                from commands.surface import run
                result = run(query)
            elif cmd in ("/compare", "compare") and query:
                from commands.compare import run
                result = run(query)
            elif cmd in ("/animate", "animate") and query:
                from commands.animate import run
                result = run(query)
            elif cmd in ("/stats", "stats") and query:
                from commands.stats import run
                result = run(query)
            elif cmd in ("/dashboard", "dashboard") and query:
                from commands.dashboard import run
                result = run(query)
            
            # --- Delegate to other agents ---
            elif cmd == "/delegate" and query:
                parts2 = query.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                if target in ("docuclaw", "interpretclaw", "dataclaw", "webclaw", "mathematicaclaw"):
                    result = self.call_agent(target, task_text) or f"Agent {target} returned no response"
                else:
                    result = f"Unknown agent: {target}. Try: docuclaw, interpretclaw, dataclaw, webclaw, mathematicaclaw"
            
            # --- Help ---
            elif cmd in ("/help",):
                result = """PlotClaw v3 - 13 Chart Types + Data I/O
  CHARTS:   /bar /pie /plot /scatter /hist /box /heatmap /polar /surface /compare /animate /stats /dashboard
  DATA:     /csv <file.csv> [column] [chart_type]  |  /data (list files)  |  /import <file.json>
  SHARED:   /shared read [key]  |  /shared write key:value  |  /publish <data>
  DELEGATE: /delegate <agent> <task>
  FLAGS:    --ylim 0,100 --xlim -5,5 --figsize 12,8 --dpi 200 --fontsize 12 --cmap magma --theme dark
            --format svg|pdf|png --save-only
  /stats"""
            
            elif cmd in ("/stats",):
                result = f"PlotClaw v3 | 13 chart types | CSV/JSON/Shared | Exports to PNG/SVG/PDF | Interactions: {self.state.get('interactions', 0)}"
            
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Chart visualization: {query}").get("result","")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = PlotClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
