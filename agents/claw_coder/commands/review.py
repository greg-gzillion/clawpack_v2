"""review command - Review code via LLMClaw"""
import requests
name = "review"
A2A = "http://127.0.0.1:8766"

def run(code: str) -> str:
    if not code:
        return "Usage: review <code>"
    prompt = f"Review this code for quality, bugs, and improvements: {code}"
    try:
        response = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}"}, timeout=60)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", "") if data.get("status") == "success" else data.get("result", "Error")
        return f"A2A Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
