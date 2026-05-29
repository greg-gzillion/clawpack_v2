"""debug command - Constitutional code debugging with memory"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "debug"

def run(args: str, agent=None) -> str:
    from agents.claw_coder.commands._memory import recall, remember
    from agents.claw_coder.commands._helpers import get_lang_info
    
    query = args.strip()
    if not query:
        return "Usage: /debug <code to debug>"
    
    lang, version, ext = get_lang_info(query)
    
    prior = recall(f"debug {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior fix: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Debug and fix this code. Show corrected version with explanations: {query}"
    if prior_text:
        prompt = f"Prior debugging sessions:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="debug", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85,
             metadata={"lang": lang})
    return result
