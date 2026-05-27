"""analyze command - Comprehensive law text analysis"""
import re
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

name = "/analyze"
A2A = "http://127.0.0.1:8766"

def run(args):
    if not args:
        return "Usage: /analyze [law text, case citation, statute, or legal document excerpt]"

    output = []
    output.append("=" * 70)
    output.append("LAW TEXT ANALYSIS")
    output.append("=" * 70)
    output.append(f"TEXT: {args[:200]}{'...' if len(args) > 200 else ''}")
    output.append("")

    try:
        # STEP 1: Search Chronicle for relevant references
        output.append("[1/4] Searching Chronicle...")
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
                    lines.append(f"SOURCE: {url}\n{ctx[:1200]}")
                chronicle_context = "\n\n---\n\n".join(lines)
                output.append(f"  Found {len(results)} related references")
            else:
                output.append("  No Chronicle references found")
        except Exception as e:
            output.append(f"  Chronicle error: {e}")

        # STEP 2: Extract URLs and fetch live content via WebClaw
        output.append("[2/4] Fetching live URLs via WebClaw...")
        urls_found = re.findall(r'https?://[^\s\)\]\<\>\"]+', args + " " + chronicle_context)
        output.append(f"  Found {len(urls_found)} URLs")

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
                        web_context += f"\n\nLIVE URL: {url}\n{content[:800]}"
                        output.append(f"  Fetched: {url[:60]}...")
            except:
                pass
        if not web_context:
            output.append("  No live URLs fetched")

        # STEP 3: Build comprehensive prompt
        output.append("[3/4] Building analysis prompt...")
        prompt = f"""You are a senior legal analyst. Perform a comprehensive analysis of the following legal text.

TEXT TO ANALYZE:
{args}

CHRONICLE REFERENCES (indexed legal database):
{chronicle_context if chronicle_context else "No indexed references found."}

LIVE WEB DATA:
{web_context if web_context else "No live web data fetched."}

Provide a thorough structured analysis including ALL of the following sections:

1. SUMMARY (2-3 sentences overview)

2. KEY LEGAL CONCEPTS IDENTIFIED
   - List and define each legal concept found in the text
   - Explain their significance in legal context

3. RELEVANT STATUTES AND REGULATIONS
   - Cite specific statutes, codes, or regulations referenced
   - Explain how they apply

4. CASE LAW AND PRECEDENTS
   - Identify any cases referenced or relevant to the text
   - Explain their holdings and how they apply

5. LEGAL PRINCIPLES AND DOCTRINES
   - Identify the underlying legal principles
   - Explain how they operate in this context

6. POTENTIAL ISSUES AND IMPLICATIONS
   - Flag any legal issues, ambiguities, or concerns
   - Discuss practical implications

7. JURISDICTIONAL CONSIDERATIONS
   - Identify relevant jurisdictions
   - Note any jurisdictional conflicts or considerations

8. RELATED AREAS FOR FURTHER RESEARCH
   - Suggest specific topics, cases, or statutes to investigate
   - Recommend resources for deeper analysis

9. CONCLUSION
   - Synthesize the analysis into actionable insights

Cite specific sources from the Chronicle references and live web data wherever possible. Use the format [Source: URL] for citations.

Analysis:"""

        # STEP 4: Call LLM via A2A llmclaw (constitutional - llmclaw IS Sovereign Gateway per Article II)
        output.append("[4/4] Synthesizing via LLM...")
        resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=180
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result:
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