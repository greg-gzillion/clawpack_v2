"""A2A Handler for DrawClaw - AI Prompts + Drawing Commands"""
import sys
from pathlib import Path

DRAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DRAWCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DRAWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import delegate, log_err


class DrawClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("drawclaw")

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Cross-Agent Delegation
            if cmd in ("/delegate", "delegate") and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                result = delegate("drawclaw", target, task_text)

            elif cmd in ("/export", "export") and query:
                result = delegate("drawclaw", "docuclaw", f"/create art: {query}", timeout=60)

            # Drawing commands
            elif cmd in ("/canvas", "canvas"):
                from agents.drawclaw.commands.canvas import run
                result = run(query)
            elif cmd in ("/sketch", "sketch") and query:
                from agents.drawclaw.commands.sketch import run
                result = run(query)
            elif cmd in ("/doodle", "doodle") and query:
                from agents.drawclaw.commands.doodle import run
                result = run(query)
            elif cmd in ("/paint", "paint") and query:
                from agents.drawclaw.commands.paint import run
                result = run(query)
            elif cmd in ("/illustrate", "illustrate") and query:
                from agents.drawclaw.commands.illustrate import run
                result = run(query)
            elif cmd in ("/cartoon", "cartoon") and query:
                from agents.drawclaw.commands.cartoon import run
                result = run(query)
            elif cmd in ("/draw", "draw") and query:
                from agents.drawclaw.commands.draw import run
                result = run(query)

            # AI prompt commands
            elif cmd in ("/prompt", "prompt") and query:
                from agents.drawclaw.commands.prompt import run
                result = run(query)
            elif cmd in ("/describe", "describe") and query:
                from agents.drawclaw.commands.describe import run
                result = run(query)
            elif cmd in ("/style", "style") and query:
                from agents.drawclaw.commands.style import run
                result = run(query)
            elif cmd in ("/compose", "compose") and query:
                from agents.drawclaw.commands.compose import run
                result = run(query)

            # Animation, filters, QR
            elif cmd in ("/animate", "animate") and query:
                from agents.drawclaw.commands.animate import run
                result = run(query)
            elif cmd in ("/filter", "filter") and query:
                from agents.drawclaw.commands.filter import run
                result = run(query)
            elif cmd in ("/qr", "qr") and query:
                from agents.drawclaw.commands.qrcode_cmd import run
                result = run(query)

            elif cmd == "/help":
                result = """DrawClaw - AI Prompt Studio + Drawing Tools
  DRAW:     /canvas - Interactive drawing window
            /sketch <style> <subject> - Pencil/charcoal/ink sketch
            /doodle <style> - Algorithmic art (11 styles)
            /paint <style> <scene> - 14 painting styles
            /illustrate <format> <desc> - Comic/storyboard/tutorial
            /cartoon <mood> <character> - Expressive cartoon faces
            /draw <scene> - AI-assisted scene rendering
  PROMPTS:  /prompt <concept> - AI image prompt card
            /describe <visual> - Visual reference card
            /style <concept> - Art style guide card
            /compose <scene> - Composition overlay
  TOOLS:    /animate <style> <frames> - Animated GIF
            /filter <mode> - Apply filter to last drawing
            /qr <url/text> - Generate QR code
  DELEGATE: /delegate /export
  META:     /help /stats"""

            elif cmd == "/stats":
                result = f"DrawClaw | 14 Commands + GIF + Filters + QR | Interactions: {self.state.get('interactions', 0)}"

            elif query:
                result = self.ask_llm(f"Act as a professional digital artist and art director. Query: {query}")
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            log_err("drawclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = DrawClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)