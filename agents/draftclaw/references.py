"""DraftClaw References - Chronicle/WebClaw/DataClaw integration for technical specs."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

def search_references(query, agent_callable):
    """Search chronicle, webclaw, and dataclaw for technical reference material."""
    parts = []
    try:
        web = agent_callable("webclaw", f"search technical drawing {query} specifications", timeout=10)
        if web: parts.append(str(web)[:1000])
    except: pass
    try:
        data = agent_callable("dataclaw", f"search {query}", timeout=10)
        if data: parts.append(str(data)[:1000])
    except: pass
    return chr(10).join(parts) if parts else ""
