# DraftClaw /review Agent - Commercial Plan Check Module
# Targets: PEMB, Warehouse, Auto Shop, Retail Shell, Office TI, Agricultural

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from review_agent_v2 import lookup_jurisdiction, classify_occupancy

# Commercial structure type thresholds and requirements
COMMERCIAL_STRUCTURE_TYPES = {
    'pemb': {
        'name': 'Pre-Engineered Metal Building',
        'occupancy': 'S-1',
        'construction_type': 'IIB',
        'typical_framing': 'Rigid frame / post-and-beam steel',
        'critical_checks': [
            'Foundation design for column reactions (typically 20-50 kips)',
            'Lateral bracing - rod bracing vs portal frame',
            'Roof live load vs snow load (snow drift at parapets)',
            'Wind uplift on metal panels and purlins',
            'Thermal expansion/contraction joints at 200 ft max',
            'Foundation frost depth per jurisdiction',
            'Anchor bolt embedment and edge distance',
            'Girt and purlin span tables per manufacturer',
            'Diaphragm design (roof and wall panels)',
            'Secondary framing attachment to main frames'
        ],
        'common_mistakes': [
            'Missing snow drift calculations at roof steps',
            'Undersized hairpin ties or tie rods',
            'No thermal break at foundation in cold climates',
            'PEMB manufacturer drawings not sealed by local PE',
            'Crane loads not coordinated with PEMB supplier'
        ],
        'seismic_triggers': {'SDC C': 'Special moment frames may be required', 'SDC D': 'R > 3 requires special detailing', 'SDC E': 'PEMB may not be permitted - verify with AHJ'},
        'review_time': '6-8 weeks',
        'estimated_fees': ',500 - ,000',
        'pe_required': True
    },
    'warehouse': {
        'name': 'Warehouse / Distribution Center',
        'occupancy': 'S-1',
        'construction_type': 'IIB or IIIB',
        'typical_framing': 'Tilt-up concrete or steel frame',
        'critical_checks': [
            'Fire area limits (IBC Table 506.2)',
            'Sprinkler system requirement (NFPA 13)',
            'Loading dock design and vehicle impact protection',
            'Floor slab design for racking loads (typically 4,000-6,000 psf point loads)',
            'Egress distances from rear of building',
            'Smoke and heat venting (IBC 910)',
            'Hazardous material storage separation',
            'Truck court and fire access road requirements',
            'ESFR sprinkler system interaction with storage height',
            'Mezzanine area limits (1/3 of floor area below)'
        ],
        'common_mistakes': [
            'Racking loads not specified on structural drawings',
            'Missing dock leveler pit details in foundation',
            'Inadequate fire flow at site (verify with fire marshal)',
            'No early suppression fast response (ESFR) sprinkler coordination',
            'Floor flatness tolerances not specified for VNA trucks'
        ],
        'sprinkler_triggers': {'fire_area': '12,000 sq ft (non-sprinklered)', 'storage_height': '>12 ft triggers ESFR consideration'},
        'review_time': '8-10 weeks',
        'estimated_fees': ',500 - ,500',
        'pe_required': True
    },
    'auto_shop': {
        'name': 'Auto Repair / Service Garage',
        'occupancy': 'S-1 or B',
        'construction_type': 'IIB or VB',
        'typical_framing': 'Steel or wood frame',
        'critical_checks': [
            'Hazardous material containment (oil, solvents, paints)',
            'Floor drains with oil/water separator',
            'Ventilation requirements (IBC 406.6)',
            'Fire separation from adjacent occupancies',
            'Welding area separation and ventilation',
            'Exhaust extraction system for running vehicles',
            'Floor coating for chemical resistance',
            'Parts storage mezzanine structural design',
            'Service pit structural design and ventilation',
            'Waste oil tank containment'
        ],
        'common_mistakes': [
            'Missing oil/water separator in drainage plan',
            'Inadequate ventilation calculated',
            'Floor drain connected to sanitary (must be separate system)',
            'No fire suppression in parts storage room',
            'Welding area not separated with 1-hour fire barrier'
        ],
        'hazmat_triggers': True,
        'review_time': '6-8 weeks',
        'estimated_fees': ',000 - ,000',
        'pe_required': True
    },
    'retail_shell': {
        'name': 'Retail Shell Building',
        'occupancy': 'M',
        'construction_type': 'IIB or VB',
        'typical_framing': 'Steel or CMU/wood',
        'critical_checks': [
            'ADA accessibility (parking, entries, restrooms)',
            'Energy code compliance (COMcheck)',
            'Storefront wind load design',
            'Truss or joist roof structure',
            'RTU curb and roof penetration details',
            'Tenant separation walls (fire rating)',
            'Exterior facade attachment engineering',
            'Signage structural supports',
            'Grease trap provisions (if future restaurant)',
            'Parking lot drainage and ADA stall layout'
        ],
        'common_mistakes': [
            'Missing ADA ramp and landing details',
            'COMcheck submitted for wrong climate zone',
            'No future tenant load allowance on structure',
            'Storefront not engineered for wind load',
            'Missing roof access hatch and ladder'
        ],
        'ada_triggers': True,
        'review_time': '6-8 weeks',
        'estimated_fees': ',000 - ,000',
        'pe_required': 'Depends on scope'
    },
    'office_ti': {
        'name': 'Office Tenant Improvement',
        'occupancy': 'B',
        'construction_type': 'Varies (existing)',
        'typical_framing': 'N/A (interior only)',
        'critical_checks': [
            'Demising wall fire rating (1-hour typical)',
            'ADA path of travel and accessible restrooms',
            'HVAC zoning and duct distribution',
            'Electrical service adequacy for new layout',
            'Exit sign and emergency lighting',
            'Ceiling grid and light fixture support',
            'Data/communications rough-in',
            'Acoustical separation between offices',
            'Sprinkler head relocation for new walls',
            'CO monitoring if attached to parking garage'
        ],
        'common_mistakes': [
            'Existing HVAC not sized for new layout',
            'Missing fire caulking at wall penetrations',
            'Exit path blocked by new walls',
            'Sprinkler coverage deficient after remodel',
            'No accessible route to new break room'
        ],
        'occupancy_change_triggers': 'Verify if change of use triggers full code upgrade',
        'review_time': '3-4 weeks',
        'estimated_fees': ',000 - ,000',
        'pe_required': 'Depends on scope'
    },
    'agricultural': {
        'name': 'Agricultural Building',
        'occupancy': 'U',
        'construction_type': 'VB',
        'typical_framing': 'Wood post-frame or steel',
        'critical_checks': [
            'IBC exempt? (verify with AHJ - many ag buildings exempt)',
            'Wind load on open-front structures',
            'Snow load on low-slope roofs',
            'Foundation frost depth',
            'Manure management and containment',
            'Ventilation for animal housing',
            'Electrical for wet/damp locations',
            'Grain bin foundation and anchoring',
            'Equipment storage floor loading',
            'Fire separation distance from property lines'
        ],
        'common_mistakes': [
            'Assuming all ag buildings are exempt (verify occupancy and use)',
            'Missing wind bracing on open side',
            'Undersized headers over large equipment doors',
            'No vapor barrier under concrete in cold storage',
            'Manure lagoon setback from wells'
        ],
        'exemption_possible': True,
        'review_time': '2-4 weeks',
        'estimated_fees': ' - ,000',
        'pe_required': 'Depends on scope'
    }
}

def review_commercial(jurisdiction_name: str, structure_type: str, dimensions: str = '', project_desc: str = '') -> Dict:
    """Generate commercial plan check review for specific structure types"""
    
    # Lookup jurisdiction
    jurisdictions = lookup_jurisdiction(jurisdiction_name)
    if not jurisdictions:
        return {'error': f'No jurisdiction found for "{jurisdiction_name}"'}
    
    jur = jurisdictions[0]
    content = jur['content']
    
    # Get structure type data
    struct_key = structure_type.lower().replace(' ', '_').replace('-', '_')
    struct_data = COMMERCIAL_STRUCTURE_TYPES.get(struct_key)
    
    if not struct_data:
        # Fuzzy match
        for key, data in COMMERCIAL_STRUCTURE_TYPES.items():
            if struct_key in key or key in struct_key:
                struct_data = data
                break
    
    if not struct_data:
        return {'error': f'Unknown structure type: {structure_type}. Supported: {list(COMMERCIAL_STRUCTURE_TYPES.keys())}'}
    
    # Classify occupancy
    occupancy = classify_occupancy(project_desc if project_desc else struct_data['name'])
    
    # Extract design criteria
    design_criteria = {}
    patterns = {
        'frost_depth': r'Frost[:\s]+(\d+[-\d]*\s*in)',
        'snow_load': r'Snow[:\s]+(\d+[-\d]*\s*psf)',
        'wind_speed': r'Wind[:\s]+(\d+[-\d]*\s*mph)',
        'seismic': r'Seismic[:\s]+(SDC\s*[A-D])'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            design_criteria[key] = match.group(1)
    
    # Generate jurisdiction-specific checks
    jurisdiction_checks = []
    
    # Seismic-specific
    seismic = design_criteria.get('seismic', '')
    if seismic in struct_data.get('seismic_triggers', {}):
        jurisdiction_checks.append({
            'type': 'seismic',
            'severity': 'high',
            'requirement': struct_data['seismic_triggers'][seismic],
            'design_criteria': seismic
        })
    
    # Snow-specific
    snow = design_criteria.get('snow_load', '')
    snow_num = int(re.search(r'(\d+)', snow).group(1)) if re.search(r'(\d+)', snow) else 0
    if snow_num > 40:
        jurisdiction_checks.append({
            'type': 'snow',
            'severity': 'high' if snow_num > 60 else 'medium',
            'requirement': f'Snow load {snow} exceeds 40 psf - roof drift analysis required',
            'design_criteria': snow
        })
    
    # Wind-specific
    wind = design_criteria.get('wind_speed', '')
    wind_num = int(re.search(r'(\d+)', wind).group(1)) if re.search(r'(\d+)', wind) else 0
    if wind_num > 130:
        jurisdiction_checks.append({
            'type': 'wind',
            'severity': 'high',
            'requirement': f'Wind speed {wind} requires missile impact protection (wind-borne debris region)',
            'design_criteria': wind
        })
    
    # Frost-specific
    frost = design_criteria.get('frost_depth', '')
    frost_num = int(re.search(r'(\d+)', frost).group(1)) if re.search(r'(\d+)', frost) else 0
    if frost_num > 42:
        jurisdiction_checks.append({
            'type': 'frost',
            'severity': 'high' if frost_num > 60 else 'medium',
            'requirement': f'Frost depth {frost} - deep foundation required, verify with geotechnical report',
            'design_criteria': frost
        })
    
    # Generate review
    phone = re.search(r'(\(\d{3}\)\s*\d{3}-\d{4})', content)
    url = re.search(r'(https://[^\s\)]+)', content)
    
    review = {
        'project_type': struct_data['name'],
        'jurisdiction': jur['jurisdiction'],
        'confidence_score': jur['confidence'],
        'structure': {
            'type': struct_data['name'],
            'occupancy': struct_data['occupancy'],
            'construction_type': struct_data['construction_type'],
            'typical_framing': struct_data['typical_framing']
        },
        'design_criteria': design_criteria,
        'jurisdiction_specific_checks': jurisdiction_checks,
        'critical_plan_check_items': struct_data['critical_checks'],
        'common_mistakes': struct_data['common_mistakes'],
        'estimated_review_time': struct_data['review_time'],
        'estimated_fees': struct_data['estimated_fees'],
        'pe_required': struct_data['pe_required'],
        'ahj_contact': {
            'phone': phone.group(1) if phone else 'Not found',
            'url': url.group(1) if url else 'Not found'
        }
    }
    
    # Risk flags
    risk_flags = []
    if jur['confidence'] < 60:
        risk_flags.append('🔴 Low jurisdiction data confidence - verify ALL criteria with AHJ')
    if struct_data.get('pe_required') == True:
        risk_flags.append('⚠️ PE stamp required for structural drawings')
    if struct_data.get('sprinkler_triggers'):
        risk_flags.append('⚠️ Verify sprinkler requirements with fire marshal')
    if struct_data.get('hazmat_triggers'):
        risk_flags.append('🔴 Hazardous materials - fire marshal review required')
    if struct_data.get('ada_triggers'):
        risk_flags.append('⚠️ ADA compliance review required')
    if struct_data.get('exemption_possible'):
        risk_flags.append('ℹ️ Verify if structure qualifies for agricultural exemption')
    
    review['risk_flags'] = risk_flags
    
    return review

# Test
if __name__ == '__main__':
    print('=== PEMB WAREHOUSE - DENVER ===')
    result = review_commercial('Denver', 'pemb', '100x200', 'pre-engineered metal building warehouse')
    print(json.dumps(result, indent=2))
    
    print('\n=== AUTO SHOP - PHOENIX ===')
    result2 = review_commercial('Phoenix', 'auto_shop', '60x80', 'auto repair shop 4-bay')
    print(json.dumps(result2, indent=2))
    
    print('\n=== RETAIL SHELL - MIAMI ===')
    result3 = review_commercial('Miami', 'retail_shell', '120x80', 'retail shell building strip mall')
    print(json.dumps(result3, indent=2))
