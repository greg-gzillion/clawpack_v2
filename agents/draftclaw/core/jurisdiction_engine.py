# DraftClaw Shared Jurisdiction Engine
# Core module: lookup_jurisdiction, score_confidence, classify_occupancy, extract_design_criteria
# Used by ALL review agents to prevent duplication

import re
from pathlib import Path
from typing import Dict, List

JURISDICTION_BASE = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

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



# City-to-County mapping for major US cities
CITY_TO_COUNTY = {
    "phoenix": "maricopa",
    "chicago": "cook",
    "new york": "new york",
    "los angeles": "los angeles",
    "houston": "harris",
    "dallas": "dallas",
    "san antonio": "bexar",
    "san diego": "san diego",
    "austin": "travis",
    "san jose": "santa clara",
    "fort worth": "tarrant",
    "jacksonville": "duval",
    "columbus": "franklin",
    "charlotte": "mecklenburg",
    "indianapolis": "marion",
    "san francisco": "san francisco",
    "seattle": "king",
    "boston": "suffolk",
    "nashville": "davidson",
    "portland": "multnomah",
    "oklahoma city": "oklahoma",
    "las vegas": "clark",
    "baltimore": "baltimore city",
    "louisville": "jefferson",
    "milwaukee": "milwaukee",
    "albuquerque": "bernalillo",
    "tucson": "pima",
    "fresno": "fresno",
    "sacramento": "sacramento",
    "mesa": "maricopa",
    "atlanta": "fulton",
    "omaha": "douglas",
    "colorado springs": "el paso",
    "raleigh": "wake",
    "long beach": "los angeles",
    "virginia beach": "virginia beach",
    "detroit": "wayne",
    "memphis": "shelby",
    "washington dc": "district of columbia",
    "orlando": "orange",
    "tampa": "hillsborough",
    "cleveland": "cuyahoga",
    "pittsburgh": "allegheny",
    "cincinnati": "hamilton",
    "anchorage": "anchorage",
    "honolulu": "honolulu",
    "boise": "ada",
    "des moines": "polk",
    "wichita": "sedgwick",
    "fort lauderdale": "broward",
    "st petersburg": "pinellas",
    "lubbock": "lubbock",
    "el paso": "el paso",
    "reno": "washoe",
    "spokane": "spokane",
}

CITY_TO_COUNTY = {
    "albuquerque": "bernalillo",
    "anchorage": "anchorage",
    "atlanta": "fulton",
    "austin": "travis",
    "baltimore": "baltimore",
    "boise": "ada",
    "boston": "suffolk",
    "charlotte": "mecklenburg",
    "chicago": "cook",
    "cincinnati": "hamilton",
    "cleveland": "cuyahoga",
    "colorado springs": "el paso",
    "columbus": "franklin",
    "dallas": "dallas",
    "detroit": "wayne",
    "el paso": "el paso",
    "fort worth": "tarrant",
    "fresno": "fresno",
    "honolulu": "honolulu",
    "houston": "harris",
    "indianapolis": "marion",
    "jacksonville": "duval",
    "las vegas": "clark",
    "long beach": "los angeles",
    "louisville": "jefferson",
    "lubbock": "lubbock",
    "memphis": "shelby",
    "mesa": "maricopa",
    "milwaukee": "milwaukee",
    "nashville": "davidson",
    "oklahoma city": "oklahoma",
    "omaha": "douglas",
    "orlando": "orange",
    "phoenix": "maricopa",
    "pittsburgh": "allegheny",
    "portland": "multnomah",
    "raleigh": "wake",
    "reno": "washoe",
    "sacramento": "sacramento",
    "san antonio": "bexar",
    "seattle": "king",
    "spokane": "spokane",
    "tampa": "hillsborough",
    "tucson": "pima",
    "virginia beach": "virginia beach",
    "washington dc": "district of columbia",
}

def lookup_jurisdiction(query: str) -> List[Dict]:
    """Search for a jurisdiction by county or city name. Returns list of matching dicts with content and confidence."""
    query_lower = query.lower().strip()
    results = []
    for state_dir in sorted(JURISDICTION_BASE.iterdir()):
        if state_dir.is_dir() and len(state_dir.name) == 2 and state_dir.name.isalpha():
            for county_dir in state_dir.iterdir():
                if county_dir.is_dir() and county_dir.name not in ('state', '__pycache__'):
                    bc_file = county_dir / 'building_code.md'
                    if bc_file.exists():
                        county_name = county_dir.name.replace('_', ' ').lower()
                        state_abbr = state_dir.name.upper()
                        # Check county name, or city-to-county mapping
            mapped_county = CITY_TO_COUNTY.get(query_lower, '')
            if (query_lower in county_name or 
                query_lower in f'{county_name} {state_abbr.lower()}' or
                (mapped_county and mapped_county in county_name)):
                            content = bc_file.read_text(encoding='utf-8')
                            results.append({
                                'jurisdiction': f'{county_dir.name.replace("_", " ")}, {state_abbr}',
                                'path': str(bc_file.relative_to(JURISDICTION_BASE)),
                                'content': content,
                                'confidence': _score_confidence(content)
                            })
    return results


def _score_confidence(content: str) -> int:
    """Score a jurisdiction's data confidence from 0-100."""
    score = 0
    if 'verified May 2026' in content: score += 30
    elif 'site live - browser access' in content: score += 15
    if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content): score += 20
    if 'County Seat:' in content or 'Parish Seat:' in content: score += 15
    if 'IBC' in content or 'IRC' in content: score += 15
    if 'Frost:' in content or 'Snow:' in content or 'Wind:' in content: score += 10
    if re.search(r'\d+\s+[A-Z]', content): score += 10
    return score


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
    patterns = {'frost_depth': r'Frost[:\s]+(\d+[-\d]*\s*in)', 'snow_load': r'Snow[:\s]+(\d+[-\d]*\s*psf)', 'wind_speed': r'Wind[:\s]+(\d+[-\d]*\s*mph)', 'seismic': r'Seismic[:\s]+(SDC\s*[A-D])'}
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match: criteria[key] = match.group(1)
    return criteria


def extract_contact(content: str) -> Dict:
    """Extract phone and URL from jurisdiction file content."""
    contact = {}
    phone = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url = re.search(r'(https://[^\s\)]+)', content)
    if phone: contact['phone'] = phone.group(1)
    if url: contact['url'] = url.group(1)
    return contact
