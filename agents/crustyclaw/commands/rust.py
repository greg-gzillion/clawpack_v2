"""rust command - Constitutional Rust code generation with memory + enrichment"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "rust"

def run(args: str, agent=None) -> str:
    from agents.crustyclaw.commands._memory import recall, remember
    from agents.crustyclaw.commands._helpers import validate_rust, extract_code, save_rust
    
    query = args.strip()
    if not query:
        return "Usage: /rust <task>\nExample: /rust create a TCP server"
    
    # Check memory for prior Rust solutions
    prior = recall(f"rust {query}", limit=3)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior: {p.get('fact','')[:200]}" for p in prior)
    
    # Build prompt
    prompt = f"Write clean Rust 2024 edition code. Return only the code with brief comments. Task: {query}"
    if prior_text:
        prompt = f"Prior Rust solutions:\n{prior_text}\n\n{prompt}"
    
    # Generate via Sovereign Gateway
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    # Extract, save, validate
    code = extract_code(result)
    fn, filepath = save_rust(code, query)
    validation = validate_rust(filepath)
    result = f"Saved: {fn} | Validated: {validation}\n\n{result}"
    
    # Learn
    remember(command="rust", query=query, result_summary=f"Rust code: {query[:100]} -> {fn}",
             source_type="chronicle", confidence=0.85, metadata={"file": fn})
    return result
