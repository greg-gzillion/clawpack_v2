"""A2A Handler for MathematicaClaw - Math solving + WebClaw + LLM"""
import sys
from pathlib import Path

MATHCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = MATHCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MATHCLAW_DIR))

LLMCLAW_CMDS = PROJECT_ROOT / "agents" / "llmclaw" / "commands"

def _ask_llm(prompt: str) -> str:
    try:
        sys.path.insert(0, str(LLMCLAW_CMDS.parent))
        from commands.llm_enhanced import run as llm_run
        return llm_run(prompt)
    except Exception as e:
        return f"LLM error: {e}"

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        if cmd in ("/solve", "/math", "solve") and query:
            from commands.solve import run
            result = run(query)
        elif cmd in ("/algebra", "algebra") and query:
            from commands.algebra import solve as algebra_solve
            result = algebra_solve(query)
        elif cmd in ("/calculus", "/derivative", "calculus", "derivative") and query:
            from commands.calculus import derivative
            result = derivative(query)
        elif cmd in ("/explain", "explain") and query:
            result = _ask_llm(f"Explain this math concept clearly: {query}")
        elif cmd in ("/search", "search") and query:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            ctx = WebclawProvider().search_with_context(f"math {query}", max_results=5)
            result = f"Results: {ctx}"
        elif cmd in ("/stats", "stats"):
            result = "MathematicaClaw | sympy + numpy + matplotlib | LLM: Groq chain"
        else:
            from core.math_engine import MathEngine
            eng = MathEngine()
            solved = eng.solve_equation(query)
            if solved and solved.get("success"):
                result = f"Solutions: {solved.get('solutions', solved)}"
            else:
                result = _ask_llm(f"Solve step by step: {query}")

        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
