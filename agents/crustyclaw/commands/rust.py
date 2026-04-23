"""Rust code generation command"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run(args):
    if not args:
        return "Usage: /rust <task>\nExample: /rust create a TCP server"
    
    from agents.webclaw.providers.webclaw_provider import WebclawProvider
    ctx = WebclawProvider().search_with_context(f"rust {args}", max_results=3)
    
    sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))
    from commands.llm_enhanced import run as llm_run
    return llm_run(f"You are a Rust expert. Context: {ctx}\n\nWrite Rust code for: {args}")
