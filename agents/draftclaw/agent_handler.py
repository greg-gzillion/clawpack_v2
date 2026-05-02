"""A2A Handler for DraftClaw v5 - Constitutional Technical Drawing Agent"""
import sys, os, json
from pathlib import Path
from datetime import datetime

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))

from shared.base_agent import BaseAgent
from references import search_references

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
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"draftclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved: {fn.name}"

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
                result = "DraftClaw v5 - Constitutional Technical Drawing Agent\n  /permit <project> [jurisdiction]  /blueprint /floorplan <specs>  /cad /schematic <specs>\n  /circuit /wiring <design>  /specs <project>\n  SHARED: /shared read|write  DELEGATE: /delegate <agent> <task>\n  /stats"
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

            # Gather references for better specs
            refs = search_references(query, self.call_agent) if query else ""

            if cmd in ("/permit","/compliance") and query:
                import re, datetime
                jurisdiction = "default"
                jur_match = re.search(r'(?:in|for|at)\s+([a-zA-Z\s,]+?)(?:\s*$)', query.lower())
                if jur_match:
                    jurisdiction = jur_match.group(1).strip().rstrip(",").strip()
                
                code_refs = {
                    "default": "IBC 2021, IRC 2021, NEC 2023",
                    "california": "CBC 2022 (Title 24), CRC 2022, CEC 2022",
                    "florida": "FBC 2020 (HVHZ where applicable), IRC 2020",
                    "texas": "IBC 2021 (TDLR amendments), IRC 2021",
                    "new york": "IBC 2021 (NYS amendments), NYC Building Code where applicable",
                    "colorado": "IBC 2021 (state adopted, local amendments may apply)",
                    "denver": "2022 Denver Building Code (IBC 2021 + Denver amendments)",
                    "miami": "FBC 2020 with HVHZ provisions, Miami-Dade County amendments",
                    "phoenix": "IBC 2018 (Arizona adopted), Phoenix amendments",
                    "chicago": "Chicago Building Code (Title 14B), not IBC-based",
                }
                codes = code_refs.get(jurisdiction, code_refs["default"])
                
                prompt = f"Generate a permit application compliance package for: {query}\n\nInclude:\n1. Jurisdiction: {jurisdiction.title()}\n2. Applicable Codes: {codes}\n3. Occupancy classification per IBC Chapter 3\n4. Construction type per IBC Chapter 6\n5. Fire separation requirements per IBC Chapter 7\n6. Egress calculations per IBC Chapter 10\n7. Accessibility requirements per ADA 2010 Standards\n8. Permit submission checklist\n9. Required stamped drawings list\n10. AHJ review notes\n\nCite specific code sections. Note that local amendments may apply."
                if refs: prompt = f"Reference codes:\n{refs[:3000]}\n\n{prompt}"
                result = self.ask_llm(prompt)
                result += f"\n\n---\n## Permit Package Control\n| Field | Value |\n|-------|-------|\n| **Generated** | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')} |\n| **Jurisdiction** | {jurisdiction.title()} |\n| **Governing Codes** | {codes} |\n| **Agent** | DraftClaw v5 Constitutional |\n| **Disclaimer** | For preliminary submittal only. Verify with local AHJ. Requires PE/SE stamp. |\n\n*NOT FOR CONSTRUCTION - FOR PERMIT PREPARATION REFERENCE ONLY*"

            elif cmd in ("/blueprint","/floorplan") and query:
                prompt = f"Generate detailed architectural blueprint specifications with dimensions, room layouts, wall placements, door/window locations, and structural notes. Include code references where applicable.\n\nProject: {query}"
                if refs: prompt = f"Reference material from building codes and standards:\n{refs[:3000]}\n\n{prompt}"
                result = self.ask_llm(prompt)
                # Also generate a PIL rendering as visual supplement
                try:
                    from agents.draftclaw.commands.blueprint import run
                    pil_result = run(query)
                    if pil_result and "Error" not in str(pil_result):
                        export = self._fileclaw_export("png", str(pil_result))
                        result = f"{export}\n\n{result}"
                except:
                    pass

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
