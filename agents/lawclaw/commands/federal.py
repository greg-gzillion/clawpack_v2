"""federal command - Federal court intelligence hub"""
import requests
from pathlib import Path

name = "/federal"
A2A = "http://127.0.0.1:8766"

COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"

CIRCUITS = {
    "1": {"name": "1st Circuit", "states": ["ME", "MA", "NH", "RI", "PR"],
          "districts": ["med", "mad", "nhd", "rid", "prd"],
          "url": "https://www.ca1.uscourts.gov"},
    "2": {"name": "2nd Circuit", "states": ["CT", "NY", "VT"],
          "districts": ["ctd", "nyed", "nynd", "nysd", "nywd", "vtd"],
          "url": "https://www.ca2.uscourts.gov"},
    "3": {"name": "3rd Circuit", "states": ["DE", "NJ", "PA", "VI"],
          "districts": ["ded", "njd", "pae", "pam", "paw"],
          "url": "https://www.ca3.uscourts.gov"},
    "4": {"name": "4th Circuit", "states": ["MD", "NC", "SC", "VA", "WV"],
          "districts": ["mdd", "nce", "ncm", "ncw", "scd", "vae", "vaw", "wvn", "wvs"],
          "url": "https://www.ca4.uscourts.gov"},
    "5": {"name": "5th Circuit", "states": ["LA", "MS", "TX"],
          "districts": ["lae", "lam", "law", "msn", "mss", "txe", "txn", "txs", "txw"],
          "url": "https://www.ca5.uscourts.gov"},
    "6": {"name": "6th Circuit", "states": ["KY", "MI", "OH", "TN"],
          "districts": ["kye", "kyw", "mie", "miw", "ohn", "ohs", "tne", "tnm", "tnw"],
          "url": "https://www.ca6.uscourts.gov"},
    "7": {"name": "7th Circuit", "states": ["IL", "IN", "WI"],
          "districts": ["ilc", "iln", "ils", "inn", "ins", "wie", "wiw"],
          "url": "https://www.ca7.uscourts.gov"},
    "8": {"name": "8th Circuit", "states": ["AR", "IA", "MN", "MO", "NE", "ND", "SD"],
          "districts": ["ard", "arw", "ian", "ias", "mnd", "moe", "mow", "ned", "ndd", "sdd"],
          "url": "https://www.ca8.uscourts.gov"},
    "9": {"name": "9th Circuit", "states": ["AK", "AZ", "CA", "HI", "ID", "MT", "NV", "OR", "WA", "GU", "MP"],
          "districts": ["akd", "azd", "cac", "cae", "can", "cas", "hid", "idd", "mtd", "nvd", "ord", "wae", "waw"],
          "url": "https://www.ca9.uscourts.gov"},
    "10": {"name": "10th Circuit", "states": ["CO", "KS", "NM", "OK", "UT", "WY"],
           "districts": ["cod", "ksd", "nmd", "oke", "okn", "okw", "utd", "wyd"],
           "url": "https://www.ca10.uscourts.gov"},
    "11": {"name": "11th Circuit", "states": ["AL", "FL", "GA"],
           "districts": ["alm", "aln", "als", "flm", "fln", "fls", "gam", "gan", "gas"],
           "url": "https://www.ca11.uscourts.gov"},
    "dc": {"name": "D.C. Circuit", "states": ["DC"],
           "districts": ["dcd"],
           "url": "https://www.cadc.uscourts.gov"},
    "fc": {"name": "Federal Circuit", "states": ["National"],
           "districts": ["uscfc"],
           "url": "https://www.cafc.uscourts.gov"},
}

DISTRICT_NAMES = {
    "akd": "D. Alaska",
    "alm": "M.D. Ala.", "aln": "N.D. Ala.", "als": "S.D. Ala.",
    "ard": "E.D. Ark.", "arw": "W.D. Ark.",
    "azd": "D. Ariz.",
    "cac": "C.D. Cal.", "cae": "E.D. Cal.", "can": "N.D. Cal.", "cas": "S.D. Cal.",
    "cod": "D. Colo.",
    "ctd": "D. Conn.",
    "dcd": "D.D.C.",
    "ded": "D. Del.",
    "flm": "M.D. Fla.", "fln": "N.D. Fla.", "fls": "S.D. Fla.",
    "gam": "M.D. Ga.", "gan": "N.D. Ga.", "gas": "S.D. Ga.",
    "hid": "D. Haw.",
    "ian": "N.D. Iowa", "ias": "S.D. Iowa",
    "idd": "D. Idaho",
    "ilc": "C.D. Ill.", "iln": "N.D. Ill.", "ils": "S.D. Ill.",
    "inn": "N.D. Ind.", "ins": "S.D. Ind.",
    "ksd": "D. Kan.",
    "kye": "E.D. Ky.", "kyw": "W.D. Ky.",
    "lae": "E.D. La.", "lam": "M.D. La.", "law": "W.D. La.",
    "mad": "D. Mass.",
    "mdd": "D. Md.",
    "med": "D. Maine",
    "mie": "E.D. Mich.", "miw": "W.D. Mich.",
    "mnd": "D. Minn.",
    "moe": "E.D. Mo.", "mow": "W.D. Mo.",
    "msn": "N.D. Miss.", "mss": "S.D. Miss.",
    "mtd": "D. Mont.",
    "nce": "E.D.N.C.", "ncm": "M.D.N.C.", "ncw": "W.D.N.C.",
    "ndd": "D.N.D.",
    "ned": "D. Neb.",
    "nhd": "D.N.H.",
    "njd": "D.N.J.",
    "nmd": "D.N.M.",
    "nvd": "D. Nev.",
    "nyed": "E.D.N.Y.", "nynd": "N.D.N.Y.", "nysd": "S.D.N.Y.", "nywd": "W.D.N.Y.",
    "ohn": "N.D. Ohio", "ohs": "S.D. Ohio",
    "oke": "E.D. Okla.", "okn": "N.D. Okla.", "okw": "W.D. Okla.",
    "ord": "D. Ore.",
    "pae": "E.D. Pa.", "pam": "M.D. Pa.", "paw": "W.D. Pa.",
    "prd": "D.P.R.",
    "rid": "D.R.I.",
    "scd": "D.S.C.",
    "sdd": "D.S.D.",
    "tne": "E.D. Tenn.", "tnm": "M.D. Tenn.", "tnw": "W.D. Tenn.",
    "txe": "E.D. Tex.", "txn": "N.D. Tex.", "txs": "S.D. Tex.", "txw": "W.D. Tex.",
    "utd": "D. Utah",
    "vae": "E.D. Va.", "vaw": "W.D. Va.",
    "vtd": "D. Vt.",
    "wae": "E.D. Wash.", "waw": "W.D. Wash.",
    "wie": "E.D. Wis.", "wiw": "W.D. Wis.",
    "wvn": "N.D.W. Va.", "wvs": "S.D.W. Va.",
    "wyd": "D. Wyo.",
    "uscfc": "Fed. Cl.",
}

ABBREV_MAP = {
    "sdny": "nysd", "edny": "nyed", "ndny": "nynd", "wdny": "nywd",
    "cdca": "cac", "edca": "cae", "ndca": "can", "sdca": "cas",
    "edtx": "txe", "ndtx": "txn", "sdtx": "txs", "wdtx": "txw",
    "edpa": "pae", "mdpa": "pam", "wdpa": "paw",
    "edva": "vae", "wdva": "vaw",
    "ndga": "gan", "sdga": "gas", "mdga": "gam",
    "ndal": "aln", "sdal": "als", "mdal": "alm",
    "ndfl": "fln", "sdfl": "fls", "mdfl": "flm",
    "edla": "lae", "mdla": "lam", "wdla": "law",
    "ndms": "msn", "sdms": "mss",
    "edmi": "mie", "wdmi": "miw",
    "edmo": "moe", "wdmo": "mow",
    "ednc": "nce", "mdnc": "ncm", "wdnc": "ncw",
    "ndoh": "ohn", "sdoh": "ohs",
    "edok": "oke", "ndok": "okn", "wdok": "okw",
    "edtn": "tne", "mdtn": "tnm", "wdtn": "tnw",
    "edwa": "wae", "wdwa": "waw",
    "edwi": "wie", "wdwi": "wiw",
    "edky": "kye", "wdky": "kyw",
    "edar": "ard", "wdar": "arw",
    "ndia": "ian", "sdia": "ias",
    "ndil": "iln", "sdil": "ils", "cdil": "ilc",
    "ndin": "inn", "sdin": "ins",
    "ndwv": "wvn", "sdwv": "wvs",
    "ddc": "dcd",
}


def get_token():
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        for line in env_path.read_text().split("\n"):
            if "COURTLISTENER_TOKEN" in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except:
        pass
    return None


def resolve_district_code(args_lower):
    """Resolve user input to a district code, or None."""
    lookup = args_lower.replace(".", "").replace(" ", "")
    code = ABBREV_MAP.get(lookup, lookup)
    if code in DISTRICT_NAMES:
        return code
    # Check full name match
    for dc, dname in DISTRICT_NAMES.items():
        if dname.lower() == args_lower:
            return dc
    return None


def show_judges(code, output):
    """Fetch and display judges for a district or circuit court."""
    token = get_token()
    if not token:
        output.append("  (Add COURTLISTENER_TOKEN to .env for judge data)")
        return

    headers = {"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"}
    
    # Determine court IDs to query
    court_ids = [code]
    if code.startswith("ca"):
        # Circuit court — also get the circuit number for district judges
        circuit_num = code.replace("ca", "")
        if circuit_num in CIRCUITS:
            court_ids.extend(CIRCUITS[circuit_num]["districts"][:3])  # first 3 districts
    else:
        # District court — also get its circuit
        for cnum, cdata in CIRCUITS.items():
            if code in cdata["districts"]:
                court_ids.append(f"ca{cnum}")
                break

    all_judges = []
    for cid in court_ids:
        try:
            r = requests.get(
                f"{COURTLISTENER_API}/positions/",
                params={"court": cid, "page_size": 50},
                headers=headers, timeout=15
            )
            if r.status_code == 200:
                all_judges.extend(r.json().get("results", []))
        except:
            pass

    # Filter to judge positions only
    judge_positions = [p for p in all_judges if p.get("position_type") == "jud"]
    
    if not judge_positions:
        # Fallback: search Chronicle for judge reference files
        output.append("")
        output.append("  (No judge data from CourtListener API)")
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            court_name = DISTRICT_NAMES.get(code, code.upper())
            results = chronicle.recover_by_context(f"{court_name} judge federal district", limit=5)
            if results:
                output.append("  Chronicle references:")
                for r in results[:5]:
                    ctx = r["context"] if isinstance(r, dict) else str(r)
                    url = r["url"] if isinstance(r, dict) else ""
                    output.append(f"\n    SOURCE: {url}")
                    output.append(f"    {ctx[:800]}")
        except:
            pass
        return

    # Deduplicate by person ID
    seen = set()
    unique = []
    for j in judge_positions:
        person = j.get("person", {})
        pid = person.get("id") if isinstance(person, dict) else None
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(j)

    # Split active vs senior
    active = [j for j in unique if not j.get("date_termination")]
    senior = [j for j in unique if j.get("date_termination")]

    if active:
        output.append(f"\n  Active Judges ({len(active)}):")
        for j in active[:20]:
            person = j.get("person", {})
            if isinstance(person, dict):
                first = person.get("name_first", "")
                last = person.get("name_last", "")
                name = f"{first} {last}".strip()
            else:
                name = "Unknown"
            
            date_start = j.get("date_start", "?") or "?"
            # Appointer is a string URL like "/api/rest/v4/people/1862/"
            appointer = j.get("appointer", "")
            if appointer and isinstance(appointer, str):
                # Just note that appointer data exists, don't try to dereference
                output.append(f"    {name} (since {date_start})")
            else:
                output.append(f"    {name} (since {date_start})")

    if senior:
        output.append(f"\n  Senior Judges ({len(senior)}):")
        for j in senior[:15]:
            person = j.get("person", {})
            if isinstance(person, dict):
                first = person.get("name_first", "")
                last = person.get("name_last", "")
                name = f"{first} {last}".strip()
            else:
                name = "Unknown"
            
            date_term = j.get("date_termination", "?") or "?"
            output.append(f"    {name} (senior since {date_term})")


def show_opinions(court_id, output, limit=10):
    """Fetch and display recent opinions for a court."""
    token = get_token()
    if not token:
        output.append("  (Add COURTLISTENER_TOKEN to .env for live opinions)")
        return

    headers = {"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"}
    
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/opinions/",
            params={"court": court_id, "order_by": "-date_filed", "page_size": limit},
            headers=headers, timeout=15
        )
        if r.status_code == 200:
            opinions = r.json().get("results", [])
            if opinions:
                output.append(f"\n  Recent Opinions ({len(opinions)}):")
                for o in opinions:
                    case = o.get("case_name", "Unknown")
                    date = o.get("date_filed", "?")
                    url = f"https://www.courtlistener.com{o.get('absolute_url', '')}"
                    snippet = (o.get("plain_text", "") or "")[:200].replace("\n", " ")
                    output.append(f"    {date} | {case}")
                    output.append(f"    {url}")
                    if snippet:
                        output.append(f"    \"{snippet}...\"")
                        output.append("")
    except:
        pass


def show_court_detail(code, output):
    """Fetch and display detailed court info from CourtListener API."""
    token = get_token()
    if not token:
        return

    headers = {"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"}
    
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/courts/{code}/",
            headers=headers, timeout=15
        )
        if r.status_code == 200:
            c = r.json()
            address = c.get("address", "")
            phone = c.get("phone", "")
            url = c.get("url", "")
            if address:
                output.append(f"  Address: {address}")
            if phone:
                output.append(f"  Phone: {phone}")
            if url and url != f"https://www.{code}.uscourts.gov":
                output.append(f"  Court Website: {url}")
    except:
        pass


def run(args):
    if not args:
        return "[FEDERAL] Usage: /federal [circuit|district|supreme|judges|opinions|rules|pacer] -- e.g., /federal 9th circuit, /federal SDNY, /federal SDNY judges, /federal 9th circuit opinions"

    output = []
    output.append("")
    output.append("=" * 60)
    output.append(f"FEDERAL COURTS: {args}")
    output.append("=" * 60)

    try:
        args_lower = args.lower().strip()
        token = get_token()
        headers = {"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"} if token else {}

        # --- CIRCUIT LOOKUP ---
        circuit_num = None
        for num in CIRCUITS:
            if (num == args_lower) or (f"{num} " in args_lower and "circuit" in args_lower) or (f"{num}th" in args_lower and "circuit" in args_lower):
                circuit_num = num
                break
        if not circuit_num:
            for num, data in CIRCUITS.items():
                if data["name"].lower() in args_lower:
                    circuit_num = num
                    break

        if circuit_num:
            c = CIRCUITS[circuit_num]
            output.append(f"  {c['name']}")
            output.append(f"  States: {', '.join(c['states'])}")
            output.append(f"  Website: {c['url']}")

            # Check for subcommands
            if "judge" in args_lower:
                show_judges(f"ca{circuit_num}", output)
                return "\n".join(output)

            if "opinion" in args_lower:
                show_opinions(f"ca{circuit_num}", output)
                return "\n".join(output)

            output.append(f"\n  District Courts ({len(c['districts'])}):")
            for d in c["districts"]:
                name = DISTRICT_NAMES.get(d, d.upper())
                output.append(f"    {name}")
                output.append(f"      https://www.{d}.uscourts.gov")
                output.append(f"      PACER: https://ecf.{d}.uscourts.gov")
            output.append("")
            output.append("  For judges: /federal [circuit] judges")
            output.append("  For opinions: /federal [circuit] opinions")
            output.append("  Resources (Ctrl+Click):")
            output.append(f"    {c['url']}")
            output.append("    https://pacer.uscourts.gov")
            return "\n".join(output)

        # --- SUPREME COURT ---
        if "supreme" in args_lower or "scotus" in args_lower:
            output.append("  Supreme Court of the United States")
            output.append("  Website: https://www.supremecourt.gov")

            if "judge" in args_lower or "justice" in args_lower:
                show_judges("scotus", output)
                return "\n".join(output)

            if "opinion" in args_lower:
                show_opinions("scotus", output)
                return "\n".join(output)

            # Default: show recent opinions
            show_opinions("scotus", output, limit=5)
            
            output.append("")
            output.append("  Resources (Ctrl+Click):")
            output.append("    https://www.supremecourt.gov")
            output.append("    https://www.oyez.org")
            return "\n".join(output)

        # --- SPECIFIC DISTRICT ---
        district_code = resolve_district_code(args_lower)
        
        # Handle "SDNY judges", "SDNY opinions", etc.
        if not district_code:
            parts = args_lower.split()
            if len(parts) >= 2:
                potential_code = resolve_district_code(parts[0])
                if potential_code:
                    district_code = potential_code

        if district_code:
            name = DISTRICT_NAMES[district_code]
            output.append(f"  {name}")
            output.append(f"  Website: https://www.{district_code}.uscourts.gov")
            output.append(f"  PACER: https://ecf.{district_code}.uscourts.gov")

            # Find circuit
            for cnum, cdata in CIRCUITS.items():
                if district_code in cdata["districts"]:
                    output.append(f"  Circuit: {cdata['name']} ({cdata['url']})")
                    break

            # Subcommands
            if "judge" in args_lower:
                show_court_detail(district_code, output)
                show_judges(district_code, output)
                return "\n".join(output)

            if "opinion" in args_lower or "case" in args_lower:
                show_opinions(district_code, output)
                return "\n".join(output)

            output.append("")
            output.append("  For judges: /federal [court] judges")
            output.append("  For opinions: /federal [court] opinions")
            output.append("  Use /docket [case number] to search for cases")
            return "\n".join(output)

        # --- FEDERAL RULES ---
        if "rule" in args_lower or "frcp" in args_lower or "fre" in args_lower or "frap" in args_lower:
            output.append("  Federal Rules lookup via Chronicle...")
            try:
                from agents.webclaw.core.chronicle_ledger import get_chronicle
                chronicle = get_chronicle()
                results = chronicle.recover_by_context(f"{args} federal rules procedure evidence appellate", limit=5)
                if results:
                    output.append(f"  Found {len(results)} references:")
                    for r in results[:5]:
                        ctx = r["context"] if isinstance(r, dict) else str(r)
                        url = r["url"] if isinstance(r, dict) else ""
                        output.append(f"\n    SOURCE: {url}")
                        output.append(f"    {ctx[:1000]}")
            except Exception as e:
                output.append(f"  Chronicle error: {e}")
            
            output.append("")
            output.append("  Federal Rules Resources:")
            output.append("    FRCP: https://www.law.cornell.edu/rules/frcp")
            output.append("    FRE: https://www.law.cornell.edu/rules/fre")
            output.append("    FRAP: https://www.law.cornell.edu/rules/frap")
            return "\n".join(output)

        # --- PACER ---
        if "pacer" in args_lower:
            output.append("  PACER - Public Access to Court Electronic Records")
            output.append("")
            output.append("  Registration: https://pacer.uscourts.gov/register-account")
            output.append("  Fees: $0.10 per page ($3.00 max per document)")
            output.append("  Fee exemption: under $30/quarter, fees are waived")
            output.append("")
            output.append("  For a specific court, use: /federal [district code]")
            output.append("  e.g., /federal SDNY shows PACER link for S.D.N.Y.")
            output.append("")
            output.append("  Resources (Ctrl+Click):")
            output.append("    https://pacer.uscourts.gov")
            output.append("    https://www.courtlistener.com (free alternative)")
            return "\n".join(output)

        # --- GENERIC FEDERAL RESEARCH ---
        output.append("[*] Researching federal court system...")
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            results = chronicle.recover_by_context(f"{args} federal court circuit district jurisdiction", limit=5)
            if results:
                ctx_parts = []
                for r in results[:5]:
                    ctx = r["context"] if isinstance(r, dict) else str(r)
                    ctx_parts.append(ctx[:1000])
                chronicle_context = "\n\n---\n\n".join(ctx_parts)
                
                prompt = f"""Provide information about the US federal court system addressing: {args}

REFERENCE DATA:
{chronicle_context[:3000]}

Cover: court structure, jurisdiction, relevant courts, website URLs, and how to access records.
Cite sources. Be specific.

Federal Court Research:"""
                
                resp = requests.post(
                    f"{A2A}/v1/message/llmclaw",
                    json={"task": f"/llm {prompt}", "agent": "lawclaw"},
                    timeout=120
                )
                if resp.status_code == 200:
                    result = resp.json().get("result", "")
                    if result and len(result) > 50:
                        output.append("")
                        output.append(result)
        except:
            pass

        output.append("")
        output.append("  Federal Resources (Ctrl+Click):")
        output.append("    Supreme Court: https://www.supremecourt.gov")
        output.append("    PACER: https://pacer.uscourts.gov")
        output.append("    US Courts: https://www.uscourts.gov")
        output.append("    CourtListener: https://www.courtlistener.com")
        return "\n".join(output)

    except Exception as e:
        output.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(output)