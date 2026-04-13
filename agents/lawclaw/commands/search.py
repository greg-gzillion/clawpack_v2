"""search command - Search legal references via WebClaw"""

name = "/search"

def run(args):
    """Execute search via WebClaw A2A"""
    import requests
    import json
    
    if not args:
        return "Usage: /search [query]"
    
    try:
        response = requests.post(
            "http://127.0.0.1:8766/v1/message/webclaw",
            json={"task": f"/search {args}", "agent": "lawclaw"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("result", "No results")
        return f"WebClaw error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
