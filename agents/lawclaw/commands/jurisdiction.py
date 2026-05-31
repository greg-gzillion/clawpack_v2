# agents/lawclaw/commands/jurisdiction.py - Rewritten with intelligence pipeline
# Chronicle FTS5 -> relevance scoring -> structured extraction -> compact prompt -> Groq (2-3s)
import re
from pathlib import Path

name = "/jurisdiction"

LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
JURISDICTIONS_ROOT = LAW_REFS / "jurisdictions" / "us"
SKIP_FOLDERS = {"docu_resources", "draw_resources", "medi_resources", "state"}
STATE_CODES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC","PR","GU","MP"}

ENTITY_PATTERNS = {
    "courts": [r"(?i)(municipal|court|circuit|district|superior|supreme|appellate|judicial|clerk of court|county court)"],
    "police": [r"(?i)(police department|sheriff|law enforcement|chief of police|public safety|highway patrol|state police)"],
    "detention": [r"(?i)(jail|detention|correction|inmate|correctional facility)"],
    "hospital": [r"(?i)(hospital|medical center|emergency room|ER|urgent care|health system|regional health)"],
    "library": [r"(?i)(library|public library|law library|county library|branch library)"],
    "building": [r"(?i)(building permit|building department|code enforcement|zoning|planning department|building inspection)"],
    "city_hall": [r"(?i)(city hall|municipal building|town hall|county administration|government center|mayor)"],
}

def score_block(block, city, state):
    """Score a block for relevance to the query city/state."""
    text = block.lower()
    city_lower = city.lower()
    state_lower = state.lower()
    score = 0
    if city_lower in text: score += 15
    if state_lower in text: score += 5
    legal_terms = ["court","municipal","ordinance","police","detention","clerk","records","statute","code","sheriff","jail","permit","zoning"]
    score += sum(2 for t in legal_terms if t in text)
    return score

def extract_entities(content, city, state):
    """Extract structured entities from raw content."""
    entities = {k: [] for k in ENTITY_PATTERNS}
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped: continue
        
        # Detect section headers
        for section, patterns in ENTITY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line_stripped):
                    current_section = section
                    break
        
        # Collect lines with URLs, addresses, or phone numbers
        has_info = any([
            'https://' in line_stripped,
            re.search(r'\d{3}[-.]\d{3}[-.]\d{4}', line_stripped),
            re.search(r'\d{1,5}\s+\w+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Way|Court|Ct|Plaza|Pkwy|Highway|Hwy)', line_stripped, re.IGNORECASE),
            current_section and len(line_stripped) > 15,
        ])
        
        if has_info and current_section:
            entities[current_section].append(line_stripped[:200])
    
    return entities

def run(args, agent=None):
    if not args:
        return "Usage: /jurisdiction <city> <state>\nExample: /jurisdiction Denver CO"

    from agents.lawclaw.commands._memory import recall, remember, show_prior

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"JURISDICTION: {args}")
    out.append("=" * 60)

    # Memory check
    prior = recall(f"jurisdiction {args}", limit=3)
    if prior:
        show_prior(f"jurisdiction {args}", out)

    try:
        # Check DataClaw cache first
        cache_key = f'jurisdiction:{args.strip().lower().replace(" ", "_")}'
        if agent and hasattr(agent, 'get_cached_result'):
            cached = agent.get_cached_result('lawclaw', cache_key)
            if cached:
                cached_text = cached.get('results', str(cached))
                out.append("[CACHE HIT] Returning cached result")
                out.append("")
                out.append("=" * 60)
                out.append(cached_text)
                out.append("=" * 60)
                return "\n".join(out)

        # Parse city and state
        parts = args.strip().split()
        state_code = None
        city_query = args.strip()
        for part in parts:
            if part.upper() in STATE_CODES:
                state_code = part.upper()
                city_query = " ".join(p for p in parts if p.upper() != state_code)
                break

        # STEP 1: Chronicle search
        out.append("[1/3] Chronicle search...")
        all_urls = []
        chronicle_blocks = []
        if agent and hasattr(agent, 'search_chronicle'):
            try:
                results = agent.search_chronicle(args, limit=10)
                if results:
                    for c in results:
                        ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                        url = c.get("url", "") if isinstance(c, dict) else ""
                        if ctx:
                            chronicle_blocks.append(ctx[:300])
                        if url and "https://" in url:
                            all_urls.append(url)
                    out.append(f"  {len(results)} references found")
            except Exception as e:
                out.append(f"  Search error: {str(e)[:50]}")

        # STEP 2: Scored file search with entity extraction
        out.append("[2/3] Extracting civic entities...")
        scored_blocks = []
        
        if state_code and JURISDICTIONS_ROOT.joinpath(state_code).exists():
            state_dir = JURISDICTIONS_ROOT / state_code
            for folder in sorted(state_dir.iterdir()):
                if not folder.is_dir() or folder.name in SKIP_FOLDERS:
                    continue
                for md_file in folder.rglob("*.md"):
                    try:
                        content = md_file.read_text(encoding="utf-8", errors="ignore")
                        score = score_block(content, city_query, state_code)
                        if score > 0:
                            scored_blocks.append((score, content[:1500], folder.name))
                        # Extract URLs from all files
                        for line in content.split("\n"):
                            if "https://" in line:
                                url = line[line.index("https://"):].split()[0].rstrip(")")
                                if url not in all_urls:
                                    all_urls.append(url)
                    except Exception:
                        pass

        # Sort by relevance score, take top 15
        scored_blocks.sort(key=lambda x: x[0], reverse=True)
        top_blocks = scored_blocks[:15]
        
        # Extract structured entities from top blocks
        all_entities = {k: [] for k in ENTITY_PATTERNS}
        for score, content, folder in top_blocks:
            entities = extract_entities(content, city_query, state_code or "")
            for section, items in entities.items():
                all_entities[section].extend(items)

        # Deduplicate
        for section in all_entities:
            all_entities[section] = list(dict.fromkeys(all_entities[section]))[:5]

        # Build structured summary
        structured = f"City: {city_query}, State: {state_code or 'unknown'}\n\n"
        section_names = {
            "courts": "COURTS", "police": "POLICE", "detention": "DETENTION",
            "hospital": "HOSPITALS", "library": "LIBRARY", "building": "BUILDING PERMITS",
            "city_hall": "CITY HALL"
        }
        for key, title in section_names.items():
            items = all_entities.get(key, [])
            if items:
                structured += f"\n{title}:\n"
                for item in items[:5]:
                    structured += f"  {item}\n"

        entity_count = sum(len(v) for v in all_entities.values())
        out.append(f"  {len(top_blocks)} relevant sources, {entity_count} entities extracted")

        # STEP 3: Compact synthesis via LLM
        out.append("[3/3] Synthesizing civic profile...")
        
        prompt = f"""Generate a professional civic profile from this structured data.

{structured}

Rules:
- Use ONLY the data provided. Never invent addresses, phones, or URLs.
- Skip any section with no data.
- Format as: COURT NAME ? Address ? Phone ? Website
- Keep each entry to one line.

Sections: COURTS | POLICE | DETENTION | HOSPITALS | LIBRARY | BUILDING PERMITS | CITY HALL"""

        result = ""
        if agent and hasattr(agent, 'ask_llm'):
            # Try Groq first, then OpenRouter, then render structured
            import time as time_mod
            for attempt in range(2):
                try:
                    result = agent.ask_llm(prompt[:2500])
                    if result and len(result) > 100 and 'rate' not in result.lower():
                        break
                except Exception:
                    pass
                if attempt == 0:
                    time_mod.sleep(3)  # Brief pause before retry

        out.append("")
        out.append("=" * 60)
        
        if result and len(result) > 50 and "no information" not in result.lower():
            out.append(result)
        else:
            # Fallback: render structured data directly
            out.append("")
            out.append("CIVIC PROFILE (structured data):")
            out.append("")
            out.append(structured)
        
        out.append("=" * 60)

        # URLs
        unique_urls = list(dict.fromkeys(all_urls))
        if unique_urls:
            gov_urls = [u for u in unique_urls if ".gov" in u.lower()]
            other_urls = [u for u in unique_urls if ".gov" not in u.lower()]
            ranked = gov_urls + other_urls
            out.append("")
            out.append("  Reference URLs:")
            for url in ranked[:15]:
                out.append(f"    {url}")

        # Save to DataClaw cache for instant future retrieval
        final = result if result else structured
        if len(final) > 50 and agent and hasattr(agent, 'cache_result'):
            try:
                agent.cache_result('lawclaw', cache_key, final)
                out.append("  [Cached for instant recall]")
            except:
                pass

        # Remember for future
        remember(command="/jurisdiction", query=args, result_summary=final[:400], source_type="chronicle", confidence=0.95)

        return "\n".join(out)

    except Exception as e:
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)
