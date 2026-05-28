"""jurisdiction command - Civic intelligence via jurisdiction files + Chronicle + LLM"""
import requests
import re
from pathlib import Path

name = "/jurisdiction"
A2A = "http://127.0.0.1:8766"

LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
JURISDICTIONS_ROOT = LAW_REFS / "jurisdictions" / "us"

SKIP_FOLDERS = {"docu_resources", "draw_resources", "medi_resources", "state"}

STATE_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY","DC","PR","GU","MP"
}

LEGAL_HINTS = [
    "law", "legal", "ordinance", "code", "municipal", "court",
    "forms", "statute", "library", "zoning", "permit", "tenant",
    "housing", "landlord", "clerk", "filing", "rules", "procedures"
]


def _log(agent, event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent, event=event, detail=str(detail)[:500])
    except Exception:
        pass


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
        _log("lawclaw", "jurisdiction_llm_error", str(e)[:100])
    return ""


def webclaw(url, timeout=20):
    try:
        resp = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"fetch {url}", "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result and len(result) > 50:
                return result
    except Exception as e:
        _log("lawclaw", "jurisdiction_webclaw_error", str(e)[:100])
    return ""


def chronicle_search(query, limit=10):
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        return results if results else []
    except Exception as e:
        _log("lawclaw", "jurisdiction_chronicle_error", str(e)[:100])
    return []


def normalize(s):
    if not s:
        return ""
    return s.lower().replace(" ", "_").replace("-", "_").replace(".", "").replace(",", "").strip("_")


def is_legal_resource(url):
    u = url.lower()
    return any(h in u for h in LEGAL_HINTS)


def classify_resource(url):
    u = url.lower()
    if "code" in u or "ordinance" in u:
        return "Municipal Code"
    if "form" in u:
        return "Court Forms"
    if "zoning" in u:
        return "Zoning"
    if "tenant" in u or "housing" in u or "landlord" in u:
        return "Tenant/Housing"
    if "legal" in u and "aid" in u:
        return "Legal Aid"
    if "library" in u:
        return "Library"
    if "clerk" in u or "filing" in u:
        return "Court Filings"
    if "rule" in u or "procedure" in u:
        return "Court Rules"
    return "Legal Resource"


def parse_query(args):
    """Parse 'Daytona Beach FL', 'Bedford VA', 'Volusia County FL', 'Chicago IL'"""
    parts = args.strip().split()
    state = None
    county = None
    city_parts = []

    remaining = []
    for p in parts:
        if p.upper() in STATE_CODES:
            state = p.upper()
        else:
            remaining.append(p)

    county_idx = None
    for i, p in enumerate(remaining):
        if p.lower() == "county":
            county_idx = i
            break

    if county_idx is not None:
        county = " ".join(remaining[:county_idx])
        city_parts = remaining[county_idx + 1:]
    else:
        city_parts = remaining

    city = " ".join(city_parts) if city_parts else None

    return {"city": city, "county": county, "state": state}


def find_folders(query):
    """Walk us/{state}/{county}/{city}/ and return matches by specificity."""
    if not JURISDICTIONS_ROOT.exists():
        return []

    city = query.get("city")
    county = query.get("county")
    state = query.get("state")

    city_norm = normalize(city) if city else None
    county_norm = normalize(county) if county else None

    matches = []

    for state_dir in sorted(JURISDICTIONS_ROOT.iterdir()):
        if not state_dir.is_dir():
            continue
        if state and state_dir.name.upper() != state:
            continue

        for county_dir in sorted(state_dir.iterdir()):
            if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS:
                continue

            cname = normalize(county_dir.name)
            county_match = (not county_norm or county_norm in cname or cname in county_norm)

            if not county_match:
                continue

            county_md = [f for f in county_dir.iterdir() if f.suffix == ".md"]
            if county_md:
                label = f"{county_dir.name.replace('_',' ').title()} County Courts, {state_dir.name.upper()}"
                matches.append(("county", county_dir, label, 1))

            for city_dir in sorted(county_dir.iterdir()):
                if not city_dir.is_dir() or city_dir.name in SKIP_FOLDERS:
                    continue

                if city_norm:
                    ciname = normalize(city_dir.name).rstrip("_0123456789")
                    if city_norm not in ciname and ciname not in city_norm:
                        continue

                md_files = [f for f in city_dir.iterdir() if f.suffix == ".md"]
                if md_files:
                    label = f"{city_dir.name.replace('_',' ').title()}, {county_dir.name.replace('_',' ').title()}, {state_dir.name.upper()}"
                    priority = 3 if city_norm else 2
                    matches.append(("city", city_dir, label, priority))

    matches.sort(key=lambda x: -x[3])
    seen = set()
    unique = []
    for m in matches:
        if m[1] not in seen:
            seen.add(m[1])
            unique.append(m)

    return unique


def run(args):
    if not args:
        return (
            "[JURISDICTION] Usage: /jurisdiction [city] [state] | [county] [state]\n"
            "  /jurisdiction Daytona Beach FL\n"
            "  /jurisdiction Bedford VA\n"
            "  /jurisdiction Volusia County FL"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"JURISDICTION: {args}")
    out.append("=" * 60)

    try:
        query = parse_query(args)

        # STEP 1: Chronicle
        out.append("")
        out.append("[1/4] Chronicle search...")
        search = " ".join(filter(None, [
            query.get("city") or "",
            query.get("county") or "",
            query.get("state") or "",
            "court police hospital jail municipal"
        ]))
        chronicle_results = chronicle_search(search, limit=8)
        chronicle_context = ""
        if chronicle_results:
            parts = []
            for r in chronicle_results[:5]:
                ctx = r["context"] if isinstance(r, dict) else str(r)
                url = r.get("url", "") if isinstance(r, dict) else ""
                parts.append(f"SOURCE: {url}\n{ctx[:1000]}")
            chronicle_context = "\n---\n".join(parts)
            out.append(f"  {len(chronicle_results)} Chronicle references")

        # STEP 2: Filesystem
        out.append("[2/4] Searching jurisdiction files...")
        folders = find_folders(query)

        if not folders:
            out.append("  No jurisdiction files found.")
            out.append(f"  Check: /jurisdiction [city] [2-letter state]")
            return "\n".join(out)

        all_content = []
        all_urls = []
        folder_labels = []

        for folder_type, folder_path, label, priority in folders:
            files_read = []
            for md_file in sorted(folder_path.iterdir()):
                if md_file.suffix != ".md":
                    continue
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore").strip()
                    if content:
                        files_read.append((md_file.name, content))
                        all_urls.extend(re.findall(r'https?://[^\s\)\]\<\>\"\']+', content))
                except Exception as e:
                    _log("lawclaw", "jurisdiction_read_error", str(e)[:100])

            if files_read:
                folder_labels.append(label)
                for fname, content in files_read:
                    all_content.append(f"### {label} — {fname}\n{content}")

        out.append(f"  {len(folder_labels)} folder(s): {', '.join(folder_labels[:5])}")
        out.append(f"  {len(all_content)} file(s), {len(set(all_urls))} unique URLs")

        # STEP 3: Live resource discovery via library URLs
        out.append("[3/4] Discovering legal resources via libraries...")
        library_urls = [u for u in all_urls if "library" in u.lower()][:2]
        discovered = []

        if library_urls:
            for lib_url in library_urls:
                try:
                    page = webclaw(lib_url)
                    if page and len(page) > 100:
                        links = re.findall(r'https?://[^\s\)\]\<\>\"\']+', page)
                        legal_links = [l for l in links if is_legal_resource(l)]
                        for link in legal_links[:10]:
                            category = classify_resource(link)
                            discovered.append((category, link))
                except:
                    pass

            if discovered:
                seen = set()
                unique_discovered = []
                for cat, url in discovered:
                    if url not in seen:
                        seen.add(url)
                        unique_discovered.append((cat, url))

                out.append(f"  Found {len(unique_discovered)} resources via libraries")
                for cat, url in unique_discovered[:15]:
                    all_urls.append(url)
                    all_content.append(f"[DISCOVERED] {cat}: {url}")
            else:
                out.append("  No additional legal resources discovered")
        else:
            out.append("  No library URLs found in jurisdiction files")

        # STEP 4: LLM synthesis
        out.append("[4/4] Building civic profile...")

        combined = ""
        for block in all_content:
            if len(combined) + len(block) > 6000:
                break
            combined += block + "\n\n"

        prompt = f"""Create a structured civic profile for: {args}

JURISDICTION DATA:
{combined[:6000]}

CHRONICLE:
{chronicle_context[:1500] if chronicle_context else "None."}

Rules:
- Use ONLY the data provided. No invented addresses, phones, or URLs.
- If an address is not explicitly in the source data, omit it entirely.
  Do not guess or note that you are guessing.
- Skip any section with no data. Each fact must appear only once.
- If a URL looks incorrect or generic, omit it.
- Include DISCOVERED resources in the relevant sections.

Sections (omit if no data):

COURTS — each court: name, address, phone, website
POLICE — department, non-emergency phone, address, website. Emergency: 911
JAIL — facility name, address, phone, website
HOSPITALS — each: name, address, phone, coordinates, website
LIBRARY — name, address, phone, hours, website
BUILDING PERMITS — office, address, phone, website
CITY HALL — address, phone, hours, website
LEGAL RESOURCES — municipal code, court forms, legal aid, tenant rights
URLs — all links"""

        result = llm(prompt, timeout=120)

        out.append("")
        out.append("=" * 60)
        if result and len(result) > 50:
            out.append(result)
        else:
            out.append("[LLM unavailable — showing raw data]")
            out.append("")
            for block in all_content[:4]:
                out.append(block)
                out.append("")
        out.append("=" * 60)

        # URLs
        unique_urls = list(dict.fromkeys(all_urls))
        if unique_urls:
            gov_urls = [u for u in unique_urls if ".gov" in u.lower()]
            other_urls = [u for u in unique_urls if ".gov" not in u.lower()]
            ranked = gov_urls + other_urls
            out.append("")
            out.append("  URLs (Ctrl+Click):")
            for url in ranked[:20]:
                out.append(f"    {url}")

        return "\n".join(out)

    except Exception as e:
        _log("lawclaw", "jurisdiction_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)