"""state command - State court lookup via jurisdiction files + Chronicle + LLM"""
import re
from pathlib import Path

name = "/state"

from agents.lawclaw.commands._helpers import (
    log, llm, chronicle, chronicle_context, jurisdiction_root
)
from agents.lawclaw.commands._memory import show_prior, remember
from shared.jurisdiction_validator import validate_state, sanitize_component, ALLOWED_STATES

STATE_NAMES = {
    "ak": "Alaska", "al": "Alabama", "ar": "Arkansas", "az": "Arizona",
    "ca": "California", "co": "Colorado", "ct": "Connecticut", "dc": "District of Columbia",
    "de": "Delaware", "fl": "Florida", "ga": "Georgia", "hi": "Hawaii",
    "ia": "Iowa", "id": "Idaho", "il": "Illinois", "in": "Indiana",
    "ks": "Kansas", "ky": "Kentucky", "la": "Louisiana", "ma": "Massachusetts",
    "md": "Maryland", "me": "Maine", "mi": "Michigan", "mn": "Minnesota",
    "mo": "Missouri", "ms": "Mississippi", "mt": "Montana", "nc": "North Carolina",
    "nd": "North Dakota", "ne": "Nebraska", "nh": "New Hampshire", "nj": "New Jersey",
    "nm": "New Mexico", "nv": "Nevada", "ny": "New York", "oh": "Ohio",
    "ok": "Oklahoma", "or": "Oregon", "pa": "Pennsylvania", "pr": "Puerto Rico",
    "ri": "Rhode Island", "sc": "South Carolina", "sd": "South Dakota",
    "tn": "Tennessee", "tx": "Texas", "ut": "Utah", "va": "Virginia",
    "vt": "Vermont", "wa": "Washington", "wi": "Wisconsin", "wv": "West Virginia",
    "wy": "Wyoming",
}

SKIP_FOLDERS = {"docu_resources", "draw_resources", "medi_resources", "state"}


def run(args):
    if not args:
        return (
            "[STATE] Usage: /state [state code] [county]\n"
            "  /state TX              — Texas state court system\n"
            "  /state TX Harris       — Harris County courts\n"
            "  /state VA Bedford      — Bedford County courts"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"STATE COURTS: {args}")
    out.append("=" * 60)

    prior = show_prior(args, out)

    try:
        parts = args.strip().split()
        raw_state = parts[0].lower()

        safe_state = validate_state(raw_state)
        if safe_state is None:
            out.append(f"  Invalid state code: '{parts[0]}'. Use 2-letter code like VA, TX, CA.")
            return "\n".join(out)

        raw_county = " ".join(parts[1:]) if len(parts) > 1 else ""
        safe_county = sanitize_component(raw_county, 80) if raw_county else ""

        state_full = STATE_NAMES.get(safe_state, safe_state.upper())
        juris_root = jurisdiction_root().resolve()

        # safe_state validated: validate_state() → ALLOWED_STATES frozenset membership,
        # sanitized via re.sub, resolved, and relative_to() containment checked.
        # lgtm [py/path-injection]
        state_dir = (juris_root / safe_state).resolve()
        if not state_dir.exists():
            # lgtm [py/path-injection]
            state_dir = (juris_root / safe_state.upper()).resolve()
        if not state_dir.exists():
            out.append(f"  State '{safe_state.upper()}' not found.")
            out.append("  Run /list to see all available states.")
            return "\n".join(out)

        try:
            state_dir.relative_to(juris_root)
        except ValueError:
            out.append("  Invalid path.")
            return "\n".join(out)

        if not safe_county:
            # safe_county empty — iterdir() on validated state_dir only.
            # lgtm [py/path-injection]
            counties = sorted([
                d.name.replace("_", " ").title()
                for d in state_dir.iterdir()
                if d.is_dir() and d.name not in SKIP_FOLDERS
            ])
            out.append(f"  {state_full}: {len(counties)} counties with court data")
            out.append("")
            for c in counties:
                out.append(f"    {c}")
            out.append("")
            out.append(f"  /state {safe_state.upper()} [county] — court details")
            out.append(f"  /jurisdiction [city] {safe_state.upper()} — civic profile")
            return "\n".join(out)

        out.append("")
        out.append("[1/3] Searching jurisdiction files...")

        all_content = []
        all_urls = []
        files_found = 0

        # safe_county sanitized via sanitize_component(), length-bounded to 80 chars.
        # lgtm [py/path-injection]
        for county_dir in sorted(state_dir.iterdir()):
            if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS:
                continue

            cname = county_dir.name.replace("_", " ").lower()
            if safe_county.lower() in cname:
                for f in sorted(county_dir.iterdir()):
                    if f.suffix == ".md":
                        try:
                            content = f.read_text(encoding="utf-8", errors="ignore").strip()
                            if content:
                                label = f"{county_dir.name.replace('_', ' ').title()} County — {f.name}"
                                all_content.append(f"### {label}\n{content}")
                                all_urls.extend(re.findall(r'https?://[^\s\)\]\<\>\"\']+', content))
                                files_found += 1
                        except:
                            pass

        out.append(f"  {files_found} court files found in {state_full}")

        if files_found == 0:
            close = []
            for d in sorted(state_dir.iterdir()):
                if d.is_dir() and safe_county[:4].lower() in d.name.lower():
                    close.append(d.name.replace("_", " ").title())
            if close:
                out.append(f"  Did you mean: {', '.join(close[:3])}?")
                return "\n".join(out)

        out.append("[2/3] Searching Chronicle...")
        chronicle_ctx = chronicle_context(f"{state_full} {safe_county} state court", limit=8)
        if chronicle_ctx:
            out.append("  Chronicle references found")

        out.append("[3/3] Generating state court profile...")

        result = ""
        if all_content:
            combined = "\n\n".join(block[:1500] for block in all_content[:10])

            prompt = f"""Create a state court profile for: {args}

JURISDICTION FILES:
{combined}

CHRONICLE:
{chronicle_ctx[:1500] if chronicle_ctx else "None."}

Cover: state court structure, types of courts, key courts found in the files,
how to access records, and relevant URLs.
Use ONLY the data provided. Do not invent courts or URLs.
Under 300 words.

Profile:"""

            result = llm(prompt, timeout=120)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)
            else:
                out.append("")
                out.append("[LLM unavailable — showing raw data]")
                out.append("")
                for block in all_content[:4]:
                    out.append(block[:1500])
                    out.append("")
        else:
            out.append("  No court files found for this county.")
            out.append(f"  Try: /jurisdiction [city] {safe_state.upper()}")

        if result:
            remember(command="/state", query=args, result_summary=result[:400], source_type="chronicle", confidence=0.90)

        unique_urls = list(dict.fromkeys(all_urls))
        if unique_urls:
            gov_urls = [u for u in unique_urls if ".gov" in u.lower()]
            other_urls = [u for u in unique_urls if ".gov" not in u.lower()]
            ranked = gov_urls + other_urls
            out.append("")
            out.append("  URLs (Ctrl+Click):")
            for url in ranked[:15]:
                out.append(f"    {url}")

        out.append("")
        out.append(f"  /jurisdiction [city] {safe_state.upper()} — full civic profile")
        out.append(f"  /list {safe_state.upper()} — all counties")

        return "\n".join(out)

    except Exception as e:
        log("state_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)