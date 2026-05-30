"""braille command - Convert text to Braille (Grade 1 & 2) for accessibility.
OPT-IN FEATURE: Not enabled by default. Set INTERPRETCLAW_BRAILLE=1 to activate.
Best results with reasoning models (deepseek-r1, claude, gpt-4).
Small local models produce unreliable Braille output.
"""
import sys, os
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "braille"

BRAILLE_ENABLED = os.environ.get("INTERPRETCLAW_BRAILLE", "0") == "1"

def run(args: str, agent=None) -> str:
    if not BRAILLE_ENABLED:
        return ("Braille translation is an opt-in accessibility feature.\n\n"
                "To enable: set environment variable INTERPRETCLAW_BRAILLE=1\n"
                "Best results: deepseek-r1:8b (Ollama), claude-sonnet (Anthropic), gpt-4 (OpenAI)\n"
                "Not recommended: small local models (tinyllama, smollm2) — unreliable Braille output\n\n"
                "Once enabled, usage: /braille <text>\n"
                "Supports Grade 1 (uncontracted) and Grade 2 (contracted) Braille ASCII.")
    
    from agents.interpretclaw.commands._memory import recall, remember
    
    query = args.strip()
    if not query:
        return "Usage: /braille <text>  — Converts English to Braille ASCII"

    grade = 2
    if "grade 1" in query.lower() or "uncontracted" in query.lower():
        grade = 1
        query = query.replace("grade 1", "").replace("uncontracted", "").strip()
    
    prompt = f"""Convert this English text to Grade {grade} Braille using standard ASCII Braille notation.
Use these Braille ASCII conventions:
- Capital sign: , (comma before capital letter)
- Number sign: # (hash before numbers)
- Period: . (dot)
- Each Braille cell mapped to its standard ASCII equivalent
- Grade {grade}: {"letter-by-letter" if grade == 1 else "use standard contractions"}

Text: {query}

Return in this format:
ORIGINAL: [text]
BRAILLE ASCII: [braille]"""

    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    remember(command="braille", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.80,
             metadata={"grade": grade})
    return result
