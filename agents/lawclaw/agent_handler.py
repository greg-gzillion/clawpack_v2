"""A2A Handler for LawClaw - Legal research with WebClaw enrichment"""
import sys
import os
import requests
from pathlib import Path

LAWCLAW_DIR = Path(__file__).parent
os.chdir(str(LAWCLAW_DIR))
sys.path.insert(0, str(LAWCLAW_DIR.parent.parent))

A2A = "http://127.0.0.1:8766"

def search_law_references(query: str) -> str:
    """Search WebClaw for LAW references (not generic legal)"""
    try:
        # Search specifically for law references
        response = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"search {query} law"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                result = data.get("result", "")
                # Clean for A2A
                result = result.replace('\n', ' ').replace('\r', ' ')
                result = result.replace('"', "'")
                return result
    except:
        pass
    return ""

def process_task(task: str, agent: str = None):
    """Process A2A task"""
    task = task.strip()
    
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    try:
        if cmd == "/ask" or cmd == "ask":
            print("[lawclaw] Searching WebClaw for law references...")
            context = search_law_references(args)
            
            if context:
                prompt = f"Law Reference: {context} Question: {args}"
                prompt = prompt.replace('\n', ' ').replace('"', "'")
            else:
                prompt = f"Legal Question: {args}"
            
            response = requests.post(
                f"{A2A}/v1/message/llmclaw",
                json={"task": f"/llm {prompt}"},
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                return {"status": "success", "result": data.get("result", "")}
            else:
                return {"status": "error", "result": f"LLM error: {response.status_code}"}
                
        elif cmd == "search" or cmd == "/search":
            result = search_law_references(args)
            if result:
                return {"status": "success", "result": result}
            return {"status": "error", "result": "No results found"}
        
        else:
            return process_task(f"/ask {task}", agent)
            
    except Exception as e:
        return {"status": "error", "result": str(e)}

