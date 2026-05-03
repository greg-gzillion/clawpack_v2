from pathlib import Path
import re
import json

base = Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\draftclaw\jurisdictions\us')

report = {
    'total_states': 0,
    'total_counties': 0,
    'total_files': 0,
    'missing_counties': [],
    'malformed_files': [],
    'missing_state_resources': [],
    'duplicate_counties': [],
    'empty_files': [],
    'invalid_urls': [],
    'missing_phones': [],
    'unverified_urls': 0,
    'verified_urls': 0,
    'per_state': {}
}

for state_dir in sorted(base.iterdir()):
    if state_dir.is_dir() and len(state_dir.name) == 2 and state_dir.name.isalpha():
        st = state_dir.name.upper()
        report['total_states'] += 1
        state_data = {'counties': 0, 'with_bc': 0, 'verified': 0, 'unverified': 0, 'issues': []}
        
        # Check state folder
        state_folder = state_dir / 'state'
        if not state_folder.exists():
            state_data['issues'].append('Missing state folder')
        else:
            state_bc = state_folder / 'building_code.md'
            if not state_bc.exists():
                report['missing_state_resources'].append(st)
                state_data['issues'].append('Missing state building_code.md')
        
        # Check each county
        for county_dir in sorted(state_dir.iterdir()):
            if county_dir.is_dir() and county_dir.name not in ('state', '__pycache__') and not county_dir.name.startswith('.'):
                state_data['counties'] += 1
                report['total_counties'] += 1
                bc_file = county_dir / 'building_code.md'
                
                if not bc_file.exists():
                    report['missing_counties'].append(f'{st}/{county_dir.name}')
                    state_data['issues'].append(f'Missing: {county_dir.name}')
                    continue
                
                report['total_files'] += 1
                state_data['with_bc'] += 1
                content = bc_file.read_text(encoding='utf-8')
                
                # Check empty
                if len(content.strip()) < 50:
                    report['empty_files'].append(f'{st}/{county_dir.name}')
                    state_data['issues'].append(f'Empty: {county_dir.name}')
                
                # Check for verified URL
                if 'verified May 2026' in content:
                    state_data['verified'] += 1
                    report['verified_urls'] += 1
                elif 'No verified website found' in content or 'verify locally' in content.lower():
                    state_data['unverified'] += 1
                    report['unverified_urls'] += 1
                
                # Check phone number
                if not re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', content):
                    report['missing_phones'].append(f'{st}/{county_dir.name}')
                
                # Check for malformed markdown
                if content.count('#') < 1:
                    report['malformed_files'].append(f'{st}/{county_dir.name}')
        
        report['per_state'][st] = state_data

# Check for duplicate county names within states
for state_dir in sorted(base.iterdir()):
    if state_dir.is_dir() and len(state_dir.name) == 2:
        counties = [d.name for d in state_dir.iterdir() if d.is_dir() and d.name not in ('state', '__pycache__')]
        seen = set()
        for c in counties:
            if c in seen:
                report['duplicate_counties'].append(f'{state_dir.name.upper()}/{c}')
            seen.add(c)

# Print summary
print('=' * 60)
print('JURISDICTION DATABASE AUDIT REPORT')
print('=' * 60)
print(f'Total States: {report["total_states"]}')
print(f'Total Counties: {report["total_counties"]}')
print(f'Total building_code.md files: {report["total_files"]}')
print(f'Verified URLs: {report["verified_urls"]}')
print(f'Unverified URLs: {report["unverified_urls"]}')
print(f'Coverage: {report["total_files"]}/{report["total_counties"]} ({report["total_files"]*100//report["total_counties"]}%)')

print(f'\n--- CRITICAL ISSUES ---')
print(f'Missing Counties: {len(report["missing_counties"])}')
if report['missing_counties']:
    for m in report['missing_counties'][:10]: print(f'  {m}')
    if len(report['missing_counties']) > 10: print(f'  ... and {len(report["missing_counties"])-10} more')

print(f'Missing State Resources: {len(report["missing_state_resources"])}')
for m in report['missing_state_resources']: print(f'  {m}')

print(f'Empty Files: {len(report["empty_files"])}')
for m in report['empty_files'][:5]: print(f'  {m}')

print(f'Malformed Files: {len(report["malformed_files"])}')
for m in report['malformed_files'][:5]: print(f'  {m}')

print(f'Missing Phone Numbers: {len(report["missing_phones"])}')

print(f'\n--- PER STATE SUMMARY ---')
for st, data in sorted(report['per_state'].items()):
    pct = f'{data["with_bc"]*100//data["counties"]}%' if data['counties'] > 0 else 'N/A'
    issues = f' ({len(data["issues"])} issues)' if data['issues'] else ''
    print(f'{st}: {data["with_bc"]}/{data["counties"]} ({pct}) V:{data["verified"]} U:{data["unverified"]}{issues}')

# Save detailed report
report_path = Path(r'C:\Users\greg\dev\clawpack_v2\audit_jurisdictions_report.json')
report_path.write_text(json.dumps(report, indent=2))
print(f'\nDetailed report saved to: {report_path}')
