"""A2A Handler for MedicLaw - Medical Agent with A2A routing"""
import sys, time, json, re
from pathlib import Path

MEDICLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(MEDICLAW_DIR))

from core.agent import MediclawAgent
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class MedicLawHandler(BaseAgent):
    def __init__(self):
        super().__init__("mediclaw")
        self.agent = MediclawAgent()

    def _gather_context(self, query=""):
        """Gather medical context from WebClaw and DataClaw."""
        parts = []
        web = self.cached_search(f"ns:mediclaw medical {query}")
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
        data = self.call_agent("dataclaw", f"/search ns:mediclaw {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + str(data)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:500])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/help", "help"):
                result = """MedicLaw - Medical AI Agent
  /research <topic> /diagnose <symptoms> /treatment <condition>
  /medications <drug> /interactions <drugs> /warnings <drug>
  /pediatrics <issue> /geriatrics <issue> /lab <test> /icd <diagnosis>
  /prevention <condition> /diet <condition> /exercise <condition>
  /natural <condition> /procedure <name> /prognosis <condition>
  /referral <condition> /emergency <symptom> /hospital <city>
  /delegate <agent> <task> /translate <text> <lang>
  /sources /stats /help"""
            elif cmd in ("/sources", "sources"):
                result = f"Medical Sources ({len(self.agent.list_sources())}):\n" + "\n".join(f"  {i}. {s}" for i, s in enumerate(self.agent.list_sources(), 1))
            elif cmd in ("/stats", "stats"):
                result = f"MedicLaw | Queries: {len(self.agent.session["queries"])} | Sources: {len(self.agent.list_sources())} | Started: {self.agent.session["started"]}"
            elif cmd in ("/diagnose",) and args:
                from agents.mediclaw.commands.diagnose import run as diagnose_run
                result = diagnose_run(args, agent=self)
            elif cmd in ("/treatment", "/research", "/med") and args:
                method = {"treatment": self.agent.treatment, "research": self.agent.research, "med": self.agent.research}[cmd.lstrip("/")]
                result = method(args)
            elif cmd == "/medications" and args: result = self.agent.medications(args)
            elif cmd == "/interactions" and args: result = self.agent.interactions(args)
            elif cmd == "/warnings" and args: result = self.agent.warnings(args)
            elif cmd == "/pediatrics" and args: result = self.agent.pediatrics(args)
            elif cmd == "/geriatrics" and args: result = self.agent.geriatrics(args)
            elif cmd == "/lab" and args: result = self.agent.lab_tests(args)
            elif cmd == "/icd" and args: result = self.agent.coding(args)
            elif cmd == "/prevention" and args: result = self.agent.prevention(args)
            elif cmd == "/diet" and args: result = self.agent.diet(args)
            elif cmd == "/exercise" and args: result = self.agent.exercise(args)
            elif cmd == "/natural" and args: result = self.agent.natural(args)
            elif cmd == "/procedure" and args: result = self.agent.procedure(args)
            elif cmd == "/prognosis" and args: result = self.agent.prognosis(args)
            elif cmd == "/referral" and args:
                from agents.mediclaw.commands._helpers import lookup_hospitals
                base_result = self.agent.referral(args)
                loc_match = re.search(r"in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s*([A-Z]{2})", args)
                if loc_match:
                    city_state = f"{loc_match.group(1)} {loc_match.group(2)}"
                    try:
                        hospitals = lookup_hospitals(city_state, agent=self)
                        if hospitals.get("hospitals"):
                            base_result += f"\n\n### Facilities in {city_state}\n"
                            for h in hospitals["hospitals"][:3]:
                                base_result += f"\n- **{h.get("name","?")}**"
                                if h.get("address"): base_result += f"\n  {h["address"]}"
                                if h.get("phone"): base_result += f"\n  {h["phone"]}"
                                if h.get("url"): base_result += f"\n  {h["url"]}"
                                if h.get("lat") and h.get("lon"): base_result += f"\n  {h["lat"]}, {h["lon"]}"
                    except Exception: pass
                result = base_result
            elif cmd == "/emergency" and args:
                from agents.mediclaw.commands.emergency import run as emergency_run
                result = emergency_run(args, agent=self)
            elif cmd in ("/delegate",) and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","liberateclaw","designclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
            elif cmd in ("/translate",) and args:
                target_lang = args.split()[-1] if args.split() else "Spanish"
                instructions = """TRANSLATION REQUIREMENTS - PRESERVE EXACTLY:
1. ALL medical terminology (diagnosis names, anatomical terms, procedure names) - DO NOT TRANSLATE
2. ALL medication names (generic and brand) - DO NOT TRANSLATE
3. ALL lab values and units - DO NOT TRANSLATE
4. ALL ICD codes and medical coding - DO NOT TRANSLATE
5. Translate all explanatory text and patient guidance to the target language"""
                payload = f"/translate to {target_lang}\n\n{instructions}\n\n{args[:5000]}"
                result = self.call_agent("interpretclaw", payload, timeout=120)
            elif cmd=="/shared" and args:
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
            elif cmd in ("/hospital", "/hospitals") and args:
                from agents.mediclaw.commands._helpers import lookup_hospitals
                hospitals = lookup_hospitals(args, agent=self)
                if "error" in hospitals:
                    result = hospitals["error"]
                else:
                    lines = [f"Hospitals: {hospitals.get("city","")}, {hospitals.get("state","")}", "=" * 50]
                    for h in hospitals.get("hospitals", []):
                        lines.append(f"\n  {h.get("name","Unknown")}")
                        if h.get("address"): lines.append(f"     Address: {h["address"]}")
                        if h.get("phone"): lines.append(f"     Phone: {h["phone"]}")
                        if h.get("url"): lines.append(f"     Website: {h["url"]}")
                        if h.get("lat") and h.get("lon"): lines.append(f"     GPS: {h["lat"]}, {h["lon"]}")
                    result = "\n".join(lines)
            elif cmd == "/nearest" and args:
                from agents.mediclaw.commands._helpers import find_nearest_hospital
                parts2 = args.split(",")
                if len(parts2) == 2:
                    try:
                        lat, lon = float(parts2[0].strip()), float(parts2[1].strip())
                        hospitals = find_nearest_hospital(lat, lon, agent=self)
                        if "error" in hospitals:
                            result = hospitals["error"]
                        else:
                            lines = [f"Nearest Hospitals to ({lat}, {lon})", "=" * 50]
                            for h in hospitals.get("hospitals", []):
                                lines.append(f"\n  {h.get("name","Unknown")}")
                                if h.get("address"): lines.append(f"     {h["address"]}")
                                if h.get("phone"): lines.append(f"     Phone: {h["phone"]}")
                                if h.get("url"): lines.append(f"     Website: {h["url"]}")
                                if h.get("lat") and h.get("lon"): lines.append(f"     GPS: {h["lat"]}, {h["lon"]}")
                            result = "\n".join(lines)
                    except ValueError:
                        result = "Usage: /nearest <lat>,<lon>"
                else:
                    result = "Usage: /nearest <lat>,<lon>"
            elif args:
                context = self._gather_context(args)
                result = self.ask_llm(f"Medical information: {args}\n\nContext:\n{context}")
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "mediclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                else:
                    result = f"Usage: {cmd} <query>  |  Type /help for all commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            log_err("mediclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = MedicLawHandler()


def process_task(task: str, agent: str = None):
    return _agent.handle(task)
