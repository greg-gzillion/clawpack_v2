"""A2A Handler for DraftClaw v5 - Constitutional Technical Drawing Agent"""
import sys, os, json, re, datetime, webbrowser
from pathlib import Path

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))

from shared.base_agent import BaseAgent
from shared.truth_resolver import merge_with_retriever
from references import search_references
from agents.draftclaw.core.jurisdiction_engine import lookup_jurisdiction, extract_design_criteria, extract_contact, classify_occupancy

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("draftclaw")

    def _log_error(self, context, error):
        """Safe error logger."""
        try:
            print(f"[draftclaw] {context}: {error}", flush=True)
        except:
            pass

    def _filter_fake_engineering(self, text):
        """Replace inference-tier structural values with DESIGN REQUIRED placeholders."""
        import re
        patterns = [
            (r'(\d{1,2})"?\s*[xX]\s*(\d{1,2})"?\s*(?:column|beam|footing|member|base\s*plate|rafter)', r'[DESIGN REQUIRED]'),
            (r'W(\d{1,2})[xX](\d{2,3})', r'[DESIGN REQUIRED - W-section]'),
            (r'(\d{2,4})\s*kip[sS]?[-\s]*(?:ft|feet)?', r'[DESIGN REQUIRED - load]'),
            (r'(\d{3,5})\s*psf', r'[DESIGN REQUIRED - capacity]'),
            (r'#\s*(\d{1,2})\s*(?:rebar|bar|@)', r'[DESIGN REQUIRED - rebar]'),
            (r'(\d{1,2})"?\s*(?:thick|slab|concrete)', r'[DESIGN REQUIRED - thickness]'),
        ]
        for pattern, replacement in patterns:
            text = re.sub(r'(?<!DESIGN REQUIRED - )' + pattern, replacement, text, flags=re.IGNORECASE)
        return text



    def _open_ahj_url(self, jur_data):
        """Auto-open AHJ website if URL is available"""
        url = jur_data.get('contact', {}).get('url')
        if url:
            try:
                webbrowser.open(url)
            except:
                pass



    def _open_ahj_url(self, jur_data):
        """Auto-open AHJ website if URL is available"""
        url = jur_data.get('contact', {}).get('url')
        if url:
            try:
                webbrowser.open(url)
            except:
                pass


    def _fileclaw_export(self, fmt, content):
        try:
            safe = content.replace(chr(10), '\\n').replace('"', '\\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe}", timeout=30)
            if result: return result
        except Exception as e:
                    self.log(f"Silent exception caught: {e}")
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"draftclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved: {fn.name}"

    def _resolve_jurisdiction(self, query):
        """Extract jurisdiction from query and look up design criteria.
        ALL criteria MUST come from webclaw/references/draftclaw/jurisdictions/us/
        No hardcoded fallback values permitted."""
        from agents.draftclaw.core.jurisdiction_engine import lookup_jurisdiction, extract_design_criteria, extract_contact

        # Extract city/state name from query
        jur_match = re.search(r'(?:in|for|at)\s+([a-zA-Z\s,]+?)(?:\s*$)', query.lower())
        jur_names = []
        if jur_match:
            full = jur_match.group(1).strip().rstrip(",").strip().replace(",", " ")
            words = full.split()
            jur_names = [full] + words + [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        else:
            words = query.lower().replace(",", " ").split()
            skip = {'warehouse','building','structural','permit','commercial','retail','industrial','office','with','and','for','the'}
            words = [w for w in words if w not in skip]
            if len(words) >= 2:
                jur_names = [' '.join(words[-3:]), ' '.join(words[-2:]), words[-1]]
            elif len(words) == 1:
                # Single word query - just use it directly
                jur_names = [words[0]]

        # Try each candidate, prioritizing city-level matches
        best = None
        for name in jur_names:
            if len(name) < 3:
                continue
            results = lookup_jurisdiction(name)
            for jur in results:
                effective_conf = jur['confidence']
                if jur.get('source') == 'city':
                    effective_conf += 20
                if best is None or effective_conf > best['confidence']:
                    jur['confidence'] = effective_conf
                    best = jur

        if best:
            criteria = extract_design_criteria(best['content'])
            contact = extract_contact(best['content'])
            result = {
                'name': best['jurisdiction'],
                'confidence': best['confidence'],
                'criteria': criteria,
                'contact': contact,
                'source': best.get('source', 'unknown')
            }
            # Constitutional: run through truth resolver (Article V)
            try:
                from shared.truth_resolver import merge_with_retriever
                result = merge_with_retriever(result, source='chronicle')
            except:
                pass
            return result

        # NO FALLBACK - all criteria must come from webclaw/references/
        return {
            'name': 'UNRESOLVED',
            'confidence': 0,
            'criteria': {},
            'contact': {},
            'source': 'none',
            'error': 'No building code reference found. Try: /lookup <city state>'
        }

    def _geo_text(self, jur_data):
        """Build jurisdiction-specific design assumptions text from looked-up data."""
        c = jur_data['criteria']
        nl = chr(10)
        lines = [
            f"## Jurisdiction-Specific Design Assumptions",
            f"- **Jurisdiction:** {jur_data['name']}",
            f"- **Ground Snow Load:** {c.get('snow_load', 'Verify per ASCE 7')}",
            f"- **Frost Depth:** {c.get('frost_depth', 'Verify per IBC 1809.5')}",
            f"- **Design Wind Speed:** {c.get('wind_speed', 'Verify per ASCE 7 Ch 26')}",
            f"- **Seismic Design Category:** {c.get('seismic', 'Verify per ASCE 7 Ch 11')}",
        ]
        if jur_data['confidence'] < 60:
            lines.append(f"- **WARNING:** Low jurisdiction data confidence ({jur_data['confidence']}%). Verify all criteria with AHJ.")
        if jur_data['contact'].get('phone'):
            lines.append(f"- **AHJ Phone:** {jur_data['contact']['phone']}")
        if jur_data['contact'].get('url'):
            ahj_url = jur_data['contact']['url']
            lines.append(f"- **AHJ URL:** [{ahj_url}]({ahj_url})")
        return nl + nl + nl.join(lines) + nl

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            q = validated["payload"].get("query","")
            result = self.ask_llm(f"Generate technical drawing specifications with dimensions for: {q}")
            return {"status":"success","result":str(result)}

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "DraftClaw v5 - Constitutional Technical Drawing Agent\n  /permit <project> [jurisdiction]  /structural <project> [jurisdiction]  /blueprint /floorplan <specs>  /cad /schematic <specs>\n  /circuit /wiring <design>  /specs <project>\n  /lookup <jurisdiction> - Search jurisdiction database\n  /correct <id> <field> <value> - Community edit (3 confirmations = consensus)\n  /correct <id> <field> <value> - Community edit (3 confirmations = consensus)\n  SHARED: /shared read|write  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}
            if cmd in ("/stats",): return {"status":"success","result":f"DraftClaw v5 | Blueprints+CAD+Circuits | Interactions: {self.state.get('interactions',0)}"}

            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}

            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","docuclaw","interpretclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            # /lookup command - search jurisdiction database
            if cmd in ("/lookup","/jurisdiction") and query:
                results = lookup_jurisdiction(query)
                # Sort: city matches first, then by confidence
                city_results = [r for r in results if r.get('source') == 'city']
                county_results = [r for r in results if r.get('source') != 'city']
                results = city_results + county_results
                # Boost results matching state in query
                import re
                state_match = re.search(r'\b([A-Z]{2})\b', query.upper())
                if state_match:
                    st = state_match.group(1)
                    for r in results:
                        if st in r.get('jurisdiction', ''):
                            r['confidence'] = r.get('confidence', 50) + 30
                    results.sort(key=lambda r: -r.get('confidence', 0))
                if results:
                    jur = results[0]
                    criteria = extract_design_criteria(jur['content'])
                    contact = extract_contact(jur['content'])
                    ahj_name = contact.get('ahj', 'Verify with AHJ')
                    ahj_phone = contact.get('phone', 'N/A')
                    ahj_url = contact.get('url', '')
                    ahj_addr = contact.get('address', '')
                    url_link = f'[{ahj_url}]({ahj_url})' if ahj_url else 'N/A'
                    lines = [
                        f"## Jurisdiction: {jur['jurisdiction']}",
                        f"**Confidence:** {jur['confidence']}%",
                        f"**AHJ:** {ahj_name}",
                        f"**Phone:** {ahj_phone}",
                        f"**URL:** {url_link}",
                        f"**Address:** {ahj_addr}",
                        f"**Design Criteria:**",
                        f"- Frost Depth: {criteria.get('frost_depth', 'N/A')}",
                        f"- Snow Load: {criteria.get('snow_load', 'N/A')}",
                        f"- Wind Speed: {criteria.get('wind_speed', 'N/A')}",
                        f"- Seismic: {criteria.get('seismic', 'N/A')}",
                    ]
                    result = chr(10).join(lines)
                    # Auto-open AHJ website in browser
                    if contact.get('url'):
                        try:
                            webbrowser.open(contact['url'])
                        except:
                            pass
                else:
                    result = f"No jurisdiction found for: {query}"
                return {"status":"success","result":result}

            # /correct command - community editing of jurisdiction data
            if cmd == "/correct" and args:
                parts2 = args.split(maxsplit=2)
                if len(parts2) >= 2:
                    import sqlite3, hashlib
                    jurisdiction_id = parts2[0]
                    field = parts2[1]
                    new_value = parts2[2] if len(parts2) > 2 else ""
                    
                    db_path = "C:/Users/greg/dev/clawpack_v2/data/chronicle.db"
                    db = sqlite3.connect(db_path)
                    pct = chr(37)
                    entry = db.execute(
                        "SELECT id, context, update_count, original_hash FROM chronicle WHERE (url LIKE ? OR json_extract(metadata, '$.city') LIKE ?) AND json_extract(metadata, '$.level') = 'city'",
                        (pct + jurisdiction_id + pct, pct + jurisdiction_id + pct)
                    ).fetchone()
                    
                    if not entry:
                        db.close()
                        return {"status":"error","result":"Jurisdiction not found: " + jurisdiction_id}
                    
                    entry_id, current_context, update_count, original_hash = entry
                    
                    if not original_hash:
                        original_hash = hashlib.sha256(current_context.encode()).hexdigest()
                    
                    # Simple string replacement - find line starting with "## Field:"
                    field_prefix = "## " + field + ":"
                    new_lines = []
                    found = False
                    for line in current_context.split(chr(10)):
                        if line.startswith(field_prefix):
                            new_lines.append("## " + field + ": " + new_value)
                            found = True
                        else:
                            new_lines.append(line)
                    if not found:
                        new_lines.append("## " + field + ": " + new_value)
                    new_context = chr(10).join(new_lines)
                    
                    from datetime import datetime, timezone
                    now = datetime.now(timezone.utc).isoformat()
                    update_count = (update_count or 0) + 1
                    
                    db.execute(
                        "UPDATE chronicle SET context=?, update_count=?, updated_by='user', timestamp=?, original_hash=COALESCE(original_hash,?) WHERE id=?",
                        (new_context, update_count, now, original_hash, entry_id)
                    )
                    db.commit()
                    
                    if update_count >= 3:
                        db.execute("UPDATE chronicle SET verified_by='consensus', verified_at=? WHERE id=?", (now, entry_id))
                        db.commit()
                        consensus = " | Consensus reached"
                    else:
                        consensus = " | " + str(3 - update_count) + " more confirmations needed"
                    
                    db.close()
                    result = "Updated: " + field + " = " + new_value + " | Jurisdiction: " + jurisdiction_id + " | Edit: " + str(update_count) + consensus
                else:
                    result = "Usage: /correct <jurisdiction_id> <field> <new_value>"
                return {"status":"success","result":result}

            refs = search_references(query, self.call_agent) if query else ""

            if cmd in ("/permit","/compliance") and query:
                jur_data = self._resolve_jurisdiction(query)
                
                # REFUSE if jurisdiction unresolved
                if jur_data.get("name") == "UNRESOLVED" or jur_data.get("error"):
                    result = "**ERROR: Jurisdiction not found.**\n\n"
                    result += "No building code reference matched your query.\n"
                    result += "Try: /lookup CITY STATE to find a jurisdiction.\n\n"
                    result += f"Query: {query}\n"
                    return {"status":"error","result":result}
                
                code_refs = {
                    "default": "IBC 2021, IRC 2021, NEC 2023",
                    "california": "CBC 2022 (Title 24), CRC 2022, CEC 2022",
                    "florida": "FBC 2020 (HVHZ where applicable)",
                    "texas": "IBC 2021 (TDLR amendments)",
                    "new york": "IBC 2021 (NYS amendments)",
                }
                codes = code_refs.get("default", code_refs["default"])
                for key in code_refs:
                    if key in jur_data['name'].lower():
                        codes = code_refs[key]
                        break

                # Auto-open AHJ website
                if jur_data.get('contact', {}).get('url'):
                    try:
                        webbrowser.open(jur_data['contact']['url'])
                    except:
                        pass
                
                prompt = f"Generate a permit application compliance package for: {query}\n\nInclude:\n1. Jurisdiction: {jur_data['name']}\n2. Applicable Codes: {codes}\n3. Occupancy classification per IBC Chapter 3\n4. Construction type per IBC Chapter 6\n5. Fire separation requirements per IBC Chapter 7\n6. Egress calculations per IBC Chapter 10\n7. Accessibility requirements per ADA 2010\n8. Permit submission checklist\n9. Required stamped drawings list\n10. AHJ review notes\n\nCite specific code sections."
                if refs: prompt = f"Reference codes:\n{refs[:3000]}\n\n{prompt}"
                
                result = self._filter_fake_engineering(self.ask_llm(prompt))
                result += f"\n\n---\n## Permit Package Control\n| Field | Value |\n|-------|-------|\n| **Generated** | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |\n| **Jurisdiction** | {jur_data['name']} |\n| **Governing Codes** | {codes} |\n| **Agent** | DraftClaw v5 Constitutional |\n| **Disclaimer** | For preliminary submittal only. Verify with local AHJ. Requires PE/SE stamp. |\n\n*NOT FOR CONSTRUCTION*"

            elif cmd in ("/structural","/engineering") and query:
                jur_data = self._resolve_jurisdiction(query)
                
                # REFUSE if jurisdiction unresolved
                if jur_data.get("name") == "UNRESOLVED" or jur_data.get("error"):
                    result = "**ERROR: Jurisdiction not found.**\n\n"
                    result += "No building code reference matched your query.\n"
                    result += "Try: /lookup CITY STATE to find a jurisdiction.\n\n"
                    result += f"Query: {query}\n"
                    return {"status":"error","result":result}
                
                c = jur_data['criteria']
                nl = chr(10)
                
                prompt = f"Generate a structural engineering CONCEPTUAL PACKAGE for: {query}{nl}{nl}Jurisdiction: {jur_data['name']}{nl}Source: Chronicle (building_code.md){nl}{nl}## LOCKED DESIGN CRITERIA (Chronicle - DO NOT CHANGE){nl}- Frost Depth: {c.get('frost_depth','VERIFY')}{nl}- Ground Snow Load: {c.get('snow_load','VERIFY')}{nl}- Design Wind Speed: {c.get('wind_speed','VERIFY')}{nl}- Seismic Design Category: {c.get('seismic','VERIFY')}{nl}{nl}## STRUCTURAL SYSTEM DESCRIPTION (Conceptual Only){nl}Describe the appropriate structural system for this project. DO NOT specify member sizes, dimensions, or capacities.{nl}{nl}## REQUIRED DELEGATIONS (For Actual Design){nl}This package must be completed by:{nl}- Mathematicaclaw: load combinations per ASCE 7, tributary areas, frame analysis{nl}- Dataclaw: material selection, section properties{nl}- Licensed PE/SE: final review and stamp{nl}{nl}## RULES{nl}- DO NOT generate any numerical structural values (sizes, loads, capacities){nl}- DO NOT specify member sections (W-shapes, HSS, etc.){nl}- DO NOT design connections, footings, or reinforcement{nl}- Mark all design-dependent items as [ANALYSIS REQUIRED]{nl}- This is a CONCEPTUAL package only - NOT FOR CONSTRUCTION"
                
                if refs: prompt = f"Reference codes:{nl}{refs[:3000]}{nl}{nl}{prompt}"
                
                result = self._filter_fake_engineering(self.ask_llm(prompt))
                # Auto-open AHJ website if URL found
                if jur_data.get('contact', {}).get('url'):
                    try:
                        webbrowser.open(jur_data['contact']['url'])
                    except:
                        pass
                result += f"{nl}{nl}---{nl}## Structural Package Control{nl}| Field | Value |{nl}|-------|-------|{nl}| **Generated** | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |{nl}| **Jurisdiction** | {jur_data['name']} |{nl}| **Design Criteria** | Frost: {c.get('frost_depth','N/A')} | Snow: {c.get('snow_load','N/A')} | Wind: {c.get('wind_speed','N/A')} | Seismic: {c.get('seismic','N/A')} |{nl}| **WARNING** | REQUIRES PE/SE STAMP PRIOR TO CONSTRUCTION |{nl}{nl}*NOT FOR CONSTRUCTION*"

            elif cmd in ("/blueprint","/floorplan") and query:
                # Resolve jurisdiction if location mentioned in query
                jur_data = self._resolve_jurisdiction(query)
                if jur_data.get('name') != 'UNRESOLVED':
                    self._open_ahj_url(jur_data)
                
                prompt = f"Generate detailed architectural blueprint specifications with dimensions, room layouts, wall placements, door/window locations, and structural notes.\n\nProject: {query}"
                if refs: prompt = f"Reference material:\n{refs[:3000]}\n\n{prompt}"
                result = self._filter_fake_engineering(self.ask_llm(prompt))
                try:
                    from agents.draftclaw.commands.blueprint import run
                    pil_result = run(query)
                    if pil_result and "Error" not in str(pil_result):
                        export = self._fileclaw_export("png", str(pil_result))
                        result = f"{export}\n\n{result}"
                except Exception as e:
                    result += f" [Blueprint visual: {str(e)[:80]}]"

            elif cmd in ("/cad","/schematic") and query:
                prompt = f"Generate a technical schematic with precise measurements, component layout, and connection points. Format as ASCII art diagram.\n\nSpecs: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self._filter_fake_engineering(self.ask_llm(prompt))

            elif cmd in ("/circuit","/wiring") and query:
                prompt = f"Create a circuit/wiring diagram with components labeled, connections shown, and specifications listed. Use ASCII art.\n\nDesign: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self._filter_fake_engineering(self.ask_llm(prompt))

            elif cmd in ("/specs","/specifications") and query:
                prompt = f"Generate detailed technical specifications with dimensions, materials, tolerances, and assembly notes.\n\nProject: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self._filter_fake_engineering(self.ask_llm(prompt))

            elif cmd=="/export" and args:
                parts2 = args.split(maxsplit=1)
                result = self._fileclaw_export(parts2[0], parts2[1]) if len(parts2)==2 else "Usage: /export <format> <content>"

            elif query:
                specs = self.ask_llm(f"Generate technical drawing specifications with dimensions for: {query}")
                result = f"Specifications generated. Use /blueprint to render.\n\n{specs}"
            else:
                result = "Type /help for commands"

            # Only persist command metadata, not LLM output (Article VI)
            from data_io import write_shared
            write_shared("draftclaw_latest", {
                "command": cmd,
                "query": query,
                "timestamp": datetime.datetime.now().isoformat(),
                "source": "draftclaw"
            })

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

_agent = DraftClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)