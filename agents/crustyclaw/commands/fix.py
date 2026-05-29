"""fix command - Constitutional Rust debugging with memory"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "fix"

def run(args: str, agent=None) -> str:
    from agents.crustyclaw.commands._memory import recall, remember
    
    query = args.strip()
    if not query:
        return "Usage: /fix <Rust code to debug>"
    
    prior = recall(f"rust fix {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior fix: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Debug and fix this Rust code: {query[:4000]}"
    if prior_text:
        prompt = f"Prior fixes:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="fix", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85)
    return result
