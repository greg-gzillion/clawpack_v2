"""A2A Handler for MathematicaClaw - Full Math Engine with A2A Routing"""
import sys
from pathlib import Path

MATHCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MATHCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MATHCLAW_DIR))

from shared.base_agent import BaseAgent
import importlib.util

def _load_mod(name):
    path = MATHCLAW_DIR / "commands" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load ALL command modules
_solve_mod = _load_mod("solve")
_algebra_mod = _load_mod("algebra")
_calculus_mod = _load_mod("calculus")
from handlers.calculus import derivative, integral, limit_func, proof
_plot_mod = _load_mod("plot")
_animate_mod = _load_mod("animate")
_arithmetic_mod = _load_mod("arithmetic")
_math_mod = _load_mod("math")
_system_mod = _load_mod("system")

class MathematicaClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("mathematicaclaw")

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # ---- Equation Solving ----
            if cmd in ("/solve", "solve") and query:
                result = _solve_mod.run(query)
            
            # ---- Algebra ----
            elif cmd in ("/simplify", "simplify") and query:
                result = _algebra_mod.simplify(query)
            elif cmd in ("/factor", "factor") and query:
                result = _algebra_mod.factor(query)
            elif cmd in ("/expand", "expand") and query:
                result = _algebra_mod.expand(query)
            elif cmd in ("/algebra", "algebra") and query:
                result = _algebra_mod.solve(query)
            
            # ---- Calculus ----
            elif cmd in ("/derivative", "/diff", "derivative", "diff") and query:
                result = _calculus_mod.derivative(query)
            elif cmd in ("/integral", "/integrate", "integral", "integrate") and query:
                result = _calculus_mod.integral(query)
            elif cmd in ("/limit", "limit") and query:
                result = _calculus_mod.limit(query)
            elif cmd in ("/proof", "proof") and query:
                from handlers.calculus import proof
                result = proof(query)
            
            # ---- Systems & Matrices ----
            elif cmd in ("/system", "system") and query:
                try:
                    import sympy as sp
                    equations = [eq.strip() for eq in query.split(',')]
                    syms = set()
                    for eq_str in equations:
                        if '=' in eq_str:
                            left, right = eq_str.split('=')
                            syms.update([s for s in sp.sympify(left).free_symbols])
                        else:
                            syms.update([s for s in sp.sympify(eq_str).free_symbols])
                    eqs = []
                    for eq_str in equations:
                        if '=' in eq_str:
                            left, right = eq_str.split('=')
                            eqs.append(sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip())))
                        else:
                            eqs.append(sp.sympify(eq_str.strip()))
                    solutions = sp.solve(eqs, list(syms), dict=True)
                    if solutions:
                        result = "Solutions:\n" + "\n".join(f"  {k} = {v}" for sol in solutions for k, v in sol.items())
                    else:
                        result = "No solution found"
                except Exception as e:
                    result = f"Error: {e}"
            elif cmd in ("/matrix", "matrix") and query:
                try:
                    import sympy as sp
                    import ast
                    mat = sp.Matrix(ast.literal_eval(query))
                    det = mat.det()
                    rref = mat.rref()[0]
                    eigenvalues = mat.eigenvals()
                    result = f"Matrix:\n{mat}\n\nDeterminant: {det}\n\nRow-Reduced Echelon Form:\n{rref}\n\nEigenvalues: {eigenvalues}"
                except Exception as e:
                    result = f"Error: {e}"
            
            # ---- Arithmetic ----
            elif cmd in ("/add", "add") and query:
                result = _arithmetic_mod.add(query)
            elif cmd in ("/subtract", "subtract") and query:
                result = _arithmetic_mod.subtract(query)
            elif cmd in ("/multiply", "multiply") and query:
                result = _arithmetic_mod.multiply(query)
            elif cmd in ("/divide", "divide") and query:
                result = _arithmetic_mod.divide(query)
            elif cmd in ("/power", "power") and query:
                result = _arithmetic_mod.power(query)
            elif cmd in ("/sqrt", "sqrt") and query:
                result = _arithmetic_mod.sqrt(query)
            elif cmd in ("/percent", "percent") and query:
                result = _arithmetic_mod.percent(query)
            
            # ---- Visualization ----
            elif cmd in ("/plot", "plot") and query:
                result = _plot_mod.run(query)
            elif cmd in ("/animate", "animate") and query:
                result = _animate_mod.run(query)
            elif cmd in ("/polar", "polar") and query:
                from visualization.graph_builder import GraphBuilder
                result = GraphBuilder.polar_plot(query)
            elif cmd in ("/parametric", "parametric") and query:
                from visualization.graph_builder import GraphBuilder
                parts = query.split(',')
                if len(parts) >= 2:
                    result = GraphBuilder.parametric_plot(parts[0].strip(), parts[1].strip())
                else:
                    result = "Usage: /parametric x_expr, y_expr"
            elif cmd in ("/contour", "contour") and query:
                from visualization.graph_builder import GraphBuilder
                result = GraphBuilder.contour_plot(query)
            
            # ---- Explanation & LLM ----
            elif cmd in ("/explain", "explain") and query:
                result = self.ask_llm(f"Explain this mathematical concept in detail with examples, proofs, and applications: {query}")
            
            # ---- Meta ----
            elif cmd in ("/help", "help"):
                result = """MathematicaClaw - Complete Math Engine
  CALCULUS:   /derivative /integral /limit
  ALGEBRA:    /solve /simplify /factor /expand /algebra
  SYSTEMS:    /system /matrix
  ARITHMETIC: /add /subtract /multiply /divide /power /sqrt /percent
  VISUALIZE:  /plot /animate
  EXPLAIN:    /explain <concept>
  META:       /help /stats"""
            elif cmd in ("/stats", "stats"):
                result = f"MathematicaClaw | SymPy + NumPy + Matplotlib + Plotly | A2A Routing | Interactions: {self.state.get('interactions', 0)}"
            
            # ---- Fallback: try to solve as equation ----
            elif query:
                result = _solve_mod.run(query)
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = MathematicaClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)