"""Mathematics commands with chronicle learning"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def get_chronicle():
    try:
        from shared.chronicle_helper import search_chronicle
        return search_chronicle
    except:
        return None

def get_llm():
    try:
        from shared.llm import get_llm_client
        return get_llm_manager()
    except:
        return None

def solve(problem):
    """Solve a mathematics problem"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    # Clean up the problem (handle '2x' -> '2*x')
    import re
    cleaned = re.sub(r'(\d)([a-z])', r'\1*\2', problem)
    cleaned = re.sub(r'([a-z])(\d)', r'\1*\2', cleaned)
    
    # Search chronicle for references
    references = []
    if chronicle:
        try:
            results = chronicle(problem, 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nReferences:\n" + "\n".join(f"- {r}" for r in references)
    
    prompt = f"Solve this math problem step by step: {cleaned}{ref_text}\n\nReturn ONLY the solution."
    
    if llm:
        try:
            response = llm.chat_sync(prompt, task_type="math")
            if response:
                return response
        except:
            pass
    
    # Fallback for simple equations
    if '=' in cleaned:
        try:
            import sympy as sp
            left, right = cleaned.split('=')
            expr = sp.sympify(f"{left} - ({right})")
            x = sp.Symbol('x')
            solution = sp.solve(expr, x)
            return f"Equation: {problem}\nSolution: x = {solution[0] if solution else 'No solution found'}"
        except:
            pass
    
    return f"Problem: {problem}\n\nSolution: (Use LLM for detailed solution)"

def explain(concept):
    """Explain a mathematical concept"""
    llm = get_llm()
    chronicle = get_chronicle()
    
    references = []
    if chronicle:
        try:
            results = chronicle(concept, 3)
            references = [getattr(r, 'url', str(r)) for r in results]
        except:
            pass
    
    ref_text = ""
    if references:
        ref_text = "\n\nResources:\n" + "\n".join(f"- {r}" for r in references)
    
    prompt = f"Explain this math concept clearly: {concept}{ref_text}\n\nReturn ONLY the explanation."
    
    if llm:
        try:
            response = llm.chat_sync(prompt, task_type="math")
            if response:
                return response
        except:
            pass
    
    return f"Concept: {concept}\n\nExplanation available with LLM connection."

def search(topic):
    """Search chronicle for math resources"""
    chronicle = get_chronicle()
    if not chronicle:
        return "Chronicle not available"
    
    try:
        results = chronicle(topic, 5)
        if not results:
            return f"No results found for '{topic}'"
        
        output = f"📚 Found {len(results)} resources:\n"
        for i, r in enumerate(results, 1):
            url = getattr(r, 'url', str(r))
            output += f"{i}. {url}\n"
        return output
    except Exception as e:
        return f"Search error: {e}"

def stats():
    """Get chronicle statistics"""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        s = chronicle.get_stats()
        return f"📊 Chronicle Stats: {s['total_cards']} cards, {s['unique_urls']} URLs"
    except:
        return "Stats not available"

def handle_solve(args):
    print(solve(args))

def handle_explain(args):
    print(explain(args))

def handle_search(args):
    print(search(args))

def handle_stats(args):
    print(stats())
