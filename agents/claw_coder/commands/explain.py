"""explain command - Constitutional code explanation with memory + enrichment"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "explain"

def run(args: str, agent=None) -> str:
    from agents.claw_coder.commands._memory import recall, remember
    from agents.claw_coder.commands._helpers import get_lang_info
    
    query = args.strip()
    if not query:
        return "Usage: /explain <code or concept to explain>"
    
    lang, version, ext = get_lang_info(query)
    
    prior = recall(query, limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior: {p.get('fact','')[:200]}" for p in prior)
    
    refs = ""
    if agent and hasattr(agent, '_read_reference_file'):
        refs = agent._read_reference_file(lang, query)
    
    prompt = f"Explain this clearly with code examples: {query}"
    if prior_text:
        prompt = f"Prior explanations:\n{prior_text}\n\n{prompt}"
    if refs:
        prompt = f"Reference:\n{refs[:2000]}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="explain", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85,
             metadata={"lang": lang})
    return result
