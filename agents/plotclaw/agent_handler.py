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
            if cmd in ("/bar", "bar") and query:
                from agents.plotclaw.commands.bar import run
                result = run(query)
            elif cmd in ("/pie", "pie") and query:
                from agents.plotclaw.commands.pie import run
                result = run(query)
            elif cmd in ("/plot", "plot") and query:
                from agents.plotclaw.commands.plot import run
                result = run(query)
            elif cmd in ("/scatter", "scatter") and query:
                from agents.plotclaw.commands.scatter import run
                result = run(query)
            elif cmd in ("/hist", "hist") and query:
                from agents.plotclaw.commands.hist import run
                result = run(query)
            elif cmd in ("/box", "box") and query:
                from agents.plotclaw.commands.box import run
                result = run(query)
            elif cmd in ("/heatmap", "heatmap") and query:
                from agents.plotclaw.commands.heatmap import run
                result = run(query)
            elif cmd in ("/polar", "polar") and query:
                from agents.plotclaw.commands.polar import run
                result = run(query)
            elif cmd in ("/surface", "surface") and query:
                from agents.plotclaw.commands.surface import run
                result = run(query)
            elif cmd in ("/compare", "compare") and query:
                from agents.plotclaw.commands.compare import run
                result = run(query)
            elif cmd in ("/animate", "animate") and query:
                from agents.plotclaw.commands.animate import run
                result = run(query)
            elif cmd in ("/stats", "stats") and query:
                from agents.plotclaw.commands.stats import run
                result = run(query)
            elif cmd in ("/dashboard", "dashboard") and query:
                from agents.plotclaw.commands.dashboard import run
                result = run(query)
            elif cmd in ("/help",):
                result = "PlotClaw v2 - 11 Chart Types\n  /bar <vals> [--horizontal] [--stacked] [--errors 1,2,0.5] [--mean --std]\n  /pie <vals> [--explode 0,0.1 --donut]\n  /plot <expr> [--range -pi,pi --legend --annotate text,x,y --logx --logy]\n  /scatter <x> <y> [--trendline]\n  /hist <vals> [--bins N]\n  /box <s1> <s2> [--labels A,B --horizontal]\n  /heatmap <row1;row2> [--cmap magma --annotate]\n  /polar <r(theta)> [--range 0,6.28]\n  /surface <z=f(x,y)> [--range -5,5 --cmap magma]\n  /compare <A:1,2> <B:3,4> [--title T]\n  /dashboard <bar:name:v1,v2> <pie:name:v1,v2> <line:name:v1,v2>\n  /animate <expr(t)> [--frames 60 --fps 15]\n  /stats <vals> (auto histogram+box+QQ+summary)\n  All: --theme dark --format svg|pdf|png --save-only\n  /stats"
            elif cmd in ("/stats",):
                result = f"PlotClaw | matplotlib charts | Bar/Pie/Plot | Exports to PNG | Interactions: {self.state.get('interactions', 0)}"
            else:
                from agents.llmclaw.agent_handler import process_task as _llm
                result = _llm(f"/llm Chart visualization: {query}").get("result","")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = PlotClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
