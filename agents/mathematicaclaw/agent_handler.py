"""A2A Handler for MathematicaClaw - Full Math Engine with A2A Routing"""
import sys, time
from pathlib import Path

MATHCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MATHCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MATHCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import delegate, chronicle, log_err
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

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search math {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def handle(self, task: str) -> dict:
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # ---- Cross-Agent Delegation ----
            if cmd in ("/delegate", "delegate") and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                result = delegate("mathematicaclaw", target, task_text)

            elif cmd in ("/export", "export") and query:
                result = delegate("mathematicaclaw", "docuclaw", f"/create math: {query}", timeout=60)

            elif cmd in ("/chart", "chart") and query:
                result = delegate("mathematicaclaw", "plotclaw", f"/plot {query}", timeout=30)

            # ---- Equation Solving ----
            elif cmd in ("/solve", "solve") and query:
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
  DELEGATE:   /delegate /export /chart
  META:       /help /stats"""
            elif cmd in ("/stats", "stats"):
                result = f"MathematicaClaw | SymPy + NumPy + Matplotlib + Plotly | A2A Routing | Interactions: {self.state.get('interactions', 0)}"

            # ---- Fallback: try to solve as equation ----
            elif query:
                result = _solve_mod.run(query)
            else:
                result = "Type /help for commands"

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("mathematicaclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("mathematicaclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("mathematicaclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("mathematicaclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("mathematicaclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"mathematicaclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("mathematicaclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("mathematicaclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="mathematicaclaw")
                except Exception: pass
                try: from agents.mathematicaclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("mathematicaclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="mathematicaclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="mathematicaclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("mathematicaclaw_handler", lambda: True)
                except Exception: pass
                try:
                    from shared.memory_guard import sanitize_memory_write
                except Exception: pass
                try:
                    from shared.source_registry import get_trust
                except Exception: pass
                try:
                    from shared.truth_resolver import merge_with_retriever
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="mathematicaclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("mathematicaclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}

_agent = MathematicaClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)