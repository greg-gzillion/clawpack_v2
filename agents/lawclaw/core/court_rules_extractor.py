# agents/lawclaw/core/court_rules_extractor.py
"""
Court Rules Extractor — fetches local court rules from live websites
and local jurisdiction files, then extracts structured filing requirements via LLM.

Constitutional: all web access through webclaw A2A, all LLM through Sovereign Gateway.

Data sources (in priority order):
  1. Local jurisdiction files (municipal_court.md, law_resources.md) — 3,800+ cities
  2. Chronicle cache — prior indexed court data
  3. Live court website fetch via webclaw

Usage:
    from agents.lawclaw.core.court_rules_extractor import extract_court_rules
    
    rules = extract_court_rules("Bedford VA")
    # Returns CourtRules dataclass with margins, font, filing deadlines, etc.
    # Data sourced from local files, Chronicle, and live court websites.
"""
import json
import re
from pathlib import Path
from typing import Optional

# Import the schema
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from shared.court_rules_schema import CourtRules, completeness_score

# ── Paths ────────────────────────────────────────────────────────────────────

JURISDICTIONS_ROOT = (
    Path(__file__).resolve().parent.parent.parent.parent /
    "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"
)


# ── Local File Reader ────────────────────────────────────────────────────────

def _read_local_jurisdiction_files(jurisdiction: str) -> str:
    """
    Read municipal_court.md and law_resources.md from the 3,800-city
    jurisdiction database. Returns combined content string or ''.
    """
    if not jurisdiction or len(jurisdiction.strip()) < 3:
        return ""

    parts = jurisdiction.strip().split()
    state = parts[-1].lower() if len(parts) >= 2 else ""
    city = parts[0].lower()

    if not state or len(state) != 2:
        return ""

    if not JURISDICTIONS_ROOT.exists():
        return ""

    # Search state directory
    for state_dir in JURISDICTIONS_ROOT.iterdir():
        if not state_dir.is_dir():
            continue
        if state_dir.name.lower() != state:
            continue

        # Search county directories within state
        for county_dir in state_dir.iterdir():
            if not county_dir.is_dir():
                continue

            # Search city directories within county
            for city_dir in county_dir.iterdir():
                if not city_dir.is_dir():
                    continue
                if city not in city_dir.name.lower():
                    continue

                # Found matching city — read local files
                content_parts = []
                for fname in ["municipal_court.md", "law_resources.md", "circuit_court.md",
                               "district_court.md", "general_district_court.md"]:
                    fpath = city_dir / fname
                    if fpath.exists():
                        try:
                            text = fpath.read_text(encoding="utf-8", errors="ignore").strip()
                            if text:
                                content_parts.append(f"### {fname}\n{text[:1500]}")
                        except Exception:
                            pass

                if content_parts:
                    return "\n\n".join(content_parts)

    return ""


def _search_all_cities_for_jurisdiction(jurisdiction: str) -> str:
    """
    Broader search across all 3,800+ cities for a jurisdiction name.
    Tries partial matches on city name, county name, and state.
    """
    parts = jurisdiction.strip().split()
    if len(parts) < 2:
        return ""

    search_terms = [p.lower() for p in parts if len(p) > 2]

    if not JURISDICTIONS_ROOT.exists():
        return ""

    matches = []
    for state_dir in JURISDICTIONS_ROOT.iterdir():
        if not state_dir.is_dir():
            continue
        for county_dir in state_dir.iterdir():
            if not county_dir.is_dir():
                continue
            for city_dir in county_dir.iterdir():
                if not city_dir.is_dir():
                    continue
                city_name = city_dir.name.lower().replace("_", " ")
                # Score match by how many search terms appear in city name
                score = sum(1 for t in search_terms if t in city_name)
                if score > 0:
                    matches.append((score, city_dir))

    if not matches:
        return ""

    # Return content from best match
    matches.sort(key=lambda x: -x[0])
    best = matches[0][1]
    content_parts = []
    for fname in ["municipal_court.md", "law_resources.md", "circuit_court.md"]:
        fpath = best / fname
        if fpath.exists():
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore").strip()
                if text:
                    content_parts.append(f"### {best.name} — {fname}\n{text[:1500]}")
            except Exception:
                pass

    return "\n\n".join(content_parts) if content_parts else ""


# ── Main Extractor ───────────────────────────────────────────────────────────

def extract_court_rules(jurisdiction: str) -> Optional[CourtRules]:
    """
    Extract structured court rules for a jurisdiction.

    Data sources (in priority order):
      1. Local jurisdiction files (municipal_court.md, law_resources.md)
      2. Chronicle cache
      3. Live court website fetch via webclaw
      4. LLM extraction of structured parameters

    Args:
        jurisdiction: e.g., "SDNY", "Bedford VA", "Hazlehurst MS"

    Returns:
        CourtRules dataclass or None if extraction fails
    """
    from agents.lawclaw.commands._helpers import webclaw, chronicle_context, llm, log

    # ── Source 1: Local jurisdiction files ──────────────────────────────
    log("court_rules_extract", f"Checking local files for {jurisdiction}")
    local_content = _read_local_jurisdiction_files(jurisdiction)

    # If exact match fails, try broader search
    if not local_content:
        local_content = _search_all_cities_for_jurisdiction(jurisdiction)

    # ── Source 2: Chronicle cache ───────────────────────────────────────
    chronicle_hits = chronicle_context(
        f"{jurisdiction} local civil rules filing requirements margins font",
        limit=5,
        max_chars=2000
    )

    # ── Source 3: Live court website ────────────────────────────────────
    search_urls = _build_search_urls(jurisdiction)
    page_content = ""
    for url in search_urls:
        log("court_rules_fetch", f"Fetching {url}")
        content = webclaw(url, timeout=15)
        if content and len(content) > 500:
            page_content = content[:8000]
            break

    # ── Combine all sources ─────────────────────────────────────────────
    if not local_content and not chronicle_hits and not page_content:
        log("court_rules_fail", f"No content found for {jurisdiction}")
        return None

    combined_context = f"""
LOCAL JURISDICTION FILES:
{local_content if local_content else "No local files found."}

CHRONICLE CACHE:
{chronicle_hits if chronicle_hits else "No cached data."}

LIVE COURT WEBSITE:
{page_content if page_content else "No live data fetched."}
"""

    # ── Source 4: LLM extraction ────────────────────────────────────────
    prompt = f"""Extract the local court filing rules from the provided content for: {jurisdiction}

Return a JSON object with these fields. Use null for any field not found in the content.

{{
  "court_name": "Full official court name",
  "jurisdiction": "e.g., US District Court, Southern District of New York",
  "filing_system": "e.g., CM/ECF, PACER, eFileIL",
  "official_url": "Court website URL",
  "case_style_format": "Caption format template",
  "margins": "Margin requirements",
  "font_family": "Required font",
  "font_size": "Required font size",
  "line_spacing": "Line spacing requirement",
  "page_size": "Page size",
  "page_numbering": "Page numbering rules",
  "max_file_size": "Maximum file size for e-filing",
  "accepted_formats": "Accepted file formats",
  "bookmark_required": true/false,
  "ocr_required": true/false,
  "text_searchable_required": true/false,
  "signature_requirements": "Signature block requirements",
  "briefing_schedule": "Response and reply deadlines",
  "response_deadline_days": number,
  "reply_deadline_days": number,
  "page_limits": "Page limits for motions",
  "portal": "E-filing portal name/URL",
  "emergency_filing_procedure": "Emergency filing instructions"
}}

CONTENT:
{combined_context[:6000]}

Return ONLY valid JSON. No commentary. If a field isn't found, use null.
JSON:"""

    try:
        result = llm(prompt, timeout=120)
        json_match = re.search(r'\{[\s\S]*\}', result)
        if json_match:
            data = json.loads(json_match.group(0))
            rules = CourtRules(
                court_name=data.get("court_name", "") or "",
                jurisdiction=data.get("jurisdiction", "") or "",
                filing_system=data.get("filing_system", "") or "",
                official_url=data.get("official_url", "") or "",
                case_style_format=data.get("case_style_format", "") or "",
                margins=data.get("margins", "") or "",
                font_family=data.get("font_family", "") or "",
                font_size=data.get("font_size", "") or "",
                line_spacing=data.get("line_spacing", "") or "",
                page_size=data.get("page_size", "") or "8.5 x 11 inches",
                page_numbering=data.get("page_numbering", "") or "",
                max_file_size=data.get("max_file_size", "") or "",
                accepted_formats=data.get("accepted_formats", "") or "PDF",
                bookmark_required=data.get("bookmark_required", False),
                ocr_required=data.get("ocr_required", False),
                text_searchable_required=data.get("text_searchable_required", True),
                signature_requirements=data.get("signature_requirements", "") or "",
                briefing_schedule=data.get("briefing_schedule", "") or "",
                response_deadline_days=data.get("response_deadline_days", 0),
                reply_deadline_days=data.get("reply_deadline_days", 0),
                page_limits=data.get("page_limits", "") or "",
                portal=data.get("portal", "") or "",
                emergency_filing_procedure=data.get("emergency_filing_procedure", "") or "",
            )
            score = completeness_score(rules)
            log("court_rules_done", f"{jurisdiction} score={score['percentage']}% grade={score['grade']}")
            return rules
    except Exception as e:
        log("court_rules_parse_error", str(e)[:200])

    return None


# ── URL Builder ──────────────────────────────────────────────────────────────

def _build_search_urls(jurisdiction: str) -> list:
    """Build likely URLs for a court's local rules page."""
    jl = jurisdiction.lower()
    urls = []

    # Federal district courts
    if "sdny" in jl or "southern district of new york" in jl:
        urls = [
            "https://www.nysd.uscourts.gov/rules",
            "https://www.nysd.uscourts.gov/local-rules",
        ]
    elif "edny" in jl or "eastern district of new york" in jl:
        urls = ["https://www.nyed.uscourts.gov/local-rules"]
    elif "nd cal" in jl or "northern district of california" in jl:
        urls = ["https://www.cand.uscourts.gov/local-rules"]
    elif "cd cal" in jl or "central district of california" in jl:
        urls = ["https://www.cacd.uscourts.gov/local-rules"]
    elif "ed tex" in jl or "eastern district of texas" in jl:
        urls = ["https://www.txed.uscourts.gov/local-rules"]
    elif "ddc" in jl or "district of columbia" in jl:
        urls = ["https://www.dcd.uscourts.gov/local-rules"]
    elif "nd ill" in jl or "northern district of illinois" in jl:
        urls = ["https://www.ilnd.uscourts.gov/local-rules"]
    elif "d mass" in jl or "district of massachusetts" in jl:
        urls = ["https://www.mad.uscourts.gov/local-rules"]
    elif "va" in jl or "virginia" in jl:
        urls = [
            "https://www.vacourts.gov/courts/circuit/home.html",
            "https://www.vacourts.gov",
        ]

    # Generic fallback
    if not urls:
        search_term = jurisdiction.replace(" ", "+")
        urls = [
            f"https://www.uscourts.gov/search/site/{search_term}%20local%20rules",
        ]

    return urls


# ── Prompt Context Builder ───────────────────────────────────────────────────

def rules_to_prompt_context(rules: CourtRules) -> str:
    """Convert CourtRules to a compact context string for docuclaw prompts."""
    if not rules or not rules.court_name:
        return ""

    parts = [
        f"Court: {rules.court_name}",
        f"Filing System: {rules.filing_system}",
    ]
    if rules.margins:
        parts.append(f"Margins: {rules.margins}")
    if rules.font_family:
        parts.append(f"Font: {rules.font_family}, {rules.font_size}")
    if rules.line_spacing:
        parts.append(f"Spacing: {rules.line_spacing}")
    if rules.page_limits:
        parts.append(f"Page Limits: {rules.page_limits}")
    if rules.signature_requirements:
        parts.append(f"Signature: {rules.signature_requirements}")
    if rules.briefing_schedule:
        parts.append(f"Deadlines: {rules.briefing_schedule}")
    if rules.portal:
        parts.append(f"E-File: {rules.portal}")

    return " | ".join(parts)


def jurisdiction_files_to_context(jurisdiction: str) -> str:
    """
    Read local jurisdiction files and return a formatted context string.
    Use this when you want raw file data rather than structured CourtRules.
    """
    content = _read_local_jurisdiction_files(jurisdiction)
    if not content:
        content = _search_all_cities_for_jurisdiction(jurisdiction)
    return content


__all__ = [
    "extract_court_rules",
    "rules_to_prompt_context",
    "jurisdiction_files_to_context",
    "CourtRules",
    "completeness_score",
]