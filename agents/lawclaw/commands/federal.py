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

# District code to full name mapping (94 districts + territories)
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

# Common abbreviation to district code mapping
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
    "dak": "akd", "daz": "azd", "dco": "cod", "dct": "ctd", "dde": "ded",
    "dhi": "hid", "did": "idd", "dks": "ksd", "dma": "mad", "dmd": "mdd",
    "dme": "med", "dmn": "mnd", "dmt": "mtd", "dne": "ned", "dnh": "nhd",
    "dnj": "njd", "dnm": "nmd", "dnv": "nvd", "dor": "ord", "dpr": "prd",
    "dri": "rid", "dsc": "scd", "dsd": "sdd", "dut": "utd", "dvt": "vtd",
    "dwy": "wyd",
}

#


def get_token():
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        for line in env_path.read_text().split("\n"):
            if "COURTLISTENER_TOKEN" in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except:
        pass
    return None


def run(args):
    if not args:
        return "[FEDERAL] Usage: /federal [circuit|district|supreme|rules|pacer] -- e.g., /federal 9th circuit, /federal SDNY, /federal supreme, /federal rules of evidence"

    output = []
    output.append("")
    output.append("=" * 60)
    output.append(f"FEDERAL COURTS: {args}")
    output.append("=" * 60)

    try:
        args_lower = args.lower().strip()

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
            output.append(f"\n  District Courts ({len(c['districts'])}):")
            for d in c["districts"]:
                name = DISTRICT_NAMES.get(d, d.upper())
                output.append(f"    {name}")
                output.append(f"      https://www.{d}.uscourts.gov")
                output.append(f"      PACER: https://ecf.{d}.uscourts.gov")
            output.append("")
            output.append("  Resources (Ctrl+Click):")
            output.append(f"    {c['url']}")
            output.append("    https://pacer.uscourts.gov")
            return "\n".join(output)

        # --- SUPREME COURT ---
        if "supreme" in args_lower or "scotus" in args_lower:
            output.append("  Supreme Court of the United States")
            output.append("  Website: https://www.supremecourt.gov")
            
            token = get_token()
            if token:
                headers = {"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"}
                r = requests.get(
                    f"{COURTLISTENER_API}/opinions/",
                    params={"court": "scotus", "order_by": "-date_filed", "page_size": 5},
                    headers=headers, timeout=15
                )
                if r.status_code == 200:
                    opinions = r.json().get("results", [])
                    if opinions:
                        output.append(f"\n  Recent opinions ({len(opinions)}):")
                        for o in opinions:
                            case = o.get("case_name", "Unknown")
                            date = o.get("date_filed", "?")
                            url = f"https://www.courtlistener.com{o.get('absolute_url', '')}"
                            output.append(f"    {date} | {case}")
                            output.append(f"    {url}")
            else:
                output.append("  (Add COURTLISTENER_TOKEN to .env for live opinions)")
            
            output.append("")
            output.append("  Resources (Ctrl+Click):")
            output.append("    https://www.supremecourt.gov")
            output.append("    https://www.oyez.org")
            return "\n".join(output)

        # --- SPECIFIC DISTRICT ---
        lookup = args_lower.replace(".", "").replace(" ", "")
        matched_code = ABBREV_MAP.get(lookup, lookup)
        
        if matched_code in DISTRICT_NAMES:
            name = DISTRICT_NAMES[matched_code]
            output.append(f"  {name}")
            output.append(f"  Website: https://www.{matched_code}.uscourts.gov")
            output.append(f"  PACER: https://ecf.{matched_code}.uscourts.gov")
            
            for cnum, cdata in CIRCUITS.items():
                if matched_code in cdata["districts"]:
                    output.append(f"  Circuit: {cdata['name']} ({cdata['url']})")
                    break
            
            output.append("")
            output.append("  Use /docket [case number] to search for cases in this court")
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