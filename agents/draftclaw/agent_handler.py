"""A2A Handler for DraftClaw - Technical Drawings & Blueprints"""
import sys, os
from pathlib import Path
from datetime import datetime

DRAFTCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAFTCLAW_DIR))

from shared.base_agent import BaseAgent

class DraftClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("draftclaw")

    def _fileclaw_export(self, fmt, content):
        try:
            safe = content.replace('\n', '\\n').replace('"', '\\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe}", timeout=30)
            if result:
                return result
        except: pass
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"draftclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved: {fn.name}"

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Blueprint generation with PIL
            if cmd in ("/blueprint", "/floorplan") and query:
                from agents.draftclaw.commands.blueprint import run
                result = run(query)
                if result and "Error" not in str(result):
                    export = self._fileclaw_export("png", str(result))
                    result = f"{export}\n\n{str(result)}"

            # CAD/schematic generation via LLM
            elif cmd in ("/cad", "/schematic") and query:
                result = self.ask_llm(
                    f"Generate a technical schematic with precise measurements, component layout, and connection points. Format as ASCII art diagram.\n\nSpecs: {query}"
                )

            # Circuit diagram
            elif cmd in ("/circuit", "/wiring") and query:
                result = self.ask_llm(
                    f"Create a circuit/wiring diagram with components labeled, connections shown, and specifications listed. Use ASCII art.\n\nDesign: {query}"
                )

            # Technical specifications
            elif cmd in ("/specs", "/specifications") and query:
                result = self.ask_llm(
                    f"Generate detailed technical specifications with dimensions, materials, tolerances, and assembly notes.\n\nProject: {query}"
                )

            # Export
            elif cmd == "/export" and args:
                parts2 = args.split(maxsplit=1)
                if len(parts2) == 2:
                    result = self._fileclaw_export(parts2[0], parts2[1])
                else:
                    result = "Usage: /export <format> <content>"

            elif cmd == "/help":
                result = """DraftClaw - Technical Drawings & Blueprints
  /blueprint <specs>     - Generate PIL blueprint + auto-save PNG
  /floorplan <rooms>     - Same as /blueprint
  /cad <specs>           - Generate CAD schematic (ASCII)
  /schematic <specs>     - Same as /cad
  /circuit <design>      - Circuit/wiring diagram (ASCII)
  /wiring <design>       - Same as /circuit
  /specs <project>       - Technical specifications with dimensions
  /export <fmt> <content> - Export via FileClaw (21 formats)
  /help /stats"""

            elif cmd == "/stats":
                result = f"DraftClaw | PIL Blueprints + CAD + Circuits | FileClaw Export | Interactions: {self.state.get('interactions', 0)}"

            elif query:
                # Fallback: generate specs then offer to render
                specs = self.ask_llm(f"Generate technical drawing specifications with dimensions for: {query}")
                result = f"Specifications generated. Use /blueprint to render.\n\n{specs}"
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DraftClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)