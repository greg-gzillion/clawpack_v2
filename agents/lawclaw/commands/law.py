"""law command - Legal research via Chronicle + CourtListener + LLM"""
import requests
from pathlib import Path

name = "/law"
A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"


def _log(agent, event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent, event=event, detail=str(detail)[:500])
    except Exception:
        pass


def get_cl_token():
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        for line in env_path.read_text().split("\n"):
            if "COURTLISTENER_TOKEN" in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception as e:
        _log("lawclaw", "law_token_error", e)
    return ""


def llm(prompt, timeout=120):
    try:
        resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result and len(result) > 20:
                return result
    except Exception as e:
        _log("lawclaw", "law_llm_error", str(e)[:100])
    return ""


def chronicle_search(query, limit=10):
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        return results if results else []
    except Exception as e:
        _log("lawclaw", "law_chronicle_error", str(e)[:100])
    return []


def run(args):
    if not args:
        return (
            "[LAW] Usage: /law [law topic or question]\n"
            "  /law qualified immunity\n"
            "  /law fourth amendment search and seizure\n"
            "  /law breach of contract elements Texas"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"LAW: {args}")
    out.append("=" * 60)

    try:
        # STEP 1: Chronicle
        out.append("")
        out.append("[1/3] Searching Chronicle...")
        chronicle_results = chronicle_search(f"{args} law doctrine elements", limit=10)
        chronicle_context = ""
        if chronicle_results:
            parts = []
            for r in chronicle_results[:6]:
                ctx = r["context"] if isinstance(r, dict) else str(r)
                url = r.get("url", "") if isinstance(r, dict) else ""
                parts.append(f"SOURCE: {url}\n{ctx[:1000]}")
            chronicle_context = "\n---\n".join(parts)
            out.append(f"  {len(chronicle_results)} Chronicle references")

        # STEP 2: CourtListener case law
        out.append("[2/3] Searching CourtListener opinions...")
        token = get_cl_token()
        cl_context = ""
        cl_urls = []
        if token:
            r = requests.get(
                f"{COURTLISTENER_API}/search/",
                params={"q": args, "type": "o", "order_by": "score desc", "page_size": 8,
                "court": "scotus,ca1,ca2,ca3,ca4,ca5,ca6,ca7,ca8,ca9,ca10,ca11,cadc,cafc"},
                headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
                timeout=15,
            )
            if r.status_code == 200:
                data = r.json()
                results = data.get("results", [])
                if results:
                    count = data.get("count", 0)
                    count_str = f"{int(count):,}" if count else "unknown"
                    out.append(f"  {len(results)} cases found ({count_str} total)")
                    for o in results[:8]:
                        case_name = o.get("caseName", "Unknown")
                        date = o.get("dateFiled", "?") or "?"
                        absolute_url = o.get("absolute_url", "")
                        cl_url = f"https://www.courtlistener.com{absolute_url}" if absolute_url else ""
                        citation = o.get("citation", "") or ""
                        docket = o.get("docketNumber", "") or ""
                        court = o.get("court_citation_string", "") or ""

                        out.append(f"    [{date}] {case_name}")
                        if court:
                            out.append(f"      Court: {court}")
                        if citation:
                            out.append(f"      Cite: {citation}")
                        if cl_url:
                            out.append(f"      URL: {cl_url}")
                            cl_urls.append(cl_url)
                        out.append("")
                    cl_context = "\n".join(cl_urls)
                else:
                    out.append("  No CourtListener cases found")
            else:
                out.append(f"  CourtListener API error: {r.status_code}")
        else:
            out.append("  (Add COURTLISTENER_TOKEN to .env for case law)")

        # STEP 3: LLM synthesis
        out.append("[3/3] Synthesizing law overview...")

        prompt = f"""Research this law topic: {args}

CHRONICLE REFERENCES:
{chronicle_context[:2500] if chronicle_context else "None."}

COURTLISTENER CASE LAW:
{cl_context[:2500] if cl_context else "None."}

Create a structured law overview with these sections (omit any with no data):

DEFINITION - Plain English definition in 2-3 sentences
KEY ELEMENTS - What must be shown or proven
CONTROLLING AUTHORITY - Key cases with citations from the CourtListener results above
PRACTICAL NOTES - Common issues, jurisdictional variations, recent developments
FURTHER RESEARCH - CourtListener search URL for this topic

Use ONLY the data provided above for case citations.
Do not invent case names or citations.
If data is limited, note that rather than fabricating.

Law Overview:"""

        result = llm(prompt, timeout=120)

        out.append("")
        out.append("=" * 60)
        if result and len(result) > 50:
            out.append(result)
        else:
            out.append("[LLM unavailable]")
            if cl_context:
                out.append("")
                out.append("[COURTLISTENER RESULTS]")
                out.append(cl_context[:2000])
            if chronicle_context:
                out.append("")
                out.append("[CHRONICLE REFERENCES]")
                out.append(chronicle_context[:1500])
        out.append("=" * 60)

        if all_cl_urls := list(dict.fromkeys(cl_urls)):
            out.append("")
            out.append("  Cases (use /docket [URL] for full entries):")
            for url in all_cl_urls[:8]:
                out.append(f"    {url}")

        out.append("")
        out.append("  Search CourtListener: https://www.courtlistener.com/?q=" + args.replace(" ", "+") + "&type=o")

        return "\n".join(out)

    except Exception as e:
        _log("lawclaw", "law_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)