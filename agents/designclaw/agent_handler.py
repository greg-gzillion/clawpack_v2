"""A2A Handler for DesignClaw - Brand & Design with Auto-Save HTML"""
import sys
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
        # Extract HTML from response
        html = content
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            blocks = html.split("```")
            for i, block in enumerate(blocks):
                if i % 2 == 1:
                    html = block
                    break
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name}_{ts}.html"
        (EXPORTS / fn).write_text(html, encoding="utf-8")
        return fn

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Brand identity
            if cmd in ("/brand", "/identity", "brand") and query:
                result = self.ask_llm(
                    f"Create a complete brand identity. Provide: 1. Brand essence 2. Logo concept 3. Color palette with hex codes 4. Typography recommendations 5. Brand voice.\n\nBrief: {query}"
                )

            # Color palette
            elif cmd in ("/colors", "/palette", "colors") and query:
                result = self.ask_llm(
                    f"Create a cohesive color palette with 5 hex codes, descriptive names, and usage notes.\n\nContext: {query}"
                )

            # Mood board
            elif cmd in ("/mood", "mood") and query:
                result = self.ask_llm(
                    f"Describe an aesthetic mood direction. Include: vibe, color story, texture/feel, typography style, reference imagery.\n\nContext: {query}"
                )

            # Typography
            elif cmd in ("/type", "/fonts", "type") and query:
                result = self.ask_llm(
                    f"Recommend font pairings with Google Fonts links. Include header font, body font, and reasoning.\n\nStyle: {query}"
                )

            # Copywriting
            elif cmd in ("/copy", "/slogan", "copy") and query:
                result = self.ask_llm(
                    f"Write brand copy: tagline, value proposition, mission statement, and 3 adjectives for brand voice.\n\nBrand: {query}"
                )

            # Logo generation
            elif cmd in ("/logo", "logo") and query:
                result = self.ask_llm(
                    f"Create an SVG logo design. Describe the shapes, colors, and layout. Include the SVG code.\n\nLogo for: {query}"
                )

            # Full brand kit with HTML
            elif cmd in ("/kit", "/full", "kit") and query:
                result = self.ask_llm(
                    f"Create a complete brand kit as a single HTML page with inline CSS. Include: brand name, logo concept, color palette (as color swatches), typography, brand voice, and sample business card design.\n\nBrand: {query}\n\nReturn complete HTML with embedded CSS."
                )
                fn = self._save_html(result, query.replace(" ", "_")[:40])
                result = f"Saved: {fn}\n\n{result}"

            # HTML design generation
            elif cmd in ("/html", "/web", "html") and query:
                result = self.ask_llm(
                    f"Create a complete responsive HTML page with embedded CSS. Design for: {query}\n\nReturn complete HTML. Make it beautiful and modern."
                )
                fn = self._save_html(result, query.replace(" ", "_")[:40])
                result = f"Saved: {fn}\n\n{result}"

            # Help
            elif cmd in ("/help", "help"):
                result = """DesignClaw - AI Design Assistant
  /brand <brief>      - Complete brand identity
  /colors <context>   - Color palette with hex codes
  /mood <aesthetic>   - Mood board direction
  /type <style>       - Typography recommendations
  /copy <brand>       - Copywriting (tagline, voice)
  /logo <brief>       - SVG logo design
  /kit <brand>        - Full brand kit (HTML)
  /html <design>      - Responsive HTML page
  /help /stats"""

            elif cmd == "/stats":
                result = f"DesignClaw | Brand & Design | Interactions: {self.state.get('interactions', 0)}"

            elif query:
                result = self.ask_llm(f"You are a senior design consultant. Answer concisely: {query}")
            else:
                result = "Type /help for commands"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DesignClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)