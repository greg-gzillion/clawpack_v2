"""Calculus commands for mathematicaclaw - step-by-step explanations"""
import sympy as sp
import re

def derivative(args=None):
    """Derivative with step-by-step explanation"""
    if args:
        try:
            expr_str = args.replace('derivative ', '').replace('diff ', '').strip()
            
            if ' wrt ' in expr_str.lower():
                expr_part, var = expr_str.lower().split(' wrt ', 1)
                expr = sp.sympify(expr_part.strip())
                var_sym = sp.Symbol(var.strip())
                expr_str = expr_part.strip()
            else:
                expr = sp.sympify(expr_str)
                syms = list(expr.free_symbols)
                var_sym = syms[0] if syms else sp.Symbol('x')
            
            result = sp.diff(expr, var_sym)
            
            # Build step-by-step explanation
            steps = []
            steps.append(f"Find d/d{var_sym}[{expr_str}]")
            steps.append("")
            
            # Recognize the function type
            if expr.is_Add:
                steps.append("Step 1: Use the Sum Rule - derivative of a sum is the sum of derivatives")
                for term in expr.args:
                    term_deriv = sp.diff(term, var_sym)
                    steps.append(f"  d/d{var_sym}[{term}] = {term_deriv}")
            elif expr.is_Mul:
                steps.append("Step 1: Use the Product Rule - d/dx[f·g] = f'·g + f·g'")
                if len(expr.args) == 2:
                    f, g = expr.args
                    f_deriv = sp.diff(f, var_sym)
                    g_deriv = sp.diff(g, var_sym)
                    steps.append(f"  Let f = {f}, g = {g}")
                    steps.append(f"  f' = {f_deriv}")
                    steps.append(f"  g' = {g_deriv}")
                    steps.append(f"  Result: ({f_deriv})·({g}) + ({f})·({g_deriv})")
            elif isinstance(expr, sp.Pow):
                steps.append("Step 1: Use the Chain Rule / Power Rule")
                base, exp = expr.as_base_exp()
                steps.append(f"  Outer function: {exp} power")
                steps.append(f"  Inner function: {base}")
                steps.append(f"  d/d{var_sym}[({base})^{exp}] = {exp}·({base})^{exp-1} · d/d{var_sym}[{base}]")
            elif expr.func in [sp.sin, sp.cos, sp.tan, sp.exp, sp.log]:
                rules = {
                    sp.sin: "sin → cos",
                    sp.cos: "cos → -sin",
                    sp.tan: "tan → sec²",
                    sp.exp: "e^u → e^u",
                    sp.log: "ln(u) → 1/u"
                }
                steps.append(f"Step 1: Apply derivative rule for {expr.func.__name__}")
                steps.append(f"  Rule: d/dx[{expr.func.__name__}] = {rules.get(expr.func, 'see result')}")
                steps.append("  Use Chain Rule: derivative of outer × derivative of inner")
            
            steps.append("")
            steps.append(f"Final Answer: d/d{var_sym}[{expr_str}] = {sp.simplify(result)}")
            
            return "\n".join(steps)
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: derivative x**3 * sin(x)"

def integral(args=None):
    """Integral with step-by-step explanation"""
    if args:
        try:
            expr_str = args.replace('integral ', '').replace('integrate ', '').strip()
            
            # Definite integral
            if ' from ' in expr_str.lower():
                expr_part, bounds_part = expr_str.lower().split(' from ', 1)
                bounds_match = re.match(r'(.+?)\s+to\s+(.+)', bounds_part)
                if bounds_match:
                    lower = sp.sympify(bounds_match.group(1))
                    upper = sp.sympify(bounds_match.group(2))
                    expr = sp.sympify(expr_part.strip())
                    
                    # Find antiderivative
                    antideriv = sp.integrate(expr, sp.Symbol('x'))
                    result = sp.integrate(expr, ('x', lower, upper))
                    
                    steps = []
                    steps.append(f"Find ∫[{lower} to {upper}] ({expr_part.strip()}) dx")
                    steps.append("")
                    steps.append("Step 1: Find the antiderivative F(x)")
                    steps.append(f"  ∫({expr_part.strip()}) dx = {antideriv}")
                    steps.append("")
                    steps.append("Step 2: Apply the Fundamental Theorem of Calculus")
                    steps.append(f"  F({upper}) - F({lower})")
                    steps.append(f"  = ({antideriv.subs(sp.Symbol('x'), upper)}) - ({antideriv.subs(sp.Symbol('x'), lower)})")
                    steps.append(f"  = {result}")
                    steps.append("")
                    steps.append(f"Final Answer: {result}")
                    
                    return "\n".join(steps)
            
            # Indefinite integral
            expr = sp.sympify(expr_str)
            result = sp.integrate(expr)
            
            steps = []
            steps.append(f"Find ∫({expr_str}) dx")
            steps.append("")
            
            # Recognize pattern
            if expr.is_Pow and not expr.args[0].has(sp.Symbol):
                steps.append("Step 1: Use the Power Rule for integration")
                steps.append(f"  ∫x^n dx = x^(n+1)/(n+1) + C")
                steps.append(f"  Here n = {expr.args[1]}")
            elif expr.func == sp.exp:
                steps.append("Step 1: Integrate e^x")
                steps.append("  ∫e^u du = e^u + C")
            elif expr.func == sp.sin:
                steps.append("Step 1: Integrate sin(x)")
                steps.append("  ∫sin(u) du = -cos(u) + C")
            elif expr.func == sp.cos:
                steps.append("Step 1: Integrate cos(x)")
                steps.append("  ∫cos(u) du = sin(u) + C")
            else:
                steps.append("Step 1: Apply integration rules")
            
            steps.append(f"  Result: {result}")
            steps.append("")
            steps.append("Step 2: Add the constant of integration")
            steps.append(f"Final Answer: {result} + C")
            
            return "\n".join(steps)
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: integral x**2  OR  integral x**2 from 0 to 1"

def limit(args=None):
    """Limit with step-by-step explanation"""
    if args and 'as' in args:
        try:
            expr_str = args.replace('limit ', '').strip()
            expr_part, limit_info = expr_str.split('as')
            var, point = limit_info.split('->')
            expr = sp.sympify(expr_part.strip())
            var_sym = sp.Symbol(var.strip())
            val = sp.sympify(point.strip())
            result = sp.limit(expr, var_sym, val)
            
            steps = []
            steps.append(f"Find lim({var}→{val}) [{expr_part.strip()}]")
            steps.append("")
            steps.append("Step 1: Try direct substitution")
            
            try:
                subbed = expr.subs(var_sym, val)
                steps.append(f"  Substitute {var} = {val}: {subbed}")
                
                if subbed == sp.nan or subbed == sp.zoo or (isinstance(subbed, sp.Basic) and subbed.has(sp.zoo)):
                    steps.append("  Got 0/0 (indeterminate form) - need a different approach")
                    steps.append("")
                    steps.append("Step 2: Apply L'Hôpital's Rule or simplify")
                    # Try factoring or simplifying
                    simplified = sp.simplify(expr)
                    if simplified != expr:
                        steps.append(f"  Simplify: {expr_part.strip()} = {simplified}")
                        subbed2 = sp.limit(simplified, var_sym, val)
                        steps.append(f"  Now substitute: {subbed2}")
                else:
                    steps.append("  Direct substitution works!")
            except:
                steps.append("  Direct substitution doesn't work - applying limit rules")
            
            steps.append("")
            steps.append(f"Final Answer: lim({var}→{val}) [{expr_part.strip()}] = {result}")
            
            return "\n".join(steps)
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: limit sin(x)/x as x->0"