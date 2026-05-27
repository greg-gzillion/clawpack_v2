"""ask command - AI law Q&A with full context via LLMClaw"""
import requests
import json

name = "/ask"
A2A = "http://127.0.0.1:8766"

def run(args):
    if not args:
        return "Usage: /ask [law question]"

    output = []
    output.append("=" * 70)
    output.append("LAW Q&A")
    output.append("=" * 70)
    output.append(f"QUESTION: {args[:200]}{'...' if len(args) > 200 else ''}")
    output.append("")

    try:
        # STEP 1: Search Chronicle for relevant references
        output.append("[1/3] Searching Chronicle for relevant law references...")
        chronicle_context = ""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            results = chronicle.recover_by_context(args, limit=10)
            if results:
                lines = []
                for r in results[:5]:
                    ctx = r["context"] if isinstance(r, dict) else str(r)
                    url = r["url"] if isinstance(r, dict) else ""
                    lines.append(f"SOURCE: {url}\n{ctx[:1000]}")
                chronicle_context = "\n\n---\n\n".join(lines)
                output.append(f"  Found {len(results)} related references")
            else:
                output.append("  No Chronicle references found")
        except Exception as e:
            output.append(f"  Chronicle error: {e}")

        # STEP 2: Fetch any URLs found in the question or Chronicle results
        output.append("[2/3] Fetching relevant web sources...")
        import re
        urls_found = re.findall(r'https?://[^\s\)\]\<\>\"]+', args + " " + chronicle_context)
        web_context = ""
        for url in urls_found[:3]:
            try:
                resp = requests.post(
                    f"{A2A}/v1/message/webclaw",
                    json={"task": f"fetch {url}", "agent": "lawclaw"},
                    timeout=15
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("result", "")
                    if content and "fetch failed" not in content.lower():
                        web_context += f"\n\nSOURCE: {url}\n{content[:600]}"
                        output.append(f"  Fetched: {url[:60]}...")
            except:
                pass
        if not web_context:
            output.append("  No web sources fetched")

        # STEP 3: Build prompt and call LLM
        output.append("[3/3] Researching answer via LLM...")
        prompt = f"""You are an experienced legal researcher. Answer the following law question thoroughly and accurately.

QUESTION:
{args}

INDEXED LEGAL REFERENCES FROM CHRONICLE DATABASE:
{chronicle_context if chronicle_context else "No indexed references found."}

LIVE WEB SOURCES:
{web_context if web_context else "No live web sources fetched."}

Instructions:
- Answer the question directly and comprehensively
- Cite specific statutes, case law, and legal principles
- Reference any relevant sources from the Chronicle database or web sources above
- Note any jurisdictional variations if applicable
- If the answer depends on specific facts not provided, explain what facts would matter and why
- Provide practical guidance where appropriate
- End with key takeaways

Answer:"""

        resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=180
        )

        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result:
                output.append("=" * 70)
                output.append("ANSWER:")
                output.append("=" * 70)
                output.append(result)
                output.append("=" * 70)
            else:
                output.append("ERROR: LLM returned empty response")
        else:
            output.append(f"ERROR: LLM returned status {resp.status_code}")

        return "\n".join(output)

    except Exception as e:
        output.append(f"\nERROR: {str(e)[:300]}")
        return "\n".join(output)