"""code command - Constitutional code generation with memory + enrichment"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

name = "code"


def run(args: str, agent=None) -> str:
    """Generate code with memory recall, reference enrichment, and learning."""
    from agents.claw_coder.commands._memory import recall, remember
    from agents.claw_coder.commands._helpers import get_lang_info, extract_code, save_code, validate_syntax
    
    query = args.strip()
    if not query:
        return "Usage: /code <description of code to generate>"
    
    # 1. Check memory for prior solutions
    prior_matches = recall(query, limit=3)
    prior_context = ""
    if prior_matches:
        prior_context = "\n".join(
            f"Prior solution [{m.get('command','')}]: {m.get('fact','')[:300]}"
            for m in prior_matches
        )
    
    # 2. Detect language
    lang, version, ext = get_lang_info(query)
    
    # 3. Reference enrichment (via agent if available)
    refs_context = ""
    if agent and hasattr(agent, '_read_reference_file'):
        refs_context = agent._read_reference_file(lang, query)
    
    # 4. Build enriched prompt
    prompt = f"Write clean {lang} {version} code. Return only the code with brief comments.\n\nTask: {query}"
    if prior_context:
        prompt = f"Prior solutions for reference:\n{prior_context}\n\n{prompt}"
    if refs_context:
        prompt = f"Reference material for {lang}:\n{refs_context[:3000]}\n\n{prompt}"
    
    # 5. Rust-specific audit (via agent)
    if lang == "rust" and agent and hasattr(agent, 'call_agent'):
        try:
            rust_audit = agent.call_agent("crustyclaw", f"/audit {query}", timeout=10) or ""
            if rust_audit:
                prompt += f"\n\nRust best practices:\n{rust_audit[:1000]}"
        except Exception:
            pass
    
    # 6. Generate via Sovereign Gateway
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context available for LLM call"
    
    # 7. Extract, save, validate
    code = extract_code(result)
    fn, filepath = save_code(code, lang, query)
    passed, validation = validate_syntax(filepath, lang)
    
    if passed:
        result = f"Saved: {fn} | Validated: {validation}\n\n{result}"
    elif validation:
        result = f"Saved: {fn} | Validation: {validation}\n\n{result}"
    else:
        result = f"Saved: {fn} | Could not validate\n\n{result}"
    
    # 8. Remember this solution
    remember(
        command="code",
        query=query,
        result_summary=f"Generated {lang} code: {query[:100]} -> {fn}",
        source_type="chronicle",
        confidence=0.85,
        metadata={"lang": lang, "file": fn}
    )
    
    return result
