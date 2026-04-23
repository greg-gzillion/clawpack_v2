"""A2A Handler for CrustyClaw - Rust AI Shell"""
import sys
from pathlib import Path

CRUSTYCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = CRUSTYCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.llmclaw.agent_handler import process_task as _llm

def process_task(task: str, agent: str = None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        if cmd in ("/code", "/rust") and query:
            result = _llm(f"/llm Write clean, idiomatic Rust code with comments for: {query}").get("result","")
        elif cmd in ("/explain") and query:
            result = _llm(f"/llm Explain this Rust concept clearly: {query}").get("result","")
        elif cmd in ("/fix", "/debug") and query:
            result = _llm(f"/llm Fix this Rust code, return ONLY fixed code: {query}").get("result","")
        elif cmd in ("/help",):
            result = "/code <task> | /fix <code> | /explain <concept> | /stats"
        elif cmd in ("/stats",):
            result = "CrustyClaw | Rust AI via LLMClaw"
        else:
            result = _llm(f"/llm You are a Rust expert. Answer: {query}").get("result","")

        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
