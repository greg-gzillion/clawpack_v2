"""audit command - Constitutional Rust security audit"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "audit"

def run(args: str, agent=None) -> str:
    from agents.crustyclaw.commands._memory import recall, remember
    from agents.crustyclaw.commands._helpers import run_standalone
    
    query = args.strip()
    if not query:
        return "Usage: /audit <Rust code to audit>"
    
    # Try standalone binary first
    standalone = run_standalone("audit", query)
    if standalone:
        result = f"[Standalone audit]\n{standalone}"
        remember(command="audit", query=query, result_summary=result[:400],
                 source_type="chronicle", confidence=0.90)
        return result
    
    # Fall back to LLM
    prior = recall(f"rust audit {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior audit: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Security audit this Rust code. Check unsafe blocks, unwraps, input validation: {query[:4000]}"
    if prior_text:
        prompt = f"Prior audits:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="audit", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85)
    return result
