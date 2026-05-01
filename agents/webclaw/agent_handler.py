"""A2A Handler for WebClaw - Full Content with Citations"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from webclaw import Webclaw
from agents.webclaw.providers.webclaw_provider import WebclawProvider

webclaw = Webclaw()
provider = WebclawProvider()

def process_task(task: str, agent: str = None):
    task = task.strip()

    # Fetch URL with full content and citation
    if task.startswith('fetch ') or task.startswith('http'):
        url = task.replace('fetch ', '', 1).strip() if task.startswith('fetch ') else task
        try:
            result = webclaw.fetch_with_citation(url)
            if result.get("success"):
                return {'status': 'success', 'result': result["citation"] + "\n\n" + result["content"]}
            return {'status': 'error', 'result': result.get("error", "fetch failed")}
        except Exception as e:
            return {'status': 'error', 'result': str(e)}

    # Search indexed references + chronicle URLs
    if task.startswith('search '):
        query = task[7:].strip()
    else:
        query = task

    try:
        # 1. Search local markdown references
        result = provider.search_with_context(query)
        
        # 2. Search chronicle index and fetch content with citations
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            chronicle_results = chronicle.recover_by_context(query, limit=2000000)
            if chronicle_results:
                result += "\n\n=== Web Results ==="
                for c in chronicle_results:
                    url = c.url if hasattr(c, 'url') else str(c)
                    try:
                        cited = webclaw.fetch_with_citation(url)
                        if cited.get("success"):
                            result += f"\n\n{cited['citation']}\n{cited['content']}"
                        else:
                            result += f"\n\n{url} (fetch failed)"
                    except:
                        result += f"\n\n{url} (fetch error)"
        except Exception as e:
            result += f"\n\n(chronicle search error: {e})"
        
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'result': str(e)}
