"""test command - Constitutional Rust test generation"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "test"

def run(args: str, agent=None) -> str:
    from agents.crustyclaw.commands._memory import recall, remember
    
    query = args.strip()
    if not query:
        return "Usage: /test <Rust code to write tests for>"
    
    prior = recall(f"rust test {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior tests: {p.get('fact','')[:200]}" for p in prior)
    
    prompt = f"Write Rust unit tests with #[cfg(test)]: {query[:4000]}"
    if prior_text:
        prompt = f"Prior test patterns:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="test", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85)
    return result
