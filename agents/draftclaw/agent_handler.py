"""A2A Handler for DraftClaw v5 - Constitutional Technical Drawing Agent"""
import sys, os, json, re, datetime
from pathlib import Path

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))

from shared.base_agent import BaseAgent
from references import search_references
from core.jurisdiction_engine import lookup_jurisdiction, extract_design_criteria, extract_contact, classify_occupancy

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("draftclaw")

    def _fileclaw_export(self, fmt, content):
        try:
            safe = content.replace(chr(10), '\\n').replace('"', '\\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe}", timeout=30)
            if result: return result
        except: pass
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"draftclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved: {fn.name}"

    def _resolve_jurisdiction(self, query):
        """Extract jurisdiction from query and look up design criteria."""
        # Try to find jurisdiction name in query
        jur_match = re.search(r'(?:in|for|at)\s+([a-zA-Z\s,]+?)(?:\s*$)', query.lower())
        if jur_match:
            jur_name = jur_match.group(1).strip().rstrip(",").strip()
            results = lookup_jurisdiction(jur_name)
            if results:
                jur = results[0]
                criteria = extract_design_criteria(jur['content'])
                contact = extract_contact(jur['content'])
                return {
                    'name': jur['jurisdiction'],
                    'confidence': jur['confidence'],
                    'criteria': criteria,
                    'contact': contact
                }
        # Fallback: default values
        return {
            'name': 'default (verify with AHJ)',
            'confidence': 0,
            'criteria': {'frost_depth': '36 in', 'snow_load': '30 psf', 'wind_speed': '115 mph', 'seismic': 'SDC B'},
            'contact': {}
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
            lines.append(f"- **AHJ URL:** {jur_data['contact']['url']}")
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
                result = "DraftClaw v5 - Constitutional Technical Drawing Agent\n  /permit <project> [jurisdiction]  /structural <project> [jurisdiction]  /blueprint /floorplan <specs>  /cad /schematic <specs>\n  /circuit /wiring <design>  /specs <project>\n  /lookup <jurisdiction> - Search jurisdiction database\n  SHARED: /shared read|write  DELEGATE: /delegate <agent> <task>\n  /stats"
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
                if results:
                    jur = results[0]
                    criteria = extract_design_criteria(jur['content'])
                    contact = extract_contact(jur['content'])
                    lines = [
                        f"## Jurisdiction: {jur['jurisdiction']}",
                        f"**Confidence:** {jur['confidence']}%",
                        f"**Design Criteria:** {json.dumps(criteria, indent=2)}",
                        f"**AHJ Contact:** {json.dumps(contact, indent=2)}",
                    ]
                    result = chr(10).join(lines)
                else:
                    result = f"No jurisdiction found for: {query}"
                return {"status":"success","result":result}

            refs = search_references(query, self.call_agent) if query else ""

            if cmd in ("/permit","/compliance") and query:
                jur_data = self._resolve_jurisdiction(query)
                
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

                prompt = f"Generate a permit application compliance package for: {query}\n\nInclude:\n1. Jurisdiction: {jur_data['name']}\n2. Applicable Codes: {codes}\n3. Occupancy classification per IBC Chapter 3\n4. Construction type per IBC Chapter 6\n5. Fire separation requirements per IBC Chapter 7\n6. Egress calculations per IBC Chapter 10\n7. Accessibility requirements per ADA 2010\n8. Permit submission checklist\n9. Required stamped drawings list\n10. AHJ review notes\n\nCite specific code sections."
                if refs: prompt = f"Reference codes:\n{refs[:3000]}\n\n{prompt}"
                
                result = self.ask_llm(prompt)
                result += f"\n\n---\n## Permit Package Control\n| Field | Value |\n|-------|-------|\n| **Generated** | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |\n| **Jurisdiction** | {jur_data['name']} |\n| **Governing Codes** | {codes} |\n| **Agent** | DraftClaw v5 Constitutional |\n| **Disclaimer** | For preliminary submittal only. Verify with local AHJ. Requires PE/SE stamp. |\n\n*NOT FOR CONSTRUCTION*"

            elif cmd in ("/structural","/engineering") and query:
                jur_data = self._resolve_jurisdiction(query)
                c = jur_data['criteria']
                nl = chr(10)
                
                prompt = f"Generate a PE/SE stamp-ready structural engineering package for: {query}{nl}{nl}Jurisdiction: {jur_data['name']}{nl}{nl}Include detailed calculations and schedules for:{nl}1. Foundation Design: footing sizes, frost depth: {c.get('frost_depth','verify')}, soil bearing (verify w/ geotech), anchor bolt schedule per ACI 318{nl}2. Column Schedule: sizes, spacing, base plates, axial loads per AISC 360{nl}3. Beam/Rafter Schedule: member sizes, moment capacity, deflection checks per AISC 360{nl}4. Lateral System: wind bracing design for {c.get('wind_speed','verify')}, seismic per {c.get('seismic','verify')} (ASCE 7 Ch 11-12){nl}5. Roof Framing: joist spacing, deck gauge, live load 20 psf, ground snow {c.get('snow_load','verify')}, drift per ASCE 7 Ch 7{nl}6. Slab-on-Grade: thickness, reinforcement, joint spacing per ACI 360R{nl}7. Connection Details per AISC 360 Ch J{nl}8. Load Combinations per ASCE 7 Section 2.3 (LRFD){nl}{nl}Format as construction-ready schedules. WARNING: Requires review and stamp by licensed PE/SE."
                
                if refs: prompt = f"Reference codes:{nl}{refs[:3000]}{nl}{nl}{prompt}"
                
                result = self.ask_llm(prompt)
                result += f"{nl}{nl}---{nl}## Structural Package Control{nl}| Field | Value |{nl}|-------|-------|{nl}| **Generated** | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |{nl}| **Jurisdiction** | {jur_data['name']} |{nl}| **Design Criteria** | Frost: {c.get('frost_depth','N/A')} | Snow: {c.get('snow_load','N/A')} | Wind: {c.get('wind_speed','N/A')} | Seismic: {c.get('seismic','N/A')} |{nl}| **WARNING** | REQUIRES PE/SE STAMP PRIOR TO CONSTRUCTION |{nl}{nl}*NOT FOR CONSTRUCTION*"

            elif cmd in ("/blueprint","/floorplan") and query:
                prompt = f"Generate detailed architectural blueprint specifications with dimensions, room layouts, wall placements, door/window locations, and structural notes.\n\nProject: {query}"
                if refs: prompt = f"Reference material:\n{refs[:3000]}\n\n{prompt}"
                result = self.ask_llm(prompt)
                try:
                    from agents.draftclaw.commands.blueprint import run
                    pil_result = run(query)
                    if pil_result and "Error" not in str(pil_result):
                        export = self._fileclaw_export("png", str(pil_result))
                        result = f"{export}\n\n{result}"
                except: pass

            elif cmd in ("/cad","/schematic") and query:
                prompt = f"Generate a technical schematic with precise measurements, component layout, and connection points. Format as ASCII art diagram.\n\nSpecs: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)

            elif cmd in ("/circuit","/wiring") and query:
                prompt = f"Create a circuit/wiring diagram with components labeled, connections shown, and specifications listed. Use ASCII art.\n\nDesign: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)

            elif cmd in ("/specs","/specifications") and query:
                prompt = f"Generate detailed technical specifications with dimensions, materials, tolerances, and assembly notes.\n\nProject: {query}"
                if refs: prompt = f"Reference material:\n{refs[:2000]}\n\n{prompt}"
                result = self.ask_llm(prompt)

            elif cmd=="/export" and args:
                parts2 = args.split(maxsplit=1)
                result = self._fileclaw_export(parts2[0], parts2[1]) if len(parts2)==2 else "Usage: /export <format> <content>"

            elif query:
                specs = self.ask_llm(f"Generate technical drawing specifications with dimensions for: {query}")
                result = f"Specifications generated. Use /blueprint to render.\n\n{specs}"
            else:
                result = "Type /help for commands"

            from data_io import write_shared
            write_shared("draftclaw_latest", {"command":cmd,"query":query})

            return {"status":"success","result":str(result)}
        except Exception as e:
            return {"status":"error","result":str(e)}

_agent = DraftClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)