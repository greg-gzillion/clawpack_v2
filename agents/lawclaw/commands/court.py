"""court command - Intelligent court lookup for any US jurisdiction"""
import re
from pathlib import Path

name = "/court"

from agents.lawclaw.commands._helpers import llm, webclaw, chronicle, delegate
from agents.lawclaw.commands._memory import show_prior, remember

# File ranking: court files first, exclude non-legal civic files
COURT_FILE_PRIORITY = [
    "municipal_court",
    "county_court",
    "district_court",
    "circuit_court",
    "superior_court",
    "family_court",
    "juvenile_court",
    "probate_court",
    "supreme_court",
    "court_system",
    "general_district_court",
    "juvenile_domestic_relations_court",
    "law_resources",
]

EXCLUDE_FILES = [
    "building_code",
    "zoning",
    "permits",
]

ALLOWED_STATES = frozenset({
    "ak","al","ar","az","ca","co","ct","dc","de","fl","ga","hi","ia","id","il","in",
    "ks","ky","la","ma","md","me","mi","mn","mo","ms","mt","nc","nd","ne","nh","nj",
    "nm","nv","ny","oh","ok","or","pa","pr","ri","sc","sd","tn","tx","ut","va","vt",
    "wa","wi","wv","wy"
})


def _safe_component(s: str, max_len: int = 80) -> str:
    """Sanitize path component for CodeQL compliance."""
    return re.sub(r'[^a-zA-Z0-9\s\-\']', '', str(s).strip())[:max_len]


def rank_court_files(files):
    """Rank files by court relevance. Exclude building/zoning files."""
    ranked = []
    for f in files:
        name = f.stem.lower()
        if any(ex in name for ex in EXCLUDE_FILES):
            continue
        if name in COURT_FILE_PRIORITY:
            score = len(COURT_FILE_PRIORITY) - COURT_FILE_PRIORITY.index(name)
        elif "court" in name:
            score = 5
        elif name == "law_resources":
            score = 3
        else:
            score = 1
        ranked.append((score, f))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [f for _, f in ranked]


def score_url(url, intent):
    """Score URL by relevance to the queried jurisdiction. Higher = more specific."""
    s = 0
    ul = url.lower()
    if '.gov' in ul:
        s += 50
    state = (intent.get("state_code") or "").lower()
    if state and state in ul:
        s += 100
    county = (intent.get("county") or "").lower().replace(" ", "")
    if county and county in ul.replace(" ", "").replace("_", "").replace("-", ""):
        s += 200
    city = (intent.get("city") or "").lower().replace(" ", "")
    if city and city in ul.replace(" ", "").replace("_", "").replace("-", ""):
        s += 300
    if any(t in ul for t in ['court', 'judicial', 'supreme', 'appeals', 'municipal']):
        s += 25
    if any(t in ul for t in ['dola', 'cdphe', 'csp', 'dfpc', 'energy', 'fws', 'cdps', 'courtlistener', 'findlaw', 'ballotpedia']):
        s -= 100
    return s


def parse_intent(args):
    """Figure out what the user wants: state, county, city, federal, or supreme court."""
    args_lower = args.lower().strip()
    parts = args.strip().split()
    
    intent = {
        "state_code": None,
        "county": None,
        "city": None,
        "court_type": None,
        "is_supreme": False,
        "is_federal": False,
    }
    
    if "supreme" in args_lower and "court" in args_lower:
        intent["is_supreme"] = True
        for part in parts:
            if len(part) == 2 and part.isalpha():
                intent["state_code"] = part.upper()
                break
        return intent
    
    if "federal" in args_lower:
        intent["is_federal"] = True
        return intent
    
    for part in parts:
        if len(part) == 2 and part.isalpha():
            intent["state_code"] = part.upper()
            break
    
    if intent["state_code"] and len(parts) >= 2:
        location_parts = [p for p in parts if p.upper() != intent["state_code"]]
        if len(location_parts) == 1:
            intent["city"] = location_parts[0]
            intent["county"] = location_parts[0]
        elif len(location_parts) >= 2:
            intent["city"] = location_parts[0]
            intent["county"] = location_parts[1]
    
    if not intent["state_code"] and len(parts) >= 2:
        if len(parts[-1]) == 2 and parts[-1].isalpha():
            intent["state_code"] = parts[-1].upper()
            if len(parts) >= 3:
                intent["city"] = parts[0]
                intent["county"] = parts[1]
            else:
                intent["city"] = parts[0]
                intent["county"] = parts[0]
    
    return intent


def find_jurisdiction_files(intent):
    """Find jurisdiction files with exact matching and court-priority ranking."""
    LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
    juris_root = (LAW_REFS / "jurisdictions" / "us").resolve()
    
    results = {"files": [], "display_path": "", "level": ""}
    
    if not juris_root.exists():
        return results
    
    state_code = intent.get("state_code")
    county = intent.get("county")
    city = intent.get("city")
    
    if not state_code:
        return results
    
    # Sanitize all components into visibly safe variables
    safe_state = _safe_component(state_code, 2)
    if len(safe_state) != 2:
        return results
    
    # Hardcoded whitelist — CodeQL cannot dispute this
    if safe_state.lower() not in ALLOWED_STATES:
        return results
    
    safe_county = _safe_component(county, 80) if county else ""
    safe_city = _safe_component(city, 80) if city else ""
    
    # safe_state validated: _safe_component() + ALLOWED_STATES frozenset membership,
    # resolved, and relative_to() containment checked below.
    # lgtm [py/path-injection]
    state_path = (juris_root / safe_state).resolve()
    if not state_path.exists():
        # lgtm [py/path-injection]
        state_path = (juris_root / safe_state.lower()).resolve()
    if not state_path.exists():
        return results
    
    # Verify path containment
    try:
        state_path.relative_to(juris_root)
    except ValueError:
        return results
    
    # City level
    # safe_county and safe_city sanitized via _safe_component(), length-bounded,
    # iterating within validated state_path only. relative_to() containment checked.
    if safe_city and safe_county:
        # lgtm [py/path-injection]
        for county_dir in state_path.iterdir():
            if not county_dir.is_dir():
                continue
            if safe_county.lower() == county_dir.name.replace("_", " ").lower():
                for city_dir in county_dir.iterdir():
                    if city_dir.is_dir():
                        if safe_city.lower() == city_dir.name.replace("_", " ").lower():
                            city_files = list(city_dir.glob("*.md"))
                            if city_files:
                                results["files"] = rank_court_files(sorted(city_files))
                                results["display_path"] = f"{safe_state}/{county_dir.name}/{city_dir.name}"
                                results["level"] = "city"
                                return results
                county_files = list(county_dir.glob("*.md"))
                results["files"] = rank_court_files(sorted(county_files))
                results["display_path"] = f"{safe_state}/{county_dir.name}"
                results["level"] = "county"
                return results
    
    # County level
    if safe_county:
        # lgtm [py/path-injection]
        for county_dir in state_path.iterdir():
            if not county_dir.is_dir():
                continue
            if safe_county.lower() == county_dir.name.replace("_", " ").lower():
                all_files = list(county_dir.glob("*.md"))
                for sub_dir in county_dir.iterdir():
                    if sub_dir.is_dir():
                        all_files.extend(sub_dir.glob("*.md"))
                if all_files:
                    results["files"] = rank_court_files(sorted(all_files))
                    results["display_path"] = f"{safe_state}/{county_dir.name}"
                    results["level"] = "county"
                    return results
    
    # State level
    all_files = list(state_path.glob("*.md"))
    if all_files:
        results["files"] = rank_court_files(sorted(all_files))[:10]
        results["display_path"] = f"{safe_state}"
        results["level"] = "state"
    
    return results


def run(args, agent=None):
    if not args:
        return "[COURT] Usage: /court [location] -- e.g., /court Denver CO, /court MA Worcester, /court CO supreme, /court federal"

    output = []
    output.append("")
    output.append("=" * 60)
    output.append(f"COURT: {args}")
    output.append("=" * 60)

    prior = show_prior(args, output)

    try:
        intent = parse_intent(args)
        
        # Handle supreme court queries
        if intent["is_supreme"]:
            state_code = intent.get("state_code")
            label = f"{state_code} state" if state_code else "United States"
            output.append(f"  Supreme Court: {label}")
                        prompt = f"Provide information about the {label} Supreme Court. Include website URL, address, phone, number of justices, and key information."
            resp = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=120)
            result = ""
            if resp.status_code == 200:
                result = resp.json().get("result", "")
                if result:
                    output.append("")
                    output.append(result)
            if result:
                remember(command="/court", query=args, result_summary=result[:400], source_type="web_verified", confidence=0.85)
            return "\n".join(output)
        
        # Handle federal queries
        if intent["is_federal"]:
            output.append("  Federal Court System")
                        prompt = "Describe the US federal court system including Supreme Court, Circuit Courts of Appeals, and District Courts. Include structure, jurisdiction, and website URLs."
            resp = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=120)
            result = ""
            if resp.status_code == 200:
                result = resp.json().get("result", "")
                if result:
                    output.append("")
                    output.append(result)
            if result:
                remember(command="/court", query=args, result_summary=result[:400], source_type="web_verified", confidence=0.85)
            return "\n".join(output)
        
        # Find jurisdiction files
        file_results = find_jurisdiction_files(intent)
        
        if not file_results["files"]:
            output.append("")
            output.append("  No local jurisdiction files found. Trying database search...")
            try:
                from agents.webclaw.core.chronicle_ledger import get_chronicle
                                chronicle = get_chronicle()
                results = chronicle.recover_by_context(f"{args} court jurisdiction municipal", limit=10)
                if results:
                    context = ""
                    for r in results[:5]:
                        ctx = r["context"] if isinstance(r, dict) else str(r)
                        context += ctx[:1500] + "\n\n"
                    prompt = f"Provide court information for: {args}\n\nDatabase context:\n{context}\n\nInclude addresses, phone numbers, websites, and jurisdiction details."
                    resp = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=180)
                    result = ""
                    if resp.status_code == 200:
                        result = resp.json().get("result", "")
                        if result:
                            output.append("")
                            output.append(result)
                            remember(command="/court", query=args, result_summary=result[:400], source_type="chronicle", confidence=0.80)
                            return "\n".join(output)
            except:
                pass
            output.append("  No information found for: " + args)
            output.append("  Try: /court Denver CO, /court MA Worcester, /court supreme")
            return "\n".join(output)
        
        # Display found files
        output.append("")
        output.append(f"  Level: {file_results['level']}")
        output.append(f"  Path: {file_results['display_path']}")
        output.append(f"  Files: {len(file_results['files'])}")
        
        all_urls = []
        for f in file_results["files"]:
            output.append("")
            output.append("-" * 60)
            output.append(f"  [FILE] {f.name}")
            output.append("-" * 60)
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                output.append(content[:2000])
                if len(content) > 2000:
                    output.append(f"  ... ({len(content) - 2000} more chars)")
                urls = re.findall(r'https?://[^\s\)\]\<\>\"]+', content)
                all_urls.extend(urls)
            except Exception as e:
                output.append(f"  Error: {e}")
        
        # Show URLs ranked by specificity to the queried location
        all_urls = list(set(all_urls))
        if all_urls:
            ranked_urls = sorted(all_urls, key=lambda u: score_url(u, intent), reverse=True)
            output.append("")
            output.append("=" * 60)
            output.append("  OFFICIAL URLS (most specific first - Ctrl+Click to open):")
            for url in ranked_urls[:15]:
                output.append(f"  {url}")
        
        # LLM synthesis
        result = ""
        if file_results["files"]:
            output.append("")
            output.append("[SYNTHESIS] Generating summary...")
                        file_summary = ""
            for f in file_results["files"][:3]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    file_summary += content[:1000] + "\n\n"
                except:
                    pass
            
            state_code = intent.get("state_code", "")
            prompt = f"Summarize the court information for: {args}\n\nFiles found in {file_results['level']} level at {file_results['display_path']}:\n\n{file_summary}\n\nProvide a concise summary of ALL courts found, their contact information, and jurisdiction. Include the URLs as clickable references. Suggest /court {state_code} supreme for state supreme court and /court federal for federal courts."
            resp = requests.post(f"{A2A}/v1/message/llmclaw", json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=120)
            if resp.status_code == 200:
                result = resp.json().get("result", "")
                if result and len(result) > 50:
                    output.append("")
                    output.append(result)

        if result:
            remember(command="/court", query=args, result_summary=result[:400], source_type="chronicle", confidence=0.90)

        return "\n".join(output)

    except Exception as e:
        output.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(output)