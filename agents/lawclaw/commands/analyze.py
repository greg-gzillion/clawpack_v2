"""analyze command - Analyze legal text via A2A"""
import requests

name = "/analyze"
A2A = "http://127.0.0.1:8766"

def run(args):
    if not args:
        return "Usage: /analyze [legal text to analyze]"
    
    try:
        print("\n?? Analyzing legal text...")
        
        # 1. Search WebClaw for relevant legal context
        web_resp = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"/search legal analysis {args[:50]}", "agent": "lawclaw"},
            timeout=10
        )
        
        context = ""
        if web_resp.status_code == 200:
            context = web_resp.json().get("result", "")[:1000]
        
        # 2. Build analysis prompt
        prompt = f"""You are a legal expert. Analyze the following legal text:

TEXT TO ANALYZE:
{args[:2000]}

REFERENCE CONTEXT:
{context if context else "No additional context available"}

Provide a structured analysis including:
1. Key legal concepts identified
2. Relevant legal principles
3. Potential legal implications
4. Suggested areas for further research

Analysis:"""
        
        # 3. Get LLM analysis via A2A
        llm_resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/ask {prompt}", "agent": "lawclaw"},
            timeout=90
        )
        
        if llm_resp.status_code == 200:
            result = llm_resp.json().get("result", "No analysis available")
            return f"\n{'='*60}\n?? LEGAL ANALYSIS\n{'='*60}\n\nText: {args[:100]}...\n\n{result}\n{'='*60}"
        else:
            return f"Error: LLM service returned {llm_resp.status_code}"
            
    except Exception as e:
        return f"Error analyzing text: {str(e)[:200]}"
