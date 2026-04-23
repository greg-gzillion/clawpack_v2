"""A2A Handler for ClawCoder - Code generation with WebClaw + LLM"""
import sys
from pathlib import Path

CLAW_CODER_DIR = Path(__file__).parent
PROJECT_ROOT = CLAW_CODER_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CLAW_CODER_DIR))

from agents.llmclaw.agent_handler import process_task as _llm
from agents.webclaw.providers.webclaw_provider import WebclawProvider
webclaw = WebclawProvider()

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        if cmd in ("code", "/code") and query:
            ctx = webclaw.search_with_context(query, max_results=3)
            result = _llm(f"/llm Write clean, well-commented code. Context: {ctx}\nTask: {query}").get("result","")
        elif cmd in ("explain", "/explain") and query:
            result = _llm(f"/llm Explain this code in detail: {query}").get("result","")
        elif cmd in ("debug", "/debug") and query:
            result = _llm(f"/llm Debug this code, find issues and suggest fixes: {query}").get("result","")
        elif cmd in ("review", "/review") and query:
            result = _llm(f"/llm Review this code, provide feedback on style, performance, bugs: {query}").get("result","")
        elif cmd in ("tutorial", "/tutorial") and query:
            result = _llm(f"/llm Create a programming tutorial for: {query}").get("result","")
        else:
            ctx = webclaw.search_with_context(query, max_results=3)
            result = _llm(f"/llm Context: {ctx}\nTask: {query}").get("result","")

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
