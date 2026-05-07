import pathlib, re
MN = pathlib.Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\MN')

count = 0
for county_dir in MN.iterdir():
    if not county_dir.is_dir() or county_dir.name == 'state':
        continue
    for city_dir in county_dir.iterdir():
        if not city_dir.is_dir():
            continue
        law_file = city_dir / 'law_resources.md'
        court_file = city_dir / 'municipal_court.md'
        if not law_file.exists():
            continue
        content = law_file.read_text(encoding='utf-8')
        # Extract court section
        court_match = re.search(r'## Courts\n(.+?)(?=\n## |$)', content, re.DOTALL)
        city_match = re.search(r'## City Website\n(.+?)(?=\n## |$)', content, re.DOTALL)
        
        court_info = court_match.group(1).strip() if court_match else "County District Court"
        city_url = city_match.group(1).strip() if city_match else ""
        
        court_file.write_text(f"""# {city_dir.name.replace('_', ' ')} Municipal Court
## Court Information
{court_info}
## City Website
{city_url}
""", encoding='utf-8')
        count += 1

print(f"MN municipal_court.md files created: {count}")
