"""brief command - Case brief writer"""
import re

name = "/brief"

from agents.lawclaw.commands._helpers import llm, webclaw, chronicle, delegate
from agents.lawclaw.commands._memory import show_prior, remember


def run(args, agent=None):
    if not args:
        return "Usage: /brief [case name]"

    output = []
    output.append("")
    output.append("=" * 60)
    output.append(f"BRIEF: {args[:100]}{'...' if len(args) > 100 else ''}")
    output.append("=" * 60)

    prior = show_prior(args, output)

    try:
        # STEP 1: Search Chronicle
        output.append("")
        output.append("[1/3] Searching Chronicle...")
        chronicle_context = ""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            results = chronicle.recover_by_context(args + " case court", limit=10)
            if results:
                lines = []
                for r in results[:5]:
                    ctx = r["context"] if isinstance(r, dict) else str(r)
                    url = r["url"] if isinstance(r, dict) else ""
                    lines.append(f"SOURCE: {url}\n{ctx[:1000]}")
                chronicle_context = "\n\n---\n\n".join(lines)
                output.append(f"  Found {len(results)} references")
        except Exception as e:
            output.append(f"  Error: {e}")

        # STEP 2: Fetch web sources
        output.append("[2/3] Fetching web sources...")
        urls_found = re.findall(r'https?://[^\s\)\]\<\>\"]+', args + " " + chronicle_context)
        web_context = ""
        for url in urls_found[:3]:
            try:
                resp = requests.post(f"{A2A}/v1/message/webclaw", json={"task": f"fetch {url}"}, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("result", "")
                    if content and "fetch failed" not in content.lower():
                        web_context += f"\n\nSOURCE: {url}\n{content[:600]}"
            except:
                pass

        # STEP 3: LLM brief
        output.append("[3/3] Writing brief...")
        prompt = f"""Write a legal case brief for: {args}

Include: Case Name, Citation, Facts, Procedural History, Issue(s), Holding, Reasoning/Rule, Concurrences/Dissents, Significance.

CHRONICLE: {chronicle_context if chronicle_context else "None"}
WEB: {web_context if web_context else "None"}

Brief:"""
        resp = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=180)
        
        result = ""
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result:
                output.append("")
                output.append("=" * 60)
                output.append(result)
                output.append("=" * 60)
            else:
                output.append("ERROR: Empty response")
        
        # Write to shared memory
        if result:
            remember(
                command="/brief",
                query=args[:200],
                result_summary=result[:400],
                source_type="web_verified" if web_context else "chronicle",
                confidence=0.85 if web_context else 0.80,
            )

        return "\n".join(output)
    except Exception as e:
        output.append(f"ERROR: {str(e)[:200]}")
        return "\n".join(output)