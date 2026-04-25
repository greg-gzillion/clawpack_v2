"""A2A Handler for DesignClaw - Brand & Design Generator"""
import sys, os
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DESIGNCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent
from commands.llm_enhanced import run as llm_run

EXPORTS = PROJECT_ROOT / "exports"

class DesignClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('designclaw')

    def _call_llm(self, prompt: str) -> str:
        result = llm_run(prompt)
        return result if result and "Error" not in result else "Design generation failed"

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "/brand" and args:
                result = self._call_llm(f"Create a complete brand identity for: {args}. Include name, logo concept, colors, typography, brand voice.")
                result = f"🎨 BRAND IDENTITY\n\n{result}"
            elif cmd == "/mood" and args:
                result = self._call_llm(f"Describe a mood board direction for: {args}. Include vibe, color story, texture, imagery style.")
                result = f"🎭 MOOD BOARD\n\n{result}"
            elif cmd == "/colors" and args:
                result = self._call_llm(f"Create a color palette for: {args}. Provide 4-5 hex codes with names and usage notes.")
                result = f"🎨 COLOR PALETTE\n\n{result}"
            elif cmd == "/logo" and args:
                result = self._call_llm(f"Design a logo concept for: {args}. Describe the symbol, wordmark, colors, and style.")
                result = f"✨ LOGO CONCEPT\n\n{result}"
            elif cmd == "/slogan" and args:
                result = self._call_llm(f"Create brand copy for: {args}. Provide tagline, value proposition, and brand voice.")
                result = f"✍️ BRAND COPY\n\n{result}"
            elif cmd == "/help":
                result = "DesignClaw - Brand & Design Agent\n  /brand /mood /colors /logo /slogan /stats"
            elif cmd == "/stats":
                result = f"DesignClaw | Brand & Design | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.smart_ask(f"Design advice: {task}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DesignClawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
