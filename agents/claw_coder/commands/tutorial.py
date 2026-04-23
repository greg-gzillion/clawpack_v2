"""tutorial command - Programming tutorial via LLMClaw"""
import requests
name = "tutorial"
A2A = "http://127.0.0.1:8766"

def run(args: str) -> str:
    if not args:
        return "Usage: tutorial <topic> [language] [level]"
    prompt = f"Create a programming tutorial for: {args}"
    try:
        response = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}"}, timeout=90)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", "") if data.get("status") == "success" else data.get("result", "Error")
        return f"A2A Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
