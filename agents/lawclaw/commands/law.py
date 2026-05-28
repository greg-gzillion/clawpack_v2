"""law command - Legal research via Chronicle + CourtListener + LLM"""
import requests
from pathlib import Path

name = "/law"
A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"

from agents.lawclaw.commands._helpers import log, llm, chronicle_context, cl_search
from agents.lawclaw.commands._memory import show_prior, remember


def authority_score(case):
    """Rank cases by court authority. SCOTUS > Circuit > District."""
    court = (case.get("court_citation_string") or case.get("court") or "").lower()
    if "supreme" in court or "scotus" in court:
        return 100
    elif "cir." in court:
        return 30
    return 0


def run(args):
    if not args:
        return (
            "[LAW] Usage: /law [topic or question]\n"
            "  /law qualified immunity\n"
            "  /law fourth amendment search and seizure\n"
            "  /law breach of contract elements Texas"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"LAW: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        # STEP 1: Chronicle
        out.append("")
        out.append("[1/3] Searching Chronicle...")
        chronicle_ctx = chronicle_context(f"{args} legal doctrine elements", limit=10)
        if chronicle_ctx:
            out.append("  Chronicle references found")

        # STEP 2: CourtListener case law — exact phrase, ranked by authority
        out.append("[2/3] Searching CourtListener opinions...")
        cl_context = ""
        cl_urls = []
        case_names = []

        results = cl_search(
            f'"{args}"',  # exact phrase match kills false positives
            search_type="o",
            courts="scotus,ca1,ca2,ca3,ca4,ca5,ca6,ca7,ca8,ca9,ca10,ca11,cadc,cafc",
            order_by="score desc",
            limit=15,
        )

        if results:
            # Rank by authority: SCOTUS first, then circuits
            results.sort(key=authority_score, reverse=True)

            out.append(f"  {len(results)} cases found")
            for o in results[:8]:
                case_name = o.get("caseName", "Unknown")
                date = o.get("dateFiled", "?") or "?"
                absolute_url = o.get("absolute_url", "")
                cl_url = f"https://www.courtlistener.com{absolute_url}" if absolute_url else ""
                citation = o.get("citation", "") or ""
                court = o.get("court_citation_string", "") or ""

                scotus_flag = " [SCOTUS]" if authority_score(o) == 100 else ""
                out.append(f"    [{date}] {case_name}{scotus_flag}")
                if court:
                    out.append(f"      Court: {court}")
                if citation:
                    out.append(f"      Cite: {citation}")
                if cl_url:
                    out.append(f"      URL: {cl_url}")
                    cl_urls.append(cl_url)
                case_names.append(case_name)
                out.append("")

            cl_context = "\n".join(
                f"{name} | {url}" for name, url in zip(case_names, cl_urls)
            )
        else:
            out.append("  No CourtListener cases found")

        # STEP 3: Grounded LLM synthesis
        out.append("[3/3] Synthesizing overview...")

        cases_text = "\n".join(
            f"- {name} ({url})" for name, url in zip(case_names, cl_urls)
        ) if case_names else "No cases retrieved."

        prompt = f"""Topic: {args}

Use ONLY these authorities:
{cases_text}

CHRONICLE REFERENCES:
{chronicle_ctx[:1500] if chronicle_ctx else "None."}

Produce:
1. DEFINITION — Plain English, 2-3 sentences
2. GOVERNING TEST — What must be shown
3. LEADING SCOTUS AUTHORITY — Cite by name from the list above
4. CIRCUIT SPLIT — If evident from the cases above, cite by name
5. PRACTICE IMPLICATIONS — What a litigant should know

Cite cases by name from the list above. Do not say 'no specific cases provided.'
If data is limited, state what is missing rather than fabricating.

Overview:"""

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
            if chronicle_ctx:
                out.append("")
                out.append("[CHRONICLE REFERENCES]")
                out.append(chronicle_ctx[:1500])
        out.append("=" * 60)

        # Write to shared memory
        if cl_urls or chronicle_ctx:
            remember(
                command="/law",
                query=args,
                result_summary=result if result else f"Found {len(cl_urls)} cases",
                source_type="web_verified" if cl_urls else "chronicle",
                confidence=0.85 if cl_urls else 0.80,
                urls=cl_urls,
            )

        if cl_urls:
            out.append("")
            out.append("  Cases (use /docket [URL] for full entries):")
            for url in list(dict.fromkeys(cl_urls))[:8]:
                out.append(f"    {url}")

        out.append("")
        out.append("  Search CourtListener: https://www.courtlistener.com/?q=" + args.replace(" ", "+") + "&type=o")

        return "\n".join(out)

    except Exception as e:
        log("law_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)