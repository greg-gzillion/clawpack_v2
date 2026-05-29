"""review command - Constitutional code review with memory"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "review"

def run(args: str, agent=None) -> str:
    from agents.claw_coder.commands._memory import recall, remember
    
    query = args.strip()
    if not query:
        return "Usage: /review <code to review>"
    
    prior = recall(f"review {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior review: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Do a thorough code review. Check for bugs, security issues, performance problems, and style: {query}"
    if prior_text:
        prompt = f"Prior reviews:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm_smart'):
        result = agent.ask_llm_smart(prompt, task_type="verification")
    elif agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="review", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85)
    return result
