"""A2A Handler for ClawCoder - Uses WebClaw references for code generation"""
import sys
from pathlib import Path

CLAW_CODER_DIR = Path(__file__).parent
PROJECT_ROOT = CLAW_CODER_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

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
        if cmd in ("/code", "code") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Write clean, well-commented code. References: {ctx}\nTask: {query}").get("result","")
        elif cmd in ("/explain", "explain") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Explain this code. References: {ctx}\nCode: {query}").get("result","")
        elif cmd in ("/debug", "debug") and query:
            result = _llm(f"/llm Debug and fix this code: {query}").get("result","")
        elif cmd in ("/review", "review") and query:
            result = _llm(f"/llm Code review: {query}").get("result","")
        elif cmd in ("/tutorial", "tutorial") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Tutorial. References: {ctx}\nTopic: {query}").get("result","")
        elif cmd in ("/find", "find") and query:
            result = webclaw.search_with_context(f"claw_coder {query}", max_results=10)
        elif cmd in ("/help",):
            result = "ClawCoder - 1,566 References\n  /code /explain /debug /review /tutorial /find /stats"
        elif cmd in ("/stats",):
            result = f"ClawCoder | 1,566 WebClaw References | 60+ Languages"
        else:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Context: {ctx}\nTask: {query}").get("result","")

        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
