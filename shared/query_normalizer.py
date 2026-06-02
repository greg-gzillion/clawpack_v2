"""
shared/query_normalizer.py ? Canonical query normalization for all agents.

Single source of truth for:
- Command prefix stripping
- Location extraction (city/state)
- Query cleaning

Import in any agent instead of duplicating _extract_location.
"""
import re

# US state codes for detection
_STATE_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY","DC","PR"
}

_STATE_NAMES = {
    "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR",
    "california":"CA","colorado":"CO","connecticut":"CT","delaware":"DE",
    "florida":"FL","georgia":"GA","hawaii":"HI","idaho":"ID",
    "illinois":"IL","indiana":"IN","iowa":"IA","kansas":"KS",
    "kentucky":"KY","louisiana":"LA","maine":"ME","maryland":"MD",
    "massachusetts":"MA","michigan":"MI","minnesota":"MN",
    "mississippi":"MS","missouri":"MO","montana":"MT","nebraska":"NE",
    "nevada":"NV","new hampshire":"NH","new jersey":"NJ",
    "new mexico":"NM","new york":"NY","north carolina":"NC",
    "north dakota":"ND","ohio":"OH","oklahoma":"OK","oregon":"OR",
    "pennsylvania":"PA","rhode island":"RI","south carolina":"SC",
    "south dakota":"SD","tennessee":"TN","texas":"TX","utah":"UT",
    "vermont":"VT","virginia":"VA","washington":"WA",
    "west virginia":"WV","wisconsin":"WI","wyoming":"WY",
    "district of columbia":"DC","puerto rico":"PR",
}

_CMD_WORDS = {
    "court", "jurisdiction", "law", "state", "federal",
    "police", "hospital", "library", "detention", "judge",
    "statute", "docket", "precedent"
}


def strip_command(query: str) -> str:
    """Remove leading slash command and bare command words from a query.
    '/court Denver CO' -> 'Denver CO'
    'court Georgetown CO' -> 'Georgetown CO'
    """
    clean = re.sub(r'^/[a-z_]+\s+', '', query.strip(), count=1)
    parts = clean.strip().split()
    if parts and parts[0].lower() in _CMD_WORDS:
        clean = " ".join(parts[1:])
    return clean.strip()


def extract_location(query: str):
    """Extract city and state from a query for geographic filtering.
    Returns (city, state_code) or (None, None) if no location detected.
    
    Examples:
        '/court Denver CO' -> ('Denver', 'CO')
        'Colorado courts' -> (None, 'CO')
        'qualified immunity' -> (None, None)
    """
    clean = strip_command(query)
    
    # Pattern: "City, ST" or "City ST" at end
    match = re.search(r"([A-Za-z\s]+),?\s+([A-Z]{2})\s*$", clean.strip())
    if match:
        city = match.group(1).strip()
        state = match.group(2).upper()
        if state in _STATE_CODES:
            return city, state
    
    # Pattern: standalone 2-letter code anywhere
    words = clean.upper().split()
    for w in words:
        if w in _STATE_CODES:
            idx = words.index(w)
            if idx > 0:
                return words[idx-1].title(), w
            return None, w
    
    # Pattern: full state name
    clean_lower = clean.lower()
    for name, code in sorted(_STATE_NAMES.items(), key=lambda x: -len(x[0])):
        if name in clean_lower:
            return None, code
    
    return None, None
