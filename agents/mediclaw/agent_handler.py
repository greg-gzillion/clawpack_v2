"""A2A Handler for Mediclaw - Medical references via WebClaw + LLM"""
import sys
from pathlib import Path

MEDICLAW_DIR = Path(__file__).parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.webclaw.providers.webclaw_provider import WebclawProvider
provider = WebclawProvider()

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        # Search WebClaw for medical context
        search_query = f"{query} medical"
        context = provider.search_with_context(search_query, max_results=5)
        
        # For listing sources, check the references directory
        if cmd == "/sources" or cmd == "/stats":
            refs_path = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/mediclaw")
            if refs_path.exists():
                sources = sorted([d.name for d in refs_path.iterdir() if d.is_dir()])
                if cmd == "/sources":
                    result = f"Medical Sources ({len(sources)}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(sources, 1))
                else:
                    result = f"Medical Sources: {len(sources)} specialties\nProviders: Groq -> Obliterated Ollama -> OpenRouter"
                return {"status": "success", "result": result}

        # Synthesize with LLM using the context
        sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))
        from commands.llm_enhanced import run as llm_run
        
        prompt_prefix = {
            "/diagnose": f"Using this medical context, provide differential diagnosis for: {query}\n\nContext:\n{context}",
            "/treatment": f"Using this medical context, provide treatment guidelines for: {query}\n\nContext:\n{context}",
            "/research": f"Using this medical context, provide medical research on: {query}\n\nContext:\n{context}",
        }
        
        prompt = prompt_prefix.get(cmd, f"Using this medical context, answer: {query}\n\nContext:\n{context}")
        result = llm_run(prompt)
        
        if result:
            return {"status": "success", "result": result}
        return {"status": "success", "result": context}

    except Exception as e:
        return {"status": "error", "result": str(e)}
