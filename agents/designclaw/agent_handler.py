"""A2A Handler for DesignClaw v5 - Constitutional Design Agent"""
import sys, json, os
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DESIGNCLAW_DIR))

from shared.base_agent import BaseAgent

class DesignClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("designclaw")

    def _save_html(self, content, name):
        EXPORTS.mkdir(exist_ok=True)
        html = content
        if "`html" in html: html = html.split("`html")[1].split("`")[0]
        elif "`" in html:
            blocks = html.split("`")
            for i, block in enumerate(blocks):
                if i%2==1: html = block; break
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name}_{ts}.html"
        filepath = EXPORTS/fn
        filepath.write_text(html, encoding="utf-8")
        os.startfile(str(filepath))
        return fn

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]: return {"status":"error","result":f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts)>1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                result = "DesignClaw v5 - Constitutional Design Agent\n  /brand /colors /mood /type /copy /logo /kit /html\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}
            if cmd in ("/stats",): return {"status":"success","result":f"DesignClaw v5 | Brand & Design | Interactions: {self.state.get('interactions',0)}"}

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
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","interpretclaw","docuclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            if cmd in ("/brand","/identity","brand") and query:
                result = self.ask_llm(f"Create a complete brand identity: 1. Brand essence 2. Logo concept 3. Color palette with hex codes 4. Typography 5. Brand voice.\n\nBrief: {query}")
            elif cmd in ("/colors","/palette","colors") and query:
                result = self.ask_llm(f"Create a color palette with 5 hex codes and usage notes.\n\nContext: {query}")
            elif cmd in ("/mood","mood") and query:
                result = self.ask_llm(f"Describe an aesthetic mood direction: vibe, color story, texture, typography style, references.\n\nContext: {query}")
            elif cmd in ("/type","/fonts","type") and query:
                result = self.ask_llm(f"Recommend font pairings with Google Fonts links, header and body.\n\nStyle: {query}")
            elif cmd in ("/copy","/slogan","copy") and query:
                result = self.ask_llm(f"Write brand copy: tagline, value proposition, mission, 3 brand voice adjectives.\n\nBrand: {query}")
            elif cmd in ("/logo","logo") and query:
                result = self.ask_llm(f"Create an SVG logo design with shapes, colors, layout. Include SVG code.\n\nLogo for: {query}")
            elif cmd in ("/kit","/full","kit") and query:
                result = self.ask_llm(f"Create a complete brand kit as HTML with inline CSS: brand name, logo concept, color swatches, typography, brand voice, sample business card.\n\nBrand: {query}\n\nReturn complete HTML.")
                fn = self._save_html(result, query.replace(" ","_")[:40])
                result = f"Saved: {fn}\n\n{result}"
            elif cmd in ("/html","/web","html") and query:
                result = self.ask_llm(f"Create a complete responsive HTML page with embedded CSS. Beautiful and modern.\n\nDesign for: {query}\n\nReturn complete HTML.")
                fn = self._save_html(result, query.replace(" ","_")[:40])
                result = f"Saved: {fn}\n\n{result}"
            elif query: result = self.ask_llm(f"Senior design consultant. Answer concisely: {query}")
            else: result = "Type /help for commands"

            from data_io import write_shared
            write_shared("designclaw_latest", {"command":cmd,"query":query})

            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type")=="delegate":
                target = payload["target_agent"]; task_text = payload.get("payload", payload.get("command",""))
                if isinstance(task_text, dict): task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status":"success","result":str(result or f"Delegated to {target}")}
            query = payload.get("query","")
            result = self.ask_llm(f"Senior design consultant. Task: {query}")
            return {"status":"success","result":str(result)}
        except Exception as e: return {"status":"error","result":str(e)}

_agent = DesignClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
