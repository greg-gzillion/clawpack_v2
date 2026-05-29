"""tutorial command - Constitutional tutorial generation with memory"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "tutorial"

def run(args: str, agent=None) -> str:
    from agents.claw_coder.commands._memory import recall, remember
    from agents.claw_coder.commands._helpers import get_lang_info
    
    query = args.strip()
    if not query:
        return "Usage: /tutorial <topic for tutorial>"
    
    lang, version, ext = get_lang_info(query)
    
    prior = recall(f"tutorial {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior tutorial: {p.get('fact','')[:200]}" for p in prior)
    
    if agent and hasattr(agent, 'ask_llm_smart'):
        result = agent.ask_llm_smart(
            f"Create a beginner-friendly {lang} {version} tutorial: {query}",
            task_type="summarization"
        )
    elif agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(f"Create a beginner-friendly {lang} {version} tutorial: {query}")
    else:
        return "Error: No agent context"
    
    if prior_text:
        result = f"[Prior tutorials found]\n{prior_text}\n\n---\n\n{result}"
    
    remember(command="tutorial", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85,
             metadata={"lang": lang})
    return result
