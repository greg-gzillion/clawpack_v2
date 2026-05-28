"""statute command - Statute lookup via law.cornell.edu + Chronicle + LLM"""
import re
from pathlib import Path

name = "/statute"

from agents.lawclaw.commands._helpers import (
    log, llm, webclaw, chronicle, chronicle_context, jurisdiction_root
)
from agents.lawclaw.commands._memory import show_prior, remember

MAX_INPUT_LENGTH = 300  # prevent ReDoS on pathological input

# URL patterns for common statute sources
STATUTE_URLS = {
    "uscode": "https://www.law.cornell.edu/uscode/text/{title}/{section}",
    "ucc": "https://www.law.cornell.edu/ucc/{article}/{section}",
    "frcp": "https://www.law.cornell.edu/rules/frcp/rule_{rule}",
    "fre": "https://www.law.cornell.edu/rules/fre/rule_{rule}",
    "frap": "https://www.law.cornell.edu/rules/frap/rule_{rule}",
}


def parse_citation(args):
    """Parse statute citation into components. Returns dict or None."""
    args = args.strip()[:MAX_INPUT_LENGTH]

    ucc_match = re.match(r'ucc\s+(\d+)[-.](\d+[a-z]*)', args, re.IGNORECASE)
    if ucc_match:
        return {
            "type": "ucc",
            "article": ucc_match.group(1),
            "section": ucc_match.group(2),
            "url": STATUTE_URLS["ucc"].format(article=ucc_match.group(1), section=ucc_match.group(2)),
        }

    rules_match = re.match(r'(frcp|fre|frap)\s+(\d+)', args, re.IGNORECASE)
    if rules_match:
        rule_type = rules_match.group(1).lower()
        rule_num = rules_match.group(2)
        return {
            "type": rule_type,
            "rule": rule_num,
            "url": STATUTE_URLS[rule_type].format(rule=rule_num),
        }

    usc_match = re.match(r'(\d+)\s*(?:u\.?s\.?c\.?|usc)\s*(\d+[a-z]*)', args, re.IGNORECASE)
    if usc_match:
        title = usc_match.group(1)
        section = usc_match.group(2)
        return {
            "type": "uscode",
            "title": title,
            "section": section,
            "url": STATUTE_URLS["uscode"].format(title=title, section=section),
        }

    state_match = re.match(r'([a-z]{2}|[a-z]+)\s+([\d.]+[a-z]*)', args, re.IGNORECASE)
    if state_match:
        state = state_match.group(1)
        section = state_match.group(2)
        state_lower = state.lower()
        url = f"https://www.law.cornell.edu/statutes/{state_lower}#{section}"
        return {
            "type": "state",
            "state": state,
            "section": section,
            "url": url,
        }

    return None


def run(args):
    if not args:
        return (
            "[STATUTE] Usage: /statute [citation]\n"
            "  /statute 42 USC 1983       — federal statute\n"
            "  /statute UCC 2-207          — Uniform Commercial Code\n"
            "  /statute FRCP 12            — Federal Rules of Civil Procedure\n"
            "  /statute Florida 784.011    — state statute"
        )

    # Truncate input to prevent ReDoS
    args = args[:MAX_INPUT_LENGTH]

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"STATUTE: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        citation = parse_citation(args)

        # STEP 1: Chronicle
        out.append("")
        out.append("[1/3] Searching Chronicle...")
        chronicle_ctx = chronicle_context(f"{args} statute uscode law", limit=8)
        if chronicle_ctx:
            out.append("  Chronicle references found")

        # STEP 2: Fetch from law.cornell.edu
        out.append("[2/3] Fetching statute text...")
        statute_text = ""

        if citation and citation.get("url"):
            out.append(f"  Fetching: {citation['url']}")
            html = webclaw(citation["url"])
            if html and len(html) > 100:
                statute_text = html
                out.append(f"  Retrieved ({len(html)} chars)")
            else:
                out.append("  WebClaw could not fetch statute text")
        else:
            search_url = f"https://www.law.cornell.edu/search/site/{args.replace(' ', '%20')}"
            out.append(f"  No direct URL pattern matched. Search: {search_url}")
            html = webclaw(search_url)
            if html and len(html) > 100:
                statute_text = html
                out.append(f"  Search results retrieved ({len(html)} chars)")

        # STEP 3: LLM synthesis
        out.append("[3/3] Analyzing statute...")

        result = ""
        if statute_text or chronicle_ctx:
            prompt = f"""Analyze this statute: {args}

STATUTE TEXT (from law.cornell.edu):
{statute_text[:4000] if statute_text else "Not available."}

CHRONICLE REFERENCES:
{chronicle_ctx[:2000] if chronicle_ctx else "None."}

Provide:
CITATION — Full official citation
TEXT — Key provisions and operative language
ELEMENTS — What must be proven or shown (if applicable)
CONTEXT — What this statute does, why it matters
RELATED — Key related statutes or cases mentioned in the data

Use ONLY the data provided. Quote the statute text where available.
If the full text was not retrieved, summarize what is known from Chronicle.
Do not invent statutory language. Under 300 words.

Analysis:"""

            result = llm(prompt, timeout=120)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)
            else:
                out.append("")
                out.append("  (LLM unavailable)")
                if statute_text:
                    out.append("")
                    out.append("[RAW STATUTE TEXT]")
                    out.append(statute_text[:3000])
        else:
            out.append("  No data found for this statute.")
            out.append(f"  Try: https://www.law.cornell.edu/search/site/{args.replace(' ', '%20')}")

        if result:
            remember(command="/statute", query=args[:200], result_summary=result[:400], source_type="web_verified", confidence=0.85)

        out.append("")
        out.append("  Resources (Ctrl+Click):")
        if citation and citation.get("url"):
            out.append(f"    Full text: {citation['url']}")
        out.append("    US Code: https://www.law.cornell.edu/uscode/text")
        out.append("    UCC: https://www.law.cornell.edu/ucc")
        out.append("    Search: https://www.law.cornell.edu/search/site/" + args.replace(" ", "%20"))

        return "\n".join(out)

    except Exception as e:
        log("statute_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)