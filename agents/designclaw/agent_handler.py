"""A2A Handler for DesignClaw - Creative Design Assistant"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class DesignClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('designclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/brand", "brand") and query:
                result = self.ask_llm(f"Create a complete brand identity. Include: brand name ideas, color palette (hex codes), typography pairings, logo concept, brand voice, target audience. For: {query}")
            elif cmd in ("/mood", "mood") and query:
                result = self.ask_llm(f"Create a mood board concept. Describe: color mood, textures, imagery, typography, atmospheric description. For: {query}")
            elif cmd in ("/colors", "colors") and query:
                result = self.ask_llm(f"Create a color palette with hex codes. Include primary, secondary, accent, background colors. For: {query}")
            elif cmd in ("/typography", "typography") and query:
                result = self.ask_llm(f"Recommend typography pairings (heading + body fonts) with Google Fonts names. For: {query}")
            elif cmd in ("/logo", "logo") and query:
                result = self.ask_llm(f"Describe a logo concept. Include: symbol/icon, typography, colors, style, variations. For: {query}")
            elif cmd in ("/slogan", "slogan") and query:
                result = self.ask_llm(f"Generate 10 catchy slogan/tagline options. For: {query}")
            elif cmd in ("/help",):
                result = "DesignClaw - Creative Design Assistant\n  /brand <name> - Brand identity\n  /mood <aesthetic> - Mood board\n  /colors <context> - Color palette\n  /typography <style> - Font pairings\n  /logo <concept> - Logo design\n  /slogan <brand> - Taglines\n  /stats"
            elif cmd in ("/stats",):
                result = f"DesignClaw | Brand/Mood/Color/Typography | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Creative design assistant. Provide design concepts, colors, and ideas for: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DesignClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
