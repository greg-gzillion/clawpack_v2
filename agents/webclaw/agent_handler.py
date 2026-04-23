"""A2A Handler for WebClaw - Uses SQLite index"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents.webclaw.providers.webclaw_provider import WebclawProvider

provider = WebclawProvider()

def process_task(task: str, agent: str = None):
    """Process A2A search task"""
    task = task.strip()
    
    if task.startswith("search "):
        query = task[7:].strip()
    else:
        query = task
    
    try:
        result = provider.search_with_context(query)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
