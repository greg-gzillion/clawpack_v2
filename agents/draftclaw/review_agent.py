# DraftClaw /review Agent - Jurisdiction-Aware Building Permit Review
# Phase 1: Structure and jurisdiction lookup

from pathlib import Path
import re
import json

JURISDICTION_BASE = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

def lookup_jurisdiction(query: str) -> dict:
    """Search for a jurisdiction by name and return its building code data"""
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
                        
                        # Match query against county name or full path
                        if query_lower in county_name or query_lower in f'{county_name} {state_abbr.lower()}':
                            content = bc_file.read_text(encoding='utf-8')
                            results.append({
                                'jurisdiction': f'{county_dir.name.replace("_", " ")}, {state_abbr}',
                                'path': str(bc_file.relative_to(JURISDICTION_BASE)),
                                'content': content,
                                'confidence': _score_confidence(content)
                            })
    
    return results

def _score_confidence(content: str) -> int:
    """Score a jurisdiction's data confidence from 0-100"""
    score = 0
    if 'verified May 2026' in content: score += 30
    elif 'site live - browser access' in content: score += 15
    if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content): score += 20
    if 'County Seat:' in content or 'Parish Seat:' in content: score += 15
    if 'IBC' in content or 'IRC' in content: score += 15
    if 'Frost:' in content or 'Snow:' in content or 'Wind:' in content: score += 10
    if re.search(r'\d+\s+[A-Z]', content): score += 10
    return score

def review_permit(jurisdiction_name: str, project_type: str, dimensions: str = '') -> dict:
    """Review a permit application against jurisdiction requirements"""
    jurisdictions = lookup_jurisdiction(jurisdiction_name)
    
    if not jurisdictions:
        return {'error': f'No jurisdiction found for "{jurisdiction_name}"'}
    
    jur = jurisdictions[0]  # Best match
    content = jur['content']
    
    review = {
        'jurisdiction': jur['jurisdiction'],
        'confidence_score': jur['confidence'],
        'project_type': project_type,
        'dimensions': dimensions,
        'code_references': [],
        'design_criteria': {},
        'missing_items': [],
        'warnings': [],
        'ahj_contact': {},
        'recommendations': []
    }
    
    # Extract design criteria
    frost_match = re.search(r'Frost[:\s]+(\d+[-\d]*\s*in)', content)
    snow_match = re.search(r'Snow[:\s]+(\d+[-\d]*\s*psf)', content)
    wind_match = re.search(r'Wind[:\s]+(\d+[-\d]*\s*mph)', content)
    seismic_match = re.search(r'Seismic[:\s]+(SDC\s*[A-D])', content)
    
    if frost_match: review['design_criteria']['frost_depth'] = frost_match.group(1)
    if snow_match: review['design_criteria']['snow_load'] = snow_match.group(1)
    if wind_match: review['design_criteria']['wind_speed'] = wind_match.group(1)
    if seismic_match: review['design_criteria']['seismic'] = seismic_match.group(1)
    
    # Extract code references
    for code in ['IBC', 'IRC', 'NEC', 'IPC', 'IMC', 'IFC', 'IECC']:
        if code in content:
            review['code_references'].append(code)
    
    # Extract contact info
    phone_match = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url_match = re.search(r'(https://[^\s\)]+)', content)
    ahj_match = re.search(r'AHJ[:\s]+([^\n]+)', content)
    
    if phone_match: review['ahj_contact']['phone'] = phone_match.group(1)
    if url_match: review['ahj_contact']['url'] = url_match.group(1)
    if ahj_match: review['ahj_contact']['name'] = ahj_match.group(1).strip()
    
    # Check for missing critical data
    if not review['design_criteria']:
        review['missing_items'].append('No design criteria found - geotechnical report required')
        review['recommendations'].append('PE review recommended for foundation design')
    
    if not review['code_references']:
        review['missing_items'].append('No specific code references found')
        review['warnings'].append('IBC 2018 assumed - verify with AHJ')
    
    if jur['confidence'] < 60:
        review['warnings'].append(f'Low jurisdiction confidence ({jur["confidence"]}%) - verify all data with AHJ')
        review['recommendations'].append('Direct AHJ contact recommended before submission')
    
    if jur['confidence'] < 90:
        review['recommendations'].append('Verify URL and contact information before permit submittal')
    
    # Project-specific checks
    if 'warehouse' in project_type.lower() or 'commercial' in project_type.lower():
        if 'snow_load' not in review['design_criteria']:
            review['missing_items'].append('Snow load not specified - required for roof design')
        if 'wind_speed' not in review['design_criteria']:
            review['missing_items'].append('Wind speed not specified - required for lateral design')
    
    if review['confidence_score'] < 90:
        review['recommendations'].append('PE/SE stamp likely required - verify with AHJ')
    
    return review

# Test
if __name__ == '__main__':
    result = review_permit('Denver', 'commercial warehouse', '100x200')
    print(json.dumps(result, indent=2))
