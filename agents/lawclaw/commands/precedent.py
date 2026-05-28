"""precedent command - Doctrine tracker by circuit via CourtListener + Chronicle + LLM"""
import requests
from pathlib import Path

name = "/precedent"
A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"

from agents.lawclaw.commands._helpers import (
    log, llm, webclaw, chronicle, chronicle_context,
    cl_token, cl_search, delegate, jurisdiction_root
)


def run(args):
    if not args:
        return (
            "[PRECEDENT] Usage: /precedent [doctrine or case]\n"
            "  /precedent qualified immunity\n"
            "  /precedent Miranda v Arizona\n"
            "  /precedent Fourth Amendment search and seizure\n"
            "  Tracks controlling authority, circuit splits, and trend direction"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"PRECEDENT: {args}")
    out.append("=" * 60)

    try:
        # STEP 1: Chronicle — existing indexed knowledge
        out.append("")
        out.append("[1/4] Searching Chronicle...")
        chronicle_ctx = chronicle_context(f"{args} precedent case law doctrine circuit", limit=8)
        if chronicle_ctx:
            out.append(f"  Chronicle references found")
        else:
            out.append("  No Chronicle matches")

        # STEP 2: CourtListener — find controlling cases by circuit
        out.append("[2/4] Finding controlling cases via CourtListener...")
        token = cl_token()
        if not token:
            out.append("  (Add COURTLISTENER_TOKEN to .env)")
        else:
            # Search SCOTUS first for controlling authority
            scotus_cases = cl_search(
                f"{args} Supreme Court",
                search_type="o",
                courts="scotus",
                order_by="score desc",
                limit=5,
            )
            import time

            # ... after scotus_cases = cl_search(...)
            time.sleep(1)  # Rate limit protection
            
            # Then circuit courts for splits
            circuit_cases = cl_search(
                f"{args} circuit court",
                search_type="o",
                courts="ca1,ca2,ca3,ca4,ca5,ca6,ca7,ca8,ca9,ca10,ca11,cadc,cafc",
                order_by="score desc",
                limit=10,
            )
            # Then circuit search
            circuit_cases = cl_search(...)
            
            all_cases = []
            if scotus_cases:
                out.append(f"  SCOTUS: {len(scotus_cases)} controlling cases")
                for c in scotus_cases:
                    all_cases.append(("SCOTUS", c))

            if circuit_cases:
                # Group by circuit
                by_circuit = {}
                for c in circuit_cases:
                    court = c.get("court_citation_string", "") or c.get("court", "") or "Unknown"
                    if court not in by_circuit:
                        by_circuit[court] = []
                    by_circuit[court].append(c)

                out.append(f"  Circuits: {len(by_circuit)} courts with relevant cases")
                for court, cases in sorted(by_circuit.items()):
                    out.append(f"    {court}: {len(cases)} case(s)")
                    for c in cases[:3]:
                        all_cases.append((court, c))

            if not all_cases:
                out.append("  No cases found")

        # STEP 3: LLM synthesis — doctrine analysis
        out.append("[3/4] Analyzing doctrine...")

        # Build case context
        case_lines = []
        case_urls = []
        for court, c in all_cases[:15]:
            name = c.get("caseName", c.get("case_name", "Unknown"))
            date = c.get("dateFiled", c.get("date_filed", "?")) or "?"
            citation = c.get("citation", "") or ""
            url = c.get("absolute_url", "")
            cl_url = f"https://www.courtlistener.com{url}" if url else ""
            if cl_url:
                case_urls.append(cl_url)
            case_lines.append(f"{court} | {name} ({date})")
            if citation:
                case_lines.append(f"  Cite: {citation}")
            if cl_url:
                case_lines.append(f"  URL: {cl_url}")

        cases_text = "\n".join(case_lines) if case_lines else "No cases found"

        if chronicle_ctx or all_cases:
            prompt = f"""Analyze the precedential landscape for: {args}

CHRONICLE REFERENCES:
{chronicle_ctx[:2000] if chronicle_ctx else "None."}

COURTLISTENER CASES BY COURT:
{cases_text[:3000]}

Provide a structured doctrine analysis:

CONTROLLING AUTHORITY — The binding SCOTUS case(s) and what they established
CIRCUIT SPLITS — Any divisions among circuits on this doctrine
TREND DIRECTION — Is the doctrine expanding, contracting, or stable?
PRACTICAL NOTE — What a litigant should know about arguing this issue

Use ONLY the case data provided above. Do not fabricate cases.
If a section has no data, say so rather than inventing.
Under 300 words.

Analysis:"""

            result = llm(prompt, timeout=120)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)

                # STEP 4: Offer cross-agent delegation
                out.append("[4/4] Available actions...")
                out.append("")

                # Delegate to docuclaw for memo creation
                if case_urls:
                    out.append(f"  /export — create a research memo from {len(case_urls)} cases")
                    out.append(f"    {len(case_urls)} case URLs available for document creation")
                    out.append("")

                # Delegate to plotclaw for circuit split visualization
                if len(all_cases) >= 5:
                    out.append(f"  /chart — visualize circuit split ({len(all_cases)} cases across multiple courts)")
                    out.append("")

        else:
            out.append("")
            out.append("  No data available for analysis.")
            out.append(f"  Try: /law {args} for general legal research")

        # Show case URLs for /docket chain
        unique_urls = list(dict.fromkeys(case_urls))
        if unique_urls:
            out.append("  Cases (use /docket [URL] for full entries):")
            for url in unique_urls[:8]:
                out.append(f"    {url}")

        out.append("")
        out.append("  Search CourtListener: https://www.courtlistener.com/?q=" + args.replace(" ", "+") + "&type=o")

        return "\n".join(out)

    except Exception as e:
        log("precedent_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)