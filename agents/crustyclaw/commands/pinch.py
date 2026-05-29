"""pinch command - Constitutional Rust allocation analysis"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "pinch"

def run(args: str, agent=None) -> str:
    from agents.crustyclaw.commands._memory import recall, remember
    from agents.crustyclaw.commands._helpers import run_standalone
    
    query = args.strip()
    if not query:
        return "Usage: /pinch <Rust code to analyze>"
    
    standalone = run_standalone("pinch", query)
    if standalone:
        result = f"[Standalone pinch]\n{standalone}"
        remember(command="pinch", query=query, result_summary=result[:400],
                 source_type="chronicle", confidence=0.90)
        return result
    
    prior = recall(f"rust pinch {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior analysis: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Analyze for unnecessary clones and allocations: {query[:4000]}"
    if prior_text:
        prompt = f"Prior analyses:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="pinch", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85)
    return result
