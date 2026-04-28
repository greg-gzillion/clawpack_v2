"""A2A Handler for CrustyClaw - Rust AI with real commands + FileClaw"""
import sys, os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CRUSTY_DIR = Path(__file__).resolve().parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CRUSTY_DIR))

from shared.base_agent import BaseAgent
from shared.security import InputSanitizer
LLMCLAW_DIR = PROJECT_ROOT / "agents" / "llmclaw"
sys.path.insert(0, str(LLMCLAW_DIR))

class CrustyClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("crustyclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search rust {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        tx = self.call_agent("txclaw", f"/contract {query}", timeout=15)
        if tx: parts.append("[TXClaw]: " + tx)
                # Search chronicle index
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return " | ".join(parts)

    def _save_rs(self, code, task):
        EXPORTS.mkdir(exist_ok=True)
        if "```" in code:
            blocks = code.split("```")
            for i, block in enumerate(blocks):
                if i % 2 == 1:
                    block = block.split("\n", 1)[1] if "\n" in block else block
                    code = block
                    break
        name = task.replace(" ", "_").replace(chr(92), "").replace("/", "")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"{name}_{ts}.rs"
        fn = InputSanitizer.sanitize_filename(fn)
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
            # Use real command modules
            if cmd in ("/rust", "/code") and query:
                from agents.crustyclaw.commands.rust import run
                result = run(query)
                fn = self._save_rs(result, query)
                result = f"Saved: {fn}\n\n{result}"
            elif cmd in ("/explain",) and query:
                from agents.crustyclaw.commands.explain import run
                result = run(query)
            elif cmd in ("/cargo",) and query:
                from agents.crustyclaw.commands.cargo import run
                result = run(query)
            elif cmd in ("/fix", "/debug") and query:
                ctx = self._gather_context(query)
                result = self.ask_llm("Context: " + ctx + "\n\nFix this Rust code, return fixed code only: {query}")
                fn = self._save_rs(result, "fixed")
                result = f"Saved: {fn}\n\n{result}"
            elif cmd in ("/audit",) and query:
                ctx = self._gather_context(query)
                result = self.ask_llm("Context: " + ctx + "\n\nSecurity audit this Rust code. Check unsafe blocks, unwraps, input validation, dependencies:\n{query}")
            elif cmd in ("/test",) and query:
                ctx = self._gather_context(query)
                result = self.ask_llm("Context: " + ctx + "\n\nWrite Rust unit tests with #[cfg(test)]:\n{query}")
            elif cmd in ("/help",):
                result = "CrustyClaw - Rust AI Assistant\n  /rust /code <task> - Generate Rust + auto-save .rs\n  /explain <concept> - WebClaw + LLM explanation\n  /cargo <cmd> - Run actual cargo commands\n  /fix <code> - Debug and fix Rust code\n  /audit <code> - Security audit\n  /test <code> - Generate unit tests"
            elif cmd in ("/stats",):
                result = f"CrustyClaw | Rust AI | WebClaw + LLMClaw + Cargo | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(query)
                result = self.ask_llm("Context: " + ctx + "\n\nRust expert. Question: " + query)
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = CrustyClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
