"""A2A Handler for MathematicaClaw - Math Engine with A2A Routing"""
import sys
from pathlib import Path

MATHCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MATHCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MATHCLAW_DIR))

from shared.base_agent import BaseAgent

# Import real command modules
import importlib.util

def _load_mod(name):
    path = MATHCLAW_DIR / "commands" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_solve_mod = _load_mod("solve")
_algebra_mod = _load_mod("algebra")
_calculus_mod = _load_mod("calculus")
solve_run = _solve_mod.run
algebra_solve = _algebra_mod.solve
calc_derivative = _calculus_mod.derivative
calc_integral = _calculus_mod.integral

class MathematicaClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("mathematicaclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search math formula {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/solve", "/math", "solve") and query:
                result = solve_run(query)
            elif cmd in ("/algebra", "algebra") and query:
                result = algebra_solve(query)
            elif cmd in ("/calculus", "/derivative", "calculus", "derivative") and query:
                result = calc_derivative(query)
            elif cmd in ("/integral", "integral") and query:
                result = calc_integral(query)
            elif cmd in ("/explain", "explain") and query:
                ctx = self._gather_context(query)
                result = self.ask_llm(f"Context: {ctx}\n\nExplain this math concept clearly: {query}")
            elif cmd in ("/help",):
                result = "MathematicaClaw - Math Engine with A2A Routing\n  /solve /algebra /calculus /derivative /integral /explain /stats\n  Uses: WebClaw + DataClaw + sympy + numpy -> LLMClaw -> FileClaw"
            elif cmd in ("/stats",):
                result = f"MathematicaClaw | sympy + numpy + matplotlib | A2A Routing | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(query)
                result = self.ask_llm(f"Context: {ctx}\n\nSolve this math problem step by step: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = MathematicaClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
