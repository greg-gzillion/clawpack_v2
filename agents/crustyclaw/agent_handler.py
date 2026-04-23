"""A2A Handler for CrustyClaw - Rust assistant with WebClaw + LLM"""
import sys
import importlib.util
from pathlib import Path

CRUSTYCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = CRUSTYCLAW_DIR.parent.parent

# Load LLM chain
_llm_path = PROJECT_ROOT / "agents" / "llmclaw" / "commands" / "llm_enhanced.py"
_llm_spec = importlib.util.spec_from_file_location("llm_enhanced", _llm_path)
_llm_module = importlib.util.module_from_spec(_llm_spec)
_llm_spec.loader.exec_module(_llm_module)
llm_run = _llm_module.run

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        # Search WebClaw for Rust/code context
        sys.path.insert(0, str(PROJECT_ROOT))
        from agents.webclaw.providers.webclaw_provider import WebclawProvider
        ctx = WebclawProvider().search_with_context(f"rust {query}", max_results=3)

        if cmd in ("/rust", "/code", "rust", "code") and query:
            prompt = f"You are a Rust expert. Using this context: {ctx}\n\nTask: {query}\nProvide clean Rust code with explanations."
        elif cmd in ("/explain", "explain") and query:
            prompt = f"Explain this Rust concept clearly: {query}\nContext: {ctx}"
        elif cmd in ("/help", "help"):
            return {"status": "success", "result": "CrustyClaw Commands:\n  /rust <task> - Generate Rust code\n  /explain <concept> - Explain Rust concepts\n  /cargo <command> - Cargo operations\n  /stats - System status"}
        elif cmd in ("/stats", "stats"):
            result = "CrustyClaw | Rust binary + Chronicle bridge | LLM: Groq chain\nChronicle: WebClaw + DataClaw connected"
            return {"status": "success", "result": result}
        else:
            prompt = f"You are a Rust expert. Context: {ctx}\n\nQuestion: {query}"

        result = llm_run(prompt)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
