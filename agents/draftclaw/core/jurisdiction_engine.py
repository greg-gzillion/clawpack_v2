# DraftClaw Shared Jurisdiction Engine
# Core module: lookup_jurisdiction, score_confidence, classify_occupancy, extract_design_criteria
# Used by ALL review agents to prevent duplication
# UPDATED v2: Searches city subdirectories for design criteria, not just county-level

import re
from pathlib import Path
from typing import Dict, List

JURISDICTION_BASE = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

STATE_NAMES = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR', 'california': 'CA',
    'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA',
    'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA',
    'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO',
    'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV', 'new hampshire': 'NH', 'new jersey': 'NJ',
    'new mexico': 'NM', 'new york': 'NY', 'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH',
    'oklahoma': 'OK', 'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI',
    'south carolina': 'SC', 'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX',
    'utah': 'UT', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
    'wisconsin': 'WI', 'wyoming': 'WY', 'district of columbia': 'DC', 'dc': 'DC',
    'puerto rico': 'PR', 'guam': 'GU', 'virgin islands': 'VI', 'american samoa': 'AS',
}

OCCUPANCY_CLASSES = {
    'assembly': {'group': 'A', 'subtypes': ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'], 'desc': 'Assembly', 'triggers': ['theater', 'church', 'restaurant', 'bar', 'stadium', 'arena', 'auditorium', 'gym', 'banquet', 'nightclub', 'conference']},
    'business': {'group': 'B', 'subtypes': ['B'], 'desc': 'Business', 'triggers': ['office', 'bank', 'clinic', 'professional', 'medical office', 'courthouse', 'town hall']},
    'educational': {'group': 'E', 'subtypes': ['E'], 'desc': 'Educational', 'triggers': ['school', 'daycare', 'university', 'college', 'classroom', 'academy']},
    'factory': {'group': 'F', 'subtypes': ['F-1', 'F-2'], 'desc': 'Factory/Industrial', 'triggers': ['factory', 'manufacturing', 'plant', 'mill', 'refinery', 'fabrication']},
    'high_hazard': {'group': 'H', 'subtypes': ['H-1', 'H-2', 'H-3', 'H-4', 'H-5'], 'desc': 'High Hazard', 'triggers': ['chemical', 'explosive', 'flammable', 'hazardous', 'toxic', 'pyrotechnic']},
    'institutional': {'group': 'I', 'subtypes': ['I-1', 'I-2', 'I-3', 'I-4'], 'desc': 'Institutional', 'triggers': ['hospital', 'nursing home', 'jail', 'prison', 'assisted living', 'rehab']},
    'mercantile': {'group': 'M', 'subtypes': ['M'], 'desc': 'Mercantile', 'triggers': ['store', 'shop', 'retail', 'mall', 'market', 'showroom', 'grocery']},
    'residential': {'group': 'R', 'subtypes': ['R-1', 'R-2', 'R-3', 'R-4'], 'desc': 'Residential', 'triggers': ['apartment', 'condo', 'hotel', 'motel', 'house', 'home', 'dormitory', 'townhouse', 'duplex']},
    'storage': {'group': 'S', 'subtypes': ['S-1', 'S-2'], 'desc': 'Storage', 'triggers': ['warehouse', 'storage', 'garage', 'parking', 'distribution', 'self-storage']},
    'utility': {'group': 'U', 'subtypes': ['U'], 'desc': 'Utility/Misc', 'triggers': ['shed', 'fence', 'tank', 'tower', 'greenhouse', 'carport']},
}


def lookup_jurisdiction(query: str) -> List[Dict]:
    """Search for a jurisdiction by city or county name. 
    Searches BOTH county-level and city-level building_code.md files.
    City-level files contain the actual design criteria (frost, snow, wind, seismic)."""
    query_lower = query.lower().strip()
    results = []

    # Also search for individual words and state name resolution
    query_words = query_lower.split()
    # Resolve state names to abbreviations
    resolved_states = []
    for word in query_words:
        if word in STATE_NAMES:
            resolved_states.append(STATE_NAMES[word].lower())
    # Also check multi-word state names
    for state_name, abbr in STATE_NAMES.items():
        if state_name in query_lower:
            resolved_states.append(abbr.lower())
    
    for state_dir in sorted(JURISDICTION_BASE.iterdir()):
        if not state_dir.is_dir() or len(state_dir.name) != 2 or not state_dir.name.isalpha():
            continue
        state_abbr = state_dir.name.upper()
        
        for county_dir in state_dir.iterdir():
            if not county_dir.is_dir() or county_dir.name in ('state', '__pycache__'):
                continue
            county_name = county_dir.name.replace('_', ' ').lower()
            
            # --- CITY-LEVEL SEARCH (primary — contains design criteria) ---
            for city_dir in county_dir.iterdir():
                if not city_dir.is_dir():
                    continue
                city_bc = city_dir / 'building_code.md'
                if city_bc.exists():
                    city_name = city_dir.name.replace('_', ' ').lower()
                    # Match: full query in city name, or any query word in city name
                    city_match = query_lower in city_name
                    if not city_match:
                        for word in query_lower.split():
                            if len(word) >= 3 and word in city_name:
                                city_match = True
                                break
                    if not city_match:
                        for qw in query_words:
                            if qw in city_name and len(qw) >= 3:
                                city_match = True
                                break
                    if city_match:
                        content = city_bc.read_text(encoding='utf-8')
                        results.append({
                            'jurisdiction': f'{city_dir.name.replace("_", " ")}, {state_abbr}',
                            'county': county_name,
                            'path': str(city_bc.relative_to(JURISDICTION_BASE)),
                            'content': content,
                            'confidence': _score_confidence(content),
                            'source': 'city'
                        })
            
            # --- COUNTY-LEVEL SEARCH (fallback if city not found) ---
            bc_file = county_dir / 'building_code.md'
            if bc_file.exists() and (query_lower in county_name or query_lower in f'{county_name} {state_abbr.lower()}'):
                content = bc_file.read_text(encoding='utf-8')
                results.append({
                    'jurisdiction': f'{county_dir.name.replace("_", " ")}, {state_abbr}',
                    'county': None,
                    'path': str(bc_file.relative_to(JURISDICTION_BASE)),
                    'content': content,
                    'confidence': _score_confidence(content),
                    'source': 'county'
                })
    
    return results


def _score_confidence(content: str) -> int:
    """Score a jurisdiction's data confidence from 0-100."""
    score = 30  # Base score for having a file
    if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content): score += 15
    if '## AHJ:' in content: score += 10
    if '## URL:' in content: score += 10
    if '## County:' in content or '## Parish:' in content: score += 10
    if '## Wind:' in content: score += 10
    if '## Frost:' in content: score += 5
    if '## Snow:' in content: score += 5
    if '## Seismic:' in content: score += 5
    return min(score, 100)


def classify_occupancy(project_description: str) -> Dict:
    """Classify project into IBC occupancy group based on description text."""
    desc_lower = project_description.lower()
    for key, data in OCCUPANCY_CLASSES.items():
        for trigger in data['triggers']:
            if trigger in desc_lower:
                return {'group': data['group'], 'classification': data['desc'], 'subtypes': data['subtypes'], 'trigger_word': trigger, 'confidence': 'high' if trigger in desc_lower.split() else 'medium'}
    return {'group': 'B', 'classification': 'Business (default)', 'subtypes': ['B'], 'trigger_word': 'none', 'confidence': 'low - verify with AHJ'}


def extract_design_criteria(content: str) -> Dict:
    """Extract frost_depth, snow_load, wind_speed, seismic from jurisdiction file content."""
    criteria = {}
    patterns = {
        'frost_depth': r'Frost[:\s]+(\d+[-\d]*\s*in)',
        'snow_load': r'Snow[:\s]+(\d+[-\d]*\s*psf)',
        'wind_speed': r'Wind[:\s]+(\d+[-\d]*\s*mph)',
        'seismic': r'Seismic[:\s]+(SDC\s*[A-D][A-D]?)'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            criteria[key] = match.group(1).strip()
    return criteria


def extract_contact(content: str) -> Dict:
    """Extract phone and URL from jurisdiction file content."""
    contact = {}
    phone = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url = re.search(r'(https?://[^\s\)]+)', content)
    ahj = re.search(r'## AHJ:\s*(.+)', content)
    if phone: contact['phone'] = phone.group(1)
    if url: contact['url'] = url.group(1)
    if ahj: contact['ahj'] = ahj.group(1).strip()
    return contact
