"""ask command - AI legal Q&A via WebClaw"""

name = "/ask"

def run(args):
    if not args:
        return "Usage: /ask [question]"
    import requests
    try:
        response = requests.post(
            "http://127.0.0.1:8766/v1/message/webclaw",
            json={"task": f"/llm {args}", "agent": "lawclaw"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("result", "No response")
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
