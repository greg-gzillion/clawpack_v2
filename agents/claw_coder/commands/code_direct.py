"""code command - Direct import of llmclaw (bypasses A2A)"""
import sys
from pathlib import Path

# Add llmclaw to path
LLMCLAW_PATH = Path(__file__).parent.parent.parent / "llmclaw"
sys.path.insert(0, str(LLMCLAW_PATH))

name = "code"

def run(prompt: str) -> str:
    """Generate code using direct llmclaw import"""
    if not prompt:
        return "Usage: code <prompt>"
    
    coding_prompt = f"Write code for: {prompt}. Provide only the code with brief comments."
    
    try:
        # Direct import - no A2A overhead!
        from commands.llm_smart import run as llm_run
        return llm_run(coding_prompt)
    except Exception as e:
        return f"Error: {str(e)}"
