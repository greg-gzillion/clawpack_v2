# DraftClaw /review Agent v2
# Adds: Occupancy Classification + Permit Submittal Checklist Generation

import re
import json
from pathlib import Path
from typing import Dict, List, Optional

JURISDICTION_BASE = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

# IBC Occupancy Classifications
OCCUPANCY_CLASSES = {
    'assembly': {'group': 'A', 'subtypes': ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'], 'desc': 'Assembly', 'triggers': ['theater', 'church', 'restaurant', 'bar', 'stadium', 'arena', 'auditorium', 'gym', 'community hall', 'banquet', 'nightclub', 'conference']},
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

# Permit submittal checklists by occupancy group
PERMIT_CHECKLISTS = {
    'A': ['Site plan', 'Floor plans', 'Egress plan', 'Fire protection systems', 'Accessibility compliance (ADA)', 'Structural calculations', 'Energy compliance (COMcheck)', 'Plumbing riser diagram', 'Mechanical plan', 'Electrical plan', 'Fire alarm system', 'Sprinkler system design', 'Crowd management plan', 'Acoustical report', 'Kitchen hood suppression (if applicable)'],
    'B': ['Site plan', 'Floor plans', 'Structural calculations', 'Energy compliance (COMcheck)', 'Plumbing floor plan', 'Mechanical plan', 'Electrical plan', 'Fire alarm system', 'Accessibility compliance (ADA)', 'Life safety plan'],
    'E': ['Site plan', 'Floor plans', 'Structural calculations', 'Energy compliance (COMcheck)', 'Plumbing plan', 'Mechanical plan', 'Electrical plan', 'Fire alarm system', 'Sprinkler system', 'Accessibility compliance (ADA)', 'Life safety plan', 'Playground safety (if applicable)', 'Security plan'],
    'F': ['Site plan', 'Floor plans', 'Structural calculations', 'Energy compliance (COMcheck)', 'Process equipment plan', 'Hazardous material inventory (if applicable)', 'Ventilation plan', 'Electrical plan', 'Fire protection systems', 'Waste disposal plan', 'OSHA compliance documentation'],
    'H': ['Site plan', 'Floor plans', 'Structural calculations', 'Hazardous material management plan', 'Explosion control plan', 'Fire protection systems', 'Emergency response plan', 'Ventilation plan', 'Containment plan', 'Chemical inventory', 'OSHA PSM documentation', 'EPA permits'],
    'I': ['Site plan', 'Floor plans', 'Structural calculations', 'Fire protection systems', 'Accessibility compliance (ADA)', 'Emergency evacuation plan', 'Medical gas systems (if healthcare)', 'Nurse call systems', 'Infection control plan', 'Security plan', 'Backup power systems'],
    'M': ['Site plan', 'Floor plans', 'Structural calculations', 'Energy compliance (COMcheck)', 'Plumbing plan', 'Mechanical plan', 'Electrical plan', 'Fire alarm system', 'Sprinkler system', 'Accessibility compliance (ADA)', 'Life safety plan', 'Parking study'],
    'R': ['Site plan', 'Floor plans', 'Unit plans', 'Structural calculations', 'Energy compliance (REScheck)', 'Plumbing riser diagram', 'Mechanical plan', 'Electrical plan', 'Fire alarm system', 'Sprinkler system', 'Accessibility compliance (ADA/FHA)', 'Ventilation plan', 'Acoustical report (multi-family)'],
    'S': ['Site plan', 'Floor plans', 'Structural calculations', 'Energy compliance (COMcheck)', 'Fire protection systems', 'Hazardous material storage plan (if applicable)', 'Loading dock plan', 'Vehicle circulation plan', 'Security plan', 'Racking system engineering'],
    'U': ['Site plan', 'Structural calculations (if required)', 'Energy compliance', 'Zoning approval', 'Utility connection plan'],
}

def classify_occupancy(project_description: str) -> Dict:
    """Classify project into IBC occupancy group based on description"""
    desc_lower = project_description.lower()
    
    for key, data in OCCUPANCY_CLASSES.items():
        for trigger in data['triggers']:
            if trigger in desc_lower:
                return {
                    'group': data['group'],
                    'classification': data['desc'],
                    'subtypes': data['subtypes'],
                    'trigger_word': trigger,
                    'confidence': 'high' if trigger in desc_lower.split() else 'medium'
                }
    
    # Default to Business if no match
    return {
        'group': 'B',
        'classification': 'Business (default)',
        'subtypes': ['B'],
        'trigger_word': 'none',
        'confidence': 'low - verify with AHJ'
    }

def generate_permit_checklist(occupancy_group: str, project_type: str, jurisdiction_data: Dict) -> List[Dict]:
    """Generate permit submittal checklist based on occupancy and jurisdiction"""
    base_checklist = PERMIT_CHECKLISTS.get(occupancy_group, PERMIT_CHECKLISTS['B'])
    
    checklist = []
    for item in base_checklist:
        entry = {'item': item, 'required': True, 'notes': ''}
        
        # Jurisdiction-specific adjustments
        if item == 'Accessibility compliance (ADA)' and 'ADA' in jurisdiction_data.get('code_refs', ''):
            entry['notes'] = 'ADA 2010 + state amendments may apply'
        
        if item == 'Energy compliance (COMcheck)' and 'IECC' in jurisdiction_data.get('code_refs', ''):
            entry['notes'] = 'Verify energy code edition with AHJ'
        
        if item == 'Sprinkler system' or item == 'Sprinkler system design':
            if 'IFC' not in jurisdiction_data.get('code_refs', ''):
                entry['required'] = 'Verify with fire marshal'
                entry['notes'] = 'Confirm sprinkler requirement with local fire official'
        
        checklist.append(entry)
    
    # Add jurisdiction-specific items
    if 'seismic' in jurisdiction_data.get('design_criteria', {}):
        if 'SDC D' in jurisdiction_data['design_criteria'].get('seismic', '') or 'SDC E' in jurisdiction_data['design_criteria'].get('seismic', ''):
            checklist.append({'item': 'Seismic design calculations', 'required': True, 'notes': 'High seismic design category - special inspection required'})
    
    if 'flood' in project_type.lower() or 'coastal' in project_type.lower():
        checklist.append({'item': 'FEMA flood zone determination', 'required': True, 'notes': 'Verify flood zone with FEMA FIRM maps'})
    
    return checklist

def detect_risk_flags(jurisdiction_data: Dict, occupancy: Dict, project_type: str) -> List[str]:
    """Detect professional review requirements and risk flags"""
    flags = []
    
    # Seismic risk
    seismic = jurisdiction_data.get('design_criteria', {}).get('seismic', '')
    if 'SDC D' in seismic or 'SDC E' in seismic:
        flags.append('⚠️ SE (Structural Engineer) stamp required - high seismic')
    
    # Wind risk
    wind = jurisdiction_data.get('design_criteria', {}).get('wind_speed', '')
    wind_num = int(re.search(r'(\d+)', wind).group(1)) if re.search(r'(\d+)', wind) else 0
    if wind_num >= 140:
        flags.append('⚠️ PE/SE review required - high wind zone')
    
    # Snow risk
    snow = jurisdiction_data.get('design_criteria', {}).get('snow_load', '')
    snow_num = int(re.search(r'(\d+)', snow).group(1)) if re.search(r'(\d+)', snow) else 0
    if snow_num >= 50:
        flags.append('⚠️ Snow load exceeds 50 psf - structural review recommended')
    
    # Occupancy risk
    if occupancy['group'] in ['H', 'I']:
        flags.append('🔴 Special occupancy - fire marshal review mandatory')
        flags.append('🔴 SE stamp required for all structural elements')
    
    if occupancy['group'] == 'A':
        flags.append('⚠️ Assembly occupancy - fire protection engineer review recommended')
    
    # Confidence risk
    confidence = jurisdiction_data.get('confidence', 0)
    if confidence < 60:
        flags.append('🔴 Low jurisdiction data confidence - verify all criteria with AHJ')
    elif confidence < 90:
        flags.append('⚠️ Medium confidence - confirm code editions with AHJ')
    
    return flags

def review_permit_v2(jurisdiction_name: str, project_description: str, dimensions: str = '') -> Dict:
    """Complete permit review with occupancy classification and checklist"""
    from review_agent import lookup_jurisdiction  # reuse v1 lookup
    
    jurisdictions = lookup_jurisdiction(jurisdiction_name)
    
    if not jurisdictions:
        return {'error': f'No jurisdiction found for "{jurisdiction_name}"'}
    
    jur = jurisdictions[0]
    content = jur['content']
    
    # Classify occupancy
    occupancy = classify_occupancy(project_description)
    
    # Extract jurisdiction data
    jur_data = {
        'confidence': jur['confidence'],
        'code_refs': content,
        'design_criteria': {}
    }
    
    for item in ['frost_depth', 'snow_load', 'wind_speed', 'seismic']:
        patterns = {
            'frost_depth': r'Frost[:\s]+(\d+[-\d]*\s*in)',
            'snow_load': r'Snow[:\s]+(\d+[-\d]*\s*psf)',
            'wind_speed': r'Wind[:\s]+(\d+[-\d]*\s*mph)',
            'seismic': r'Seismic[:\s]+(SDC\s*[A-D])'
        }
        match = re.search(patterns[item], content)
        if match:
            jur_data['design_criteria'][item] = match.group(1)
    
    # Generate checklist
    checklist = generate_permit_checklist(occupancy['group'], project_description, jur_data)
    
    # Detect risks
    risks = detect_risk_flags(jur_data, occupancy, project_description)
    
    # Extract contacts
    phone = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url = re.search(r'(https://[^\s\)]+)', content)
    
    review = {
        'jurisdiction': jur['jurisdiction'],
        'confidence_score': jur['confidence'],
        'project': {
            'description': project_description,
            'dimensions': dimensions,
            'occupancy_group': occupancy['group'],
            'occupancy_classification': occupancy['classification'],
            'occupancy_confidence': occupancy['confidence'],
            'matched_keyword': occupancy['trigger_word']
        },
        'design_criteria': jur_data['design_criteria'],
        'permit_checklist': checklist,
        'risk_flags': risks,
        'ahj_contact': {
            'phone': phone.group(1) if phone else 'Not found',
            'url': url.group(1) if url else 'Not found'
        },
        'professional_reviews_required': [],
        'estimated_review_time': '4-6 weeks (standard)'
    }
    
    # Professional review requirements
    if any('SE stamp' in r for r in risks):
        review['professional_reviews_required'].append('Structural Engineer (SE)')
    if any('PE' in r for r in risks) or jur['confidence'] < 90:
        review['professional_reviews_required'].append('Professional Engineer (PE)')
    if occupancy['group'] in ['H', 'I', 'A']:
        review['professional_reviews_required'].append('Fire Protection Engineer')
    if 'flood' in project_description.lower() or 'coastal' in project_description.lower():
        review['professional_reviews_required'].append('Civil Engineer (drainage/flood)')
    
    if occupancy['group'] in ['H', 'I']:
        review['estimated_review_time'] = '8-12 weeks (special occupancy)'
    
    return review

# Test
if __name__ == '__main__':
    # Test warehouse
    result = review_permit_v2('Denver', 'commercial warehouse 100x200', '100x200')
    print('=== WAREHOUSE REVIEW ===')
    print(json.dumps(result, indent=2))
    
    print('\n=== HOSPITAL REVIEW ===')
    result2 = review_permit_v2('Miami', 'hospital 5-story medical center', '200x300')
    print(json.dumps(result2, indent=2))
    
    print('\n=== APARTMENT REVIEW ===')
    result3 = review_permit_v2('Chicago', 'apartment building 12-unit', '75x100')
    print(json.dumps(result3, indent=2))
