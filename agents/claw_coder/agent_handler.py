"""A2A Handler for ClawCoder - Code Generation with WebClaw + LLM"""
import sys
from pathlib import Path

CLAW_CODER_DIR = Path(__file__).parent
sys.path.insert(0, str(CLAW_CODER_DIR.parent.parent))
from shared.base_agent import BaseAgent

class ClawCoderAgent(BaseAgent):
    def __init__(self):
        super().__init__('claw_coder')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            ctx = self.search_web(f"code {query}", max_results=3)

            if cmd in ("/code", "code") and query:
                result = self.ask_llm(f"Write clean, well-commented code. Context: {ctx}\nTask: {query}")
            elif cmd in ("/explain", "explain") and query:
                result = self.ask_llm(f"Explain this code in detail: {query}")
            elif cmd in ("/debug", "debug") and query:
                result = self.ask_llm(f"Debug this code, find issues and suggest fixes: {query}")
            elif cmd in ("/review", "review") and query:
                result = self.ask_llm(f"Review this code for style, performance, bugs: {query}")
            elif cmd in ("/tutorial", "tutorial") and query:
                result = self.ask_llm(f"Create a programming tutorial for: {query}")
            elif cmd in ("/help",):
                result = "ClawCoder - 38 Languages\n  /code /explain /debug /review /tutorial /stats"
            elif cmd in ("/stats",):
                result = f"ClawCoder | 38 Languages | WebClaw + LLM | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Context: {ctx}\nTask: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = ClawCoderAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
