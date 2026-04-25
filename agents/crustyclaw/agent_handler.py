"""A2A Handler for CrustyClaw - Rust AI Shell with Auto-Save"""
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
from shared.base_agent import BaseAgent

class CrustyClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("crustyclaw")

    def _save_rust(self, code, task):
        EXPORTS.mkdir(exist_ok=True)
        if "```" in code:
            blocks = code.split("```")
            for i, block in enumerate(blocks):
                if i % 2 == 1:
                    block = block.split("\n", 1)[1] if "\n" in block else block
                    code = block
                    break
        name = task[:40].replace(" ", "_").replace(chr(92), "").replace("/", "")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name}_{ts}.rs"
        (EXPORTS / fn).write_text(code, encoding="utf-8")
        return fn

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            if cmd in ("/code", "/rust") and query:
                result = self.ask_llm(f"Write clean Rust code with comments for: {query}")
                fn = self._save_rust(result, query)
                result = f"Saved: {fn}\n\n{result[:600]}"
            elif cmd in ("/explain",) and query:
                result = self.ask_llm(f"Explain this Rust concept clearly: {query}")
            elif cmd in ("/fix", "/debug") and query:
                result = self.ask_llm(f"Fix this Rust code, return fixed code only: {query}")
                fn = self._save_rust(result, query)
                result = f"Saved: {fn}\n\n{result[:600]}"
            elif cmd in ("/help",):
                result = "CrustyClaw - Rust AI\n  /code <task> - Generate + auto-save .rs\n  /explain /fix /stats"
            elif cmd in ("/stats",):
                result = f"CrustyClaw | Rust | Auto-save .rs | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Rust expert. Question: {query}")
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = CrustyClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
