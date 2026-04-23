"""A2A Handler for ClawCoder - Code generation with WebClaw + LLM"""
import sys
from pathlib import Path

CLAW_CODER_DIR = Path(__file__).parent
PROJECT_ROOT = CLAW_CODER_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CLAW_CODER_DIR))

from agents.webclaw.providers.webclaw_provider import WebclawProvider
webclaw = WebclawProvider()

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""

    try:
        sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))
        from commands.llm_enhanced import run as llm_run

        if cmd in ("code", "/code"):
            context = webclaw.search_with_context(args, max_results=3)
            prompt = f"Write code for: {args}. Context: {context}. Provide clean, well-commented code."
            result = llm_run(prompt)
        elif cmd in ("explain", "/explain"):
            result = llm_run(f"Explain this code in detail: {args}")
        elif cmd in ("debug", "/debug"):
            result = llm_run(f"Debug this code, find issues and suggest fixes: {args}")
        elif cmd in ("review", "/review"):
            result = llm_run(f"Review this code, provide feedback on style, performance, bugs: {args}")
        elif cmd in ("tutorial", "/tutorial"):
            result = llm_run(f"Create a programming tutorial for: {args}")
        else:
            context = webclaw.search_with_context(task, max_results=3)
            result = llm_run(f"Context: {context}\n\nTask: {task}")

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
