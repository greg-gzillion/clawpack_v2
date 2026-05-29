"""doc command - Generate medical documents (reports, referrals, treatment plans)"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "doc"

def run(args: str, agent=None) -> str:
    from agents.mediclaw.commands._memory import recall, remember
    
    query = args.strip()
    if not query:
        return """Usage: /doc <type> <details>
Types:
  /doc medical report <condition> - patient name: <name> - findings: <text>
  /doc referral letter <condition> to <specialty> - patient: <name>
  /doc treatment plan <condition> - patient: <name>
  /doc discharge <condition> - patient: <name> - hospital: <name>"""
    
    # Detect document type
    doc_type = "medical report"
    if "referral" in query.lower():
        doc_type = "referral letter"
    elif "treatment plan" in query.lower():
        doc_type = "treatment plan"
    elif "discharge" in query.lower():
        doc_type = "discharge instructions"
    
    prompt = f"""Generate a professional {doc_type} based on the following:

{query}

Include:
- Patient information section (if provided)
- Clinical findings and assessment
- Recommendations and follow-up
- Healthcare provider signature block
- Disclaimer: This is a draft for review by a licensed healthcare professional.

Format as a clean, structured medical document. Use professional medical terminology appropriate for clinical documentation."""
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    # Export via docuclaw for formatting
    if agent and hasattr(agent, 'call_agent'):
        try:
            exported = agent.call_agent("docuclaw", f"/create {doc_type}: {query}\n\n{result[:3000]}", timeout=60)
            if exported:
                result = str(exported) + "\n\n---\n\n" + result
        except Exception:
            pass
    
    remember(command="doc", query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85,
             metadata={"doc_type": doc_type})
    return result
