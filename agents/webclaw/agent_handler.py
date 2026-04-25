"""A2A Handler for WebClaw - Full Content with Citations"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from webclaw import Webclaw
from providers.webclaw_provider import WebclawProvider

webclaw = Webclaw()
provider = WebclawProvider()

def process_task(task: str, agent: str = None):
    task = task.strip()
    
    # Fetch URL with full content and citation
    if task.startswith('fetch ') or task.startswith('http'):
        url = task.replace('fetch ', '', 1).strip() if task.startswith('fetch ') else task
        try:
            result = webclaw.fetch_with_citation(url)
            return {'status': 'success', 'result': str(result)}
        except Exception as e:
            return {'status': 'error', 'result': str(e)}
    
    # Search indexed references
    if task.startswith('search '):
        query = task[7:].strip()
    else:
        query = task
    
    try:
        result = provider.search_with_context(query)
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'result': str(e)}
