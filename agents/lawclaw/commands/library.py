"""library command - Library lookup via jurisdiction files + Chronicle + LLM"""
import re
from pathlib import Path

name = "/library"

from agents.lawclaw.commands._helpers import (
    log, llm, webclaw, chronicle_context, jurisdiction_root
)

STATE_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY","DC","PR","GU","MP"
}
SKIP_FOLDERS = {"docu_resources", "draw_resources", "medi_resources", "state"}

LEGAL_HINTS = [
    "law", "legal", "ordinance", "code", "municipal", "court",
    "forms", "statute", "zoning", "permit", "tenant",
    "housing", "landlord", "clerk", "filing", "rules", "procedures"
]


def normalize(s):
    if not s: return ""
    return s.lower().replace(" ", "_").replace("-", "_").replace(".", "").replace(",", "").strip("_")


def run(args):
    if not args:
        return "[LIBRARY] Usage: /library [city] [state]\n  /library Daytona Beach FL\n  /library Bedford VA"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"LIBRARY: {args}")
    out.append("=" * 60)

    try:
        parts = args.strip().split()
        state = None
        city_parts = []
        for p in parts:
            if p.upper() in STATE_CODES:
                state = p.upper()
            else:
                city_parts.append(p)
        city = " ".join(city_parts)
        city_norm = normalize(city)

        juris_root = jurisdiction_root()
        all_content = []
        library_urls = []
        found = False

        for state_dir in sorted(juris_root.iterdir()):
            if not state_dir.is_dir(): continue
            if state and state_dir.name.upper() != state: continue
            for county_dir in sorted(state_dir.iterdir()):
                if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS: continue
                for city_dir in sorted(county_dir.iterdir()):
                    if not city_dir.is_dir() or city_dir.name in SKIP_FOLDERS: continue
                    if city_norm not in normalize(city_dir.name).rstrip("_0123456789"): continue

                    for md_file in sorted(city_dir.iterdir()):
                        if md_file.suffix != ".md": continue
                        content = md_file.read_text(encoding="utf-8", errors="ignore")
                        if "library" in content.lower():
                            label = f"{city_dir.name.replace('_',' ').title()}, {county_dir.name.replace('_',' ').title()}, {state_dir.name.upper()}"
                            all_content.append(f"### {label} — {md_file.name}\n{content}")
                            library_urls.extend(re.findall(r'https?://[^\s\)\]\<\>\"\']+', content))
                            found = True
                    if found: break
                if found: break
            if found: break

        if not found:
            out.append(f"  No library data found for {args}.")
            out.append(f"  Try: /jurisdiction {args} for full civic profile")
            return "\n".join(out)

        # Discover legal resources from library URLs
        out.append("  Discovering legal resources via library website...")
        discovered = []
        for lib_url in [u for u in library_urls if "library" in u.lower()][:1]:
            try:
                page = webclaw(lib_url)
                if page and len(page) > 100:
                    links = re.findall(r'https?://[^\s\)\]\<\>\"\']+', page)
                    for link in links[:10]:
                        if any(h in link.lower() for h in LEGAL_HINTS):
                            discovered.append(link)
            except:
                pass

        chronicle_ctx = chronicle_context(f"{args} library public", limit=5)

        combined = "\n\n".join(block[:1500] for block in all_content[:3])
        if discovered:
            combined += "\n\n[DISCOVERED LEGAL RESOURCES]\n" + "\n".join(discovered[:8])

        prompt = f"""Extract library information for: {args}

DATA:
{combined}

CHRONICLE:
{chronicle_ctx[:1000] if chronicle_ctx else "None."}

List: library name, address, phone, hours, website.
Include any discovered legal resources (municipal code, court forms, etc).
Use ONLY the data provided. Under 200 words."""

        result = llm(prompt, timeout=90)
        out.append("")
        out.append("=" * 60)
        if result and len(result) > 20:
            out.append(result)
        else:
            out.append(combined[:2000])
        out.append("=" * 60)

        return "\n".join(out)

    except Exception as e:
        log("library_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)