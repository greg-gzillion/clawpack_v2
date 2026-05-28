"""summarize command - Universal legal document summarizer via Chronicle + LLM"""
import re
from pathlib import Path

name = "/summarize"

from agents.lawclaw.commands._helpers import (
    log, llm, webclaw, chronicle, chronicle_context, cl_search, cl_token
)
from agents.lawclaw.commands._memory import show_prior, remember


def run(args):
    if not args:
        return (
            "[SUMMARIZE] Usage: /summarize [case name | docket URL | statute | text]\n"
            "  /summarize Miranda v Arizona\n"
            "  /summarize https://www.courtlistener.com/docket/67876857/...\n"
            "  /summarize 42 USC 1983"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"SUMMARIZE: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        is_url = args.startswith("http")
        is_docket = "courtlistener.com/docket/" in args
        is_case = " v " in args.lower() or " v. " in args.lower()

        # STEP 1: Chronicle
        out.append("")
        out.append("[1/3] Searching Chronicle...")
        chronicle_ctx = chronicle_context(f"{args} case law statute legal", limit=8)
        if chronicle_ctx:
            out.append("  Chronicle references found")

        # STEP 2: Source-specific fetch
        out.append("[2/3] Fetching source data...")
        source_text = ""

        if is_docket:
            docket_id = args.split("/docket/")[1].split("/")[0].split("?")[0]
            out.append(f"  Docket ID: {docket_id}")
            token = cl_token()
            if token:
                try:
                    import requests
                    r = requests.get(
                        f"https://www.courtlistener.com/api/rest/v4/dockets/{docket_id}/",
                        headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
                        timeout=15,
                    )
                    if r.status_code == 200:
                        d = r.json()
                        source_text = f"CASE: {d.get('case_name', 'Unknown')}\n"
                        source_text += f"Court: {d.get('court', 'Unknown')}\n"
                        source_text += f"Filed: {d.get('date_filed', 'Unknown')}\n"
                        source_text += f"Docket: {d.get('docket_number', 'Unknown')}\n"
                        out.append("  Docket metadata retrieved")
                except:
                    pass
        elif is_case:
            cases = cl_search(args, search_type="o", limit=5)
            if cases:
                out.append(f"  {len(cases)} case(s) found")
                for c in cases[:5]:
                    name = c.get("caseName", c.get("case_name", "Unknown"))
                    date = c.get("dateFiled", c.get("date_filed", "?")) or "?"
                    citation = c.get("citation", "") or ""
                    snippet = (c.get("text", "") or c.get("snippet", "") or "")[:500]
                    source_text += f"CASE: {name} ({date})\n"
                    if citation:
                        source_text += f"Cite: {citation}\n"
                    if snippet:
                        source_text += f"Text: {snippet}\n"
                    source_text += "\n"
        elif is_url:
            html = webclaw(args)
            if html and len(html) > 100:
                source_text = html[:5000]
                out.append(f"  URL content retrieved ({len(html)} chars)")
            else:
                out.append("  Could not fetch URL content")
        else:
            source_text = args
            out.append("  Processing text input")

        # STEP 3: LLM synthesis
        out.append("[3/3] Generating summary...")

        result = ""
        if source_text or chronicle_ctx:
            prompt = f"""Create a structured legal summary for: {args}

SOURCE DATA:
{source_text[:4000] if source_text else "No source data."}

CHRONICLE:
{chronicle_ctx[:2000] if chronicle_ctx else "None."}

Provide a structured summary:

OVERVIEW — 1-2 sentences on what this is
KEY FACTS — Relevant factual background (if a case)
ISSUE — The legal question presented
HOLDING — What was decided
REASONING — Why the court ruled as it did
SIGNIFICANCE — Why this matters, precedential value

Use ONLY the data provided. If a section has no data, say so rather than fabricating.
Under 300 words.

Summary:"""

            result = llm(prompt, timeout=120)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)
            else:
                out.append("  (LLM unavailable)")
                if source_text:
                    out.append("")
                    out.append("[RAW SOURCE DATA]")
                    out.append(source_text[:2000])
        else:
            out.append("  No data found to summarize.")
            out.append("  Try: /law [topic] or /docket [case URL]")

        if result:
            remember(command="/summarize", query=args[:200], result_summary=result[:400], source_type="web_verified", confidence=0.85)

        return "\n".join(out)

    except Exception as e:
        log("summarize_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)