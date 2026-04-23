"""A2A Handler for MathematicaClaw - Math solving + WebClaw + LLM"""
import sys
import importlib.util
from pathlib import Path

MATHCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = MATHCLAW_DIR.parent.parent

# Load modules directly by file path - NO path conflicts
def _load_mod(rel_path):
    path = MATHCLAW_DIR / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_solve_mod = _load_mod("commands/solve.py")
_algebra_mod = _load_mod("commands/algebra.py")
_calculus_mod = _load_mod("commands/calculus.py")

_llm_path = PROJECT_ROOT / "agents" / "llmclaw" / "commands" / "llm_enhanced.py"
_llm_spec = importlib.util.spec_from_file_location("llm_enhanced", _llm_path)
_llm_module = importlib.util.module_from_spec(_llm_spec)
_llm_spec.loader.exec_module(_llm_module)
llm_run = _llm_module.run

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        if cmd in ("/solve", "/math", "solve") and query:
            result = _solve_mod.run(query)
        elif cmd in ("/algebra", "algebra") and query:
            result = _algebra_mod.solve(query)
        elif cmd in ("/calculus", "/derivative", "calculus", "derivative") and query:
            result = _calculus_mod.derivative(query)
        elif cmd in ("/integral", "integral") and query:
            result = _calculus_mod.integral(query)
        elif cmd in ("/explain", "explain") and query:
            result = llm_run(f"Explain this math concept clearly: {query}")
        elif cmd in ("/search", "search") and query:
            sys.path.insert(0, str(PROJECT_ROOT))
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            ctx = WebclawProvider().search_with_context(f"math {query}", max_results=5)
            result = f"Results: {ctx}"
        elif cmd in ("/stats", "stats"):
            result = "MathematicaClaw | sympy + numpy + matplotlib | LLM: Groq chain"
        else:
            result = llm_run(f"Solve this math problem step by step: {query}")

        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
