from pathlib import Path
import re
import json

base = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

def score_jurisdiction(content, state_code, county_name):
    """Score a single jurisdiction's data confidence from 0-100"""
    score = 0
    factors = []
    
    # Verified URL (30 points)
    if 'verified May 2026' in content:
        score += 30
        factors.append('verified_url')
    elif 'site live - browser access' in content:
        score += 15
        factors.append('blocked_url')
    
    # Phone number present (20 points)
    if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content):
        score += 20
        factors.append('phone_present')
    
    # County seat identified (15 points)
    if 'County Seat:' in content or 'Parish Seat:' in content:
        score += 15
        factors.append('county_seat')
    
    # State building code specified (15 points)
    if 'IBC' in content or 'IRC' in content:
        score += 15
        factors.append('code_reference')
    
    # Design criteria present (10 points)
    if 'Frost:' in content or 'Snow:' in content or 'Wind:' in content:
        score += 10
        factors.append('design_criteria')
    
    # Address present (10 points)
    if re.search(r'\d+\s+[A-Z]', content) and 'St' in content or 'Ave' in content or 'Dr' in content:
        score += 10
        factors.append('address_present')
    
    return score, factors

# Score all jurisdictions
results = {'high': [], 'medium': [], 'low': [], 'per_state': {}}

for state_dir in sorted(base.iterdir()):
    if state_dir.is_dir() and len(state_dir.name) == 2 and state_dir.name.isalpha():
        st = state_dir.name.upper()
        state_scores = []
        
        for county_dir in sorted(state_dir.iterdir()):
            if county_dir.is_dir() and county_dir.name not in ('state', '__pycache__'):
                bc_file = county_dir / 'building_code.md'
                if bc_file.exists():
                    content = bc_file.read_text(encoding='utf-8')
                    score, factors = score_jurisdiction(content, st, county_dir.name)
                    
                    entry = {
                        'jurisdiction': f'{st}/{county_dir.name}',
                        'score': score,
                        'factors': factors
                    }
                    
                    if score >= 90:
                        results['high'].append(entry)
                    elif score >= 60:
                        results['medium'].append(entry)
                    else:
                        results['low'].append(entry)
                    
                    state_scores.append(score)
        
        if state_scores:
            results['per_state'][st] = {
                'counties': len(state_scores),
                'avg_score': sum(state_scores) / len(state_scores),
                'max_score': max(state_scores),
                'min_score': min(state_scores),
                'high': sum(1 for s in state_scores if s >= 90),
                'medium': sum(1 for s in state_scores if 60 <= s < 90),
                'low': sum(1 for s in state_scores if s < 60)
            }

# Print confidence report
print('=' * 60)
print('JURISDICTION CONFIDENCE SCORING REPORT')
print('=' * 60)
print(f'High Confidence (90+): {len(results["high"])} jurisdictions')
print(f'Medium Confidence (60-89): {len(results["medium"])} jurisdictions')
print(f'Low Confidence (<60): {len(results["low"])} jurisdictions')
print(f'Overall: {len(results["high"]) + len(results["medium"]) + len(results["low"])} total')

print(f'\n--- TOP 10 HIGHEST CONFIDENCE ---')
for entry in sorted(results['high'], key=lambda x: x['score'], reverse=True)[:10]:
    print(f'{entry["jurisdiction"]}: {entry["score"]}%')

print(f'\n--- TOP 10 NEEDING IMPROVEMENT ---')
for entry in sorted(results['low'], key=lambda x: x['score'])[:10]:
    print(f'{entry["jurisdiction"]}: {entry["score"]}% - missing: {entry["factors"]}')

print(f'\n--- STATE AVERAGES ---')
for st in sorted(results['per_state'].keys()):
    data = results['per_state'][st]
    bar = '█' * int(data['avg_score'] / 2) + '░' * (50 - int(data['avg_score'] / 2))
    print(f'{st}: {data["avg_score"]:.0f}% avg | H:{data["high"]} M:{data["medium"]} L:{data["low"]} {bar}')

# Save report
report_path = Path(r'C:\Users\greg\dev\clawpack_v2\confidence_scores.json')
with open(report_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f'\nDetailed scores saved to: {report_path}')
