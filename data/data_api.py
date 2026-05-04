import sqlite3
import json
from pathlib import Path

DB_PATH = Path(r"C:\Users\greg\dev\clawpack_v2\data\chronicle.db")

def query_building_codes(state=None, city=None, county=None):
    """Query building codes from chronicle. Returns list of dicts with attribution."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    
    conditions = ["json_extract(metadata, '$.level') = 'city'"]
    params = []
    
    if state:
        conditions.append("json_extract(metadata, '$.state') LIKE ?")
        params.append(f"%{state.upper()}%")
    if city:
        conditions.append("json_extract(metadata, '$.city') LIKE ?")
        params.append(f"%{city}%")
    if county:
        conditions.append("json_extract(metadata, '$.county') LIKE ?")
        params.append(f"%{county}%")
    
    where = " AND ".join(conditions)
    rows = db.execute(f"SELECT url, context, metadata FROM chronicle WHERE {where} LIMIT 20", params).fetchall()
    
    results = []
    for row in rows:
        meta = json.loads(row['metadata']) if isinstance(row['metadata'], str) else {}
        # Extract design criteria from context
        criteria = {}
        for line in row['context'].split('\n'):
            line_stripped = line.strip()
            if 'Frost:' in line_stripped and '##' in line_stripped:
                val = line_stripped.split('Frost:')[1].strip()
                if '|' in val:
                    val = val.split('|')[0].strip()
                criteria['frost_depth'] = val
            if 'Snow:' in line_stripped and 'psf' in line_stripped and '##' in line_stripped:
                val = line_stripped.split('Snow:')[1].strip()
                if '|' in val:
                    val = val.split('|')[0].strip()
                criteria['snow_load'] = val
            if 'Wind:' in line_stripped and 'mph' in line_stripped and '##' in line_stripped:
                val = line_stripped.split('Wind:')[1].strip()
                if '|' in val:
                    val = val.split('|')[0].strip()
                criteria['wind_speed'] = val
            if 'Seismic:' in line_stripped and '##' in line_stripped:
                val = line_stripped.split('Seismic:')[1].strip()
                if '|' in val:
                    val = val.split('|')[0].strip()
                criteria['seismic'] = val
        
        results.append({
            "jurisdiction": {
                "city": meta.get('city'),
                "county": meta.get('county'),
                "state": meta.get('state')
            },
            "design_criteria": criteria,
            "source_url": row['url']
        })
    
    db.close()
    return results

def query_design_resources(state=None, city=None):
    """Query design resources."""
    if not state:
        return []
    
    design_path = Path(r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\designclaw\jurisdictions\us") / state.lower() / "design_resources"
    if not design_path.exists():
        return []
    
    results = []
    state_file = design_path / "design_resources.md"
    if state_file.exists():
        results.append({
            "level": "state",
            "jurisdiction": state.upper(),
            "content": state_file.read_text(encoding="utf-8")[:1000]
        })
    
    if city:
        city_file = design_path / city / "design_resources.md"
        if city_file.exists():
            results.append({
                "level": "city",
                "jurisdiction": f"{city}, {state.upper()}",
                "content": city_file.read_text(encoding="utf-8")[:1000]
            })
    
    return results

def data_response(data, query_params):
    """Wrap data with attribution metadata."""
    return {
        "data": data,
        "source": "Clawpack V2 Jurisdictional Dataset",
        "license": "CC BY 4.0",
        "doi": "10.5281/zenodo.19713157",
        "version": "3.1.0",
        "query": query_params,
        "attribution": "Data sourced from Clawpack V2 Jurisdictional Dataset (github.com/greg-gzillion/clawpack_v2), used under CC BY 4.0."
    }
