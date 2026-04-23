"""court command - County court info with LLM (ALL THROUGH A2A)"""
import requests
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

name = "/court"
A2A = "http://127.0.0.1:8766"

def run(args):
    if not args:
        return "Usage: /court [state] [county]"

    try:
        # 1. Get context from WebClaw via A2A
        search_response = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"/search {args} court", "agent": "lawclaw"},
            timeout=10
        )
        
        context = ""
        if search_response.status_code == 200:
            data = search_response.json()
            context = data.get("result", "")

        # 2. Build prompt
        prompt = f"""You are a legal assistant. Provide information about the court in {args}.

Context from database:
{context if context else "No specific context available."}

Question: What court serves {args}? Include address, jurisdiction, and contact info if known.

Answer:"""

        # 3. Get LLM response via A2A (calls llmclaw)
        llm_response = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/ask {prompt}", "agent": "lawclaw"},
            timeout=60
        )
        
        if llm_response.status_code == 200:
            data = llm_response.json()
            return f"\n??? COURT INFO: {args}\n{'-'*50}\n{data.get('result', 'No response')}\n{'-'*50}"
        else:
            return f"A2A LLM error: {llm_response.status_code}"

    except Exception as e:
        return f"Court info for: {args}\n[Error: {str(e)[:100]}]"
