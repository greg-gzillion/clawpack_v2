"""jurisdiction command - Civic intelligence via Chronicle FTS5 + Sovereign Gateway"""
import re
from pathlib import Path

name = "/jurisdiction"

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


def run(args, agent=None):
    if not args:
        return "Usage: /jurisdiction <city> <state>\nExample: /jurisdiction Denver CO"

    from agents.lawclaw.commands._memory import recall, remember, show_prior

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"JURISDICTION: {args}")
    out.append("=" * 60)

    # Check memory first
    prior = recall(f"jurisdiction {args}", limit=3)
    if prior:
        show_prior(f"jurisdiction {args}", out)

    try:
        # STEP 1: Chronicle search
        out.append("[1/4] Chronicle search...")
        chronicle_context = ""
        all_urls = []
        if agent and hasattr(agent, 'search_chronicle'):
            try:
                chronicle_results = agent.search_chronicle(args, limit=10)
                if chronicle_results:
                    lines = []
                    for c in chronicle_results:
                        ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                        url = c.get("url", "") if isinstance(c, dict) else ""
                        if ctx:
                            lines.append(ctx[:500])
                        if url and "https://" in url:
                            all_urls.append(url)
                    chronicle_context = "\n".join(lines)
                    out.append(f"  {len(chronicle_results)} Chronicle references")
            except Exception as e:
                out.append(f"  Chronicle: {str(e)[:50]}")

        # STEP 2: Search jurisdiction files
        out.append("[2/4] Searching jurisdiction files...")
        
        parts = args.strip().split()
        state_code = None
        city_query = args.strip()
        for part in parts:
            if part.upper() in STATE_CODES:
                state_code = part.upper()
                city_query = " ".join(p for p in parts if p.upper() != state_code)
                break

        all_content = []
        folder_count = 0
        file_count = 0

        if state_code:
            state_dir = JURISDICTIONS_ROOT / state_code
            if state_dir.exists():
                for folder in sorted(state_dir.iterdir()):
                    if not folder.is_dir() or folder.name in SKIP_FOLDERS:
                        continue
                    folder_count += 1
                    for md_file in folder.rglob("*.md"):
                        try:
                            content = md_file.read_text(encoding="utf-8", errors="ignore")
                            file_count += 1
                            if city_query.lower() in folder.name.lower() or city_query.lower() in content.lower()[:500]:
                                all_content.append(f"### {folder.name}/{md_file.name}\n{content[:2000]}")
                                # Extract URLs
                                for line in content.split("\n"):
                                    if "https://" in line:
                                        url = line[line.index("https://"):].split()[0].rstrip(")")
                                        if url not in all_urls:
                                            all_urls.append(url)
                        except Exception:
                            pass

        out.append(f"  {folder_count} folder(s), {file_count} file(s), {len(set(all_urls))} unique URLs")

        # STEP 3: Library discovery
        out.append("[3/4] Discovering legal resources via libraries...")
        if agent and hasattr(agent, 'lookup_jurisdiction'):
            try:
                lib_data = agent.lookup_jurisdiction(args, "library")
                if lib_data.get("libraries"):
                    out.append(f"  {len(lib_data['libraries'])} library resource(s) found")
                    for lib in lib_data["libraries"][:3]:
                        out.append(f"    {lib[:120]}")
            except Exception:
                out.append("  No additional legal resources discovered")
        else:
            out.append("  No library URLs found in jurisdiction files")

        # STEP 4: LLM synthesis via Sovereign Gateway
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
- Skip any section with no data. Each fact must appear only once.
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

        if agent and hasattr(agent, 'ask_llm'):
            result = agent.ask_llm(prompt)
        else:
            result = ""

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

        if result:
            remember(command="/jurisdiction", query=args, result_summary=result[:400], source_type="chronicle", confidence=0.95)
            try:
                from agents.lawclaw.commands._memory import remember_court
                court_data = {
                    "jurisdiction": args.strip(),
                    "summary": result[:500],
                }
                remember_court(args.strip(), court_data)
            except Exception:
                pass

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
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
