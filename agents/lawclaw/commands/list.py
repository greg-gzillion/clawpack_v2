"""list command - Browse and navigate the jurisdiction database"""
from pathlib import Path

name = "/list"

LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
JURISDICTIONS_ROOT = LAW_REFS / "jurisdictions" / "us"

SKIP_FOLDERS = {"docu_resources", "draw_resources", "medi_resources", "law_resources"}

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


def _log(event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent="lawclaw", event=event, detail=str(detail)[:500])
    except Exception:
        pass


def count_cities(state_dir):
    count = 0
    try:
        for county_dir in state_dir.iterdir():
            if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS:
                continue
            for city_dir in county_dir.iterdir():
                if city_dir.is_dir() and city_dir.name not in SKIP_FOLDERS:
                    count += 1
    except Exception as e:
        _log("list_count_error", str(e)[:100])
    return count


def list_counties(state_dir):
    counties = []
    try:
        for county_dir in sorted(state_dir.iterdir()):
            if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS:
                continue
            cities = [d for d in county_dir.iterdir() if d.is_dir() and d.name not in SKIP_FOLDERS]
            counties.append((county_dir.name.replace("_", " ").title(), len(cities)))
    except Exception as e:
        _log("list_counties_error", str(e)[:100])
    return counties


def list_cities(state_dir, county_filter=None):
    cities = []
    try:
        for county_dir in sorted(state_dir.iterdir()):
            if not county_dir.is_dir() or county_dir.name in SKIP_FOLDERS:
                continue
            if county_filter and county_filter.lower() not in county_dir.name.lower():
                continue
            county_name = county_dir.name.replace("_", " ").title()
            for city_dir in sorted(county_dir.iterdir()):
                if not city_dir.is_dir() or city_dir.name in SKIP_FOLDERS:
                    continue
                files = [f for f in city_dir.iterdir() if f.suffix == ".md"]
                city_name = city_dir.name.replace("_", " ").title()
                cities.append((county_name, city_name, len(files)))
    except Exception as e:
        _log("list_cities_error", str(e)[:100])
    return cities


def run(args):
    out = []
    out.append("")
    out.append("=" * 60)

    # Memory recall
    try:
        from agents.lawclaw.commands._memory import show_prior, remember
        prior = show_prior(args or "", out)
    except Exception:
        pass

    try:
        if not JURISDICTIONS_ROOT.exists():
            out.append("JURISDICTION DATABASE")
            out.append("=" * 60)
            out.append(f"  Database not found at: {JURISDICTIONS_ROOT}")
            return "\n".join(out)

        args_lower = args.lower().strip() if args else ""

        # /list (no args) or /list states — show all
        if not args_lower or args_lower in ("states", ""):
            out.append("JURISDICTION DATABASE — All States")
            out.append("=" * 60)

            state_dirs = sorted(
                [d for d in JURISDICTIONS_ROOT.iterdir()
                 if d.is_dir() and d.name not in SKIP_FOLDERS and d.name not in ("federal", "territorial", "tribal")],
                key=lambda d: d.name
            )

            total_cities = 0
            rows = []
            for state_dir in state_dirs:
                code = state_dir.name.upper()
                full_name = STATE_NAMES.get(state_dir.name.lower(), code)
                city_count = count_cities(state_dir)
                total_cities += city_count
                rows.append((code, full_name, city_count))

            out.append(f"  {len(rows)} states | {total_cities:,} cities indexed")
            out.append("")
            for code, full_name, city_count in rows:
                out.append(f"  {code:<4}  {full_name:<30}  {city_count:>4} cities")
            out.append("")
            out.append("  Commands:")
            out.append("    /list FL              -- counties in Florida")
            out.append("    /list FL Volusia      -- cities in Volusia County, FL")
            out.append("    /list FL all          -- all cities in Florida")
            out.append("    /jurisdiction [city] [state]  -- full civic profile")

            # Write to shared memory
            try:
                remember(
                    command="/list",
                    query="all states",
                    result_summary=f"{len(rows)} states, {total_cities:,} cities indexed",
                    source_type="chronicle",
                    confidence=0.95,
                )
            except Exception:
                pass

            return "\n".join(out)

        # Parse args: first word = state code, rest = county or "all"
        parts = args_lower.split()
        state_code = parts[0].lower()

        # Find state directory
        state_dir = None
        for d in JURISDICTIONS_ROOT.iterdir():
            if d.is_dir() and d.name.lower() == state_code:
                state_dir = d
                break

        if not state_dir:
            out.append(f"JURISDICTION DATABASE — '{args}'")
            out.append("=" * 60)
            out.append(f"  State '{state_code.upper()}' not found in database.")
            out.append("  Run /list to see all available states.")
            return "\n".join(out)

        state_full = STATE_NAMES.get(state_code, state_code.upper())

        # /list FL all — every city
        if len(parts) >= 2 and parts[1] in ("all", "cities"):
            out.append(f"JURISDICTION DATABASE — {state_full}: All Cities")
            out.append("=" * 60)
            cities = list_cities(state_dir)
            out.append(f"  {len(cities)} cities in {state_full}")
            out.append("")
            current_county = None
            for county_name, city_name, file_count in cities:
                if county_name != current_county:
                    out.append(f"  {county_name} County:")
                    current_county = county_name
                files_note = f" ({file_count} files)" if file_count else ""
                out.append(f"    {city_name}{files_note}")
            out.append("")
            out.append(f"  Use: /jurisdiction [city] {state_code.upper()}")
            return "\n".join(out)

        # /list FL Volusia — cities in county
        if len(parts) >= 2:
            county_filter = " ".join(parts[1:])
            out.append(f"JURISDICTION DATABASE — {state_full}: {county_filter.title()}")
            out.append("=" * 60)
            cities = list_cities(state_dir, county_filter=county_filter)
            if cities:
                out.append(f"  {len(cities)} cities matching '{county_filter}'")
                out.append("")
                for county_name, city_name, file_count in cities:
                    files_note = f" ({file_count} files)" if file_count else ""
                    out.append(f"    {city_name}{files_note}")
                out.append("")
                out.append(f"  Use: /jurisdiction [city] {state_code.upper()}")
            else:
                out.append(f"  No cities found matching '{county_filter}'")
                out.append(f"  Try: /list {state_code.upper()} — see all counties")
            return "\n".join(out)

        # /list FL — counties only
        out.append(f"JURISDICTION DATABASE — {state_full}: Counties")
        out.append("=" * 60)
        counties = list_counties(state_dir)
        total = sum(c for _, c in counties)
        out.append(f"  {len(counties)} counties | {total} cities indexed")
        out.append("")
        for county_name, city_count in counties:
            out.append(f"  {county_name:<30}  {city_count:>3} cities")
        out.append("")
        out.append("  Commands:")
        out.append(f"    /list {state_code.upper()} [county]  -- cities in that county")
        out.append(f"    /list {state_code.upper()} all       -- all cities in {state_full}")
        out.append(f"    /jurisdiction [city] {state_code.upper()}  -- full civic profile")

        # Write to shared memory
        try:
            remember(
                command="/list",
                query=args,
                result_summary=f"{state_full}: {len(counties)} counties, {total} cities",
                source_type="chronicle",
                confidence=0.95,
            )
        except Exception:
            pass

        return "\n".join(out)

    except Exception as e:
        _log("list_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)