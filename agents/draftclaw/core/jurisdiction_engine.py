# DraftClaw Shared Jurisdiction Engine
# Core module: lookup_jurisdiction, score_confidence, classify_occupancy, extract_design_criteria
# v3: Chronicle-powered. Queries chronicle.db instead of filesystem walk.

import re, json, sqlite3
from pathlib import Path
from typing import Dict, List

CHRONICLE_DB = Path(r"C:/Users/greg/dev/clawpack_v2/data/chronicle.db")
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
    'wisconsin': 'WI', 'wyoming': 'WY',
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
    """Search chronicle database for jurisdiction by city or county name.
    Falls back to filesystem walk if chronicle is unavailable."""
    query_lower = query.lower().replace(",", " ").strip()
    results = []
    
    try:
        db = sqlite3.connect(str(CHRONICLE_DB))
        db.row_factory = sqlite3.Row
        
        search_terms = [query_lower]
        for word in query_lower.split():
            if len(word) >= 3 and word not in search_terms:
                search_terms.append(word)
        for state_name, abbr in STATE_NAMES.items():
            if state_name in query_lower and abbr.lower() not in search_terms:
                search_terms.append(abbr.lower())
        
        for term in search_terms:
            like_term = f'%{term}%'
            rows = db.execute(
                """SELECT url, context, metadata FROM chronicle 
                   WHERE json_extract(metadata, '$.level') = 'city' 
                   AND (json_extract(metadata, '$.city') LIKE ? 
                        OR json_extract(metadata, '$.state') LIKE ? 
                        OR json_extract(metadata, '$.county') LIKE ?)
                   LIMIT 15""",
                (like_term, like_term, like_term)
            ).fetchall()
            
            for row in rows:
                meta = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
                jur_name = f"{meta.get('city', '')}, {meta.get('state', '')}"
                results.append({
                    'jurisdiction': jur_name.strip(', '),
                    'path': row['url'],
                    'content': row['context'],
                    'confidence': _score_confidence(row['context']),
                    'source': 'city'
                })
        
        if not results:
            for term in search_terms:
                like_term = f'%{term}%'
                rows = db.execute(
                    """SELECT url, context, metadata FROM chronicle 
                       WHERE json_extract(metadata, '$.level') = 'county' 
                       AND (json_extract(metadata, '$.county') LIKE ? 
                            OR json_extract(metadata, '$.state') LIKE ?)
                       LIMIT 10""",
                    (like_term, like_term)
                ).fetchall()
                for row in rows:
                    meta = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
                    jur_name = f"{meta.get('county', '')}, {meta.get('state', '')}"
                    results.append({
                        'jurisdiction': jur_name.strip(', '),
                        'path': row['url'],
                        'content': row['context'],
                        'confidence': _score_confidence(row['context']),
                        'source': 'county'
                    })
        
        db.close()
    except Exception:
        return _filesystem_lookup(query)
    
    return results


def _filesystem_lookup(query: str) -> List[Dict]:
    """Fallback: walk filesystem if chronicle is unavailable."""
    query_lower = query.lower().replace(",", " ").strip()
    results = []
    for state_dir in sorted(JURISDICTION_BASE.iterdir()):
        if not state_dir.is_dir() or len(state_dir.name) != 2 or not state_dir.name.isalpha():
            continue
        state_abbr = state_dir.name.upper()
        for county_dir in state_dir.iterdir():
            if not county_dir.is_dir() or county_dir.name in ('state', '__pycache__'):
                continue
            for city_dir in county_dir.iterdir():
                if not city_dir.is_dir():
                    continue
                city_bc = city_dir / 'building_code.md'
                if city_bc.exists():
                    city_name = city_dir.name.replace('_', ' ').lower()
                    if query_lower in city_name:
                        content = city_bc.read_text(encoding='utf-8')
                        results.append({
                            'jurisdiction': f'{city_dir.name.replace("_", " ")}, {state_abbr}',
                            'path': str(city_bc),
                            'content': content,
                            'confidence': _score_confidence(content),
                            'source': 'city'
                        })
    return results


def _score_confidence(content: str) -> int:
    """Score a jurisdiction data confidence from 0-100."""
    score = 30
    if '## AHJ:' in content: score += 10
    if '## URL:' in content: score += 10
    if '## Phone:' in content: score += 15
    if '## Wind:' in content: score += 10
    if '## Frost:' in content: score += 5
    if '## Snow:' in content: score += 5
    if '## Seismic:' in content: score += 5
    if '## County:' in content or '## Parish:' in content: score += 5
    if 'verified_by' in content: score += 10
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
    """Extract phone, URL, AHJ, address from jurisdiction file content."""
    contact = {}
    phone = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url = re.search(r'(https?://[^\s\)]+)', content)
    ahj = re.search(r'## AHJ:\s*(.+)', content)
    addr = re.search(r'## Address:\s*(.+)', content)
    if phone: contact['phone'] = phone.group(1)
    if url: contact['url'] = url.group(1)
    if ahj: contact['ahj'] = ahj.group(1).strip()
    if addr: contact['address'] = addr.group(1).strip()
    return contact