"""code command - Generate code with WebClaw reference enrichment"""
import sys
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

name = "code"
A2A = "http://127.0.0.1:8766"

def search_chronicle(query: str) -> str:
    """Search WebClaw via A2A - THIS WORKS!"""
    try:
        response = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"search {query}"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                result = data.get("result", "")
                if result and len(result) > 10:
                    return result.replace('\n', ' ').replace('"', "'")
    except Exception as e:
        print(f"[claw_coder] WebClaw error: {str(e)[:50]}")
    return ""

def run(prompt: str) -> str:
    """Generate code enriched with WebClaw references"""
    if not prompt:
        return "Usage: code <prompt>"
    
    print("[claw_coder] Searching WebClaw...")
    references = search_chronicle(prompt)
    
    if references:
        enriched = f"Reference: {references} Task: {prompt}"
        print(f"[claw_coder] Found references! ({len(references)} chars)")
    else:
        enriched = f"Write code for: {prompt}. Provide only the code with brief comments."
        print("[claw_coder] No references, using standard prompt...")
    
    try:
        response = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {enriched}"},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("result", "No code generated")
        return f"Error: LLM call failed"
    except Exception as e:
        return f"Error: {str(e)}"


