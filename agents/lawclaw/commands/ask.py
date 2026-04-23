"""ask command - AI law Q&A via LLMClaw"""
import requests
import json

name = "/ask"
A2A = "http://127.0.0.1:8766"

def run(args):
    if not args:
        return "Usage: /ask <question>"
    
    try:
        print(f"\n? Asking: {args}...")
        
        # SIMPLE - Just pass the question directly
        # Build a clean prompt
        prompt = f"Legal question: {args}. Answer concisely."
        
        # Escape for JSON
        task = json.dumps(f"/llm {prompt}")
        
        # Call LLMClaw
        llm_resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=60
        )
        
        if llm_resp.status_code == 200:
            result = llm_resp.json().get("result", "No response")
            return f"\n{'='*60}\n? {args}\n{'='*60}\n\n{result}\n{'='*60}"
        else:
            return f"Error: LLM service returned {llm_resp.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)[:200]}"
