"""A2A Handler for LLMClaw - Model Management with A2A Routing"""
import sys, os, json
from pathlib import Path

LLMCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = LLMCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

from shared.base_agent import BaseAgent

def _get_working_llms():
    f = PROJECT_ROOT / "models" / "working_llms.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except:
            pass
    return []

def _get_active():
    f = PROJECT_ROOT / "models" / "active_model.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except:
            pass
    return {"model": "llama-3.1-8b-instant", "source": "groq"}

def _set_active(model_name, source):
    config = _get_active()
    config["model"] = model_name
    config["source"] = source
    f = PROJECT_ROOT / "models" / "active_model.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(config, indent=2))

class LLMClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("llmclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        # Ask LiberateClaw for model recommendations
        lib = self.call_agent("liberateclaw", f"/models", timeout=10)
        if lib and "OBLITERATED" in lib:
            parts.append("[LiberateClaw]: Models available")
        return "\n".join(parts)

    def _run_llm(self, prompt):
        os.chdir(str(LLMCLAW_DIR))
        from commands.llm import run
        return run(prompt)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        os.chdir(str(LLMCLAW_DIR))
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd == "/llm" and args:
                ctx = self._gather_context(args)
                if ctx:
                    args = f"Context from A2A specialists:\n{ctx}\n\nTask: {args}"
                result = self._run_llm(args)
            elif cmd in ("/models", "/list", "models", "list"):
                models = _get_working_llms()
                obliterated = [m for m in models if m.get("obliterated")]
                standard = [m for m in models if not m.get("obliterated")]
                active = _get_active()
                result = f"Active: {active.get('model')} ({active.get('source')})\n\n"
                result += f"OBLITERATED ({len(obliterated)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in obliterated)
                result += f"\n\nSTANDARD ({len(standard)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
                result += "\n\nUse /use <model_name> to switch"
            elif cmd in ("/use", "use") and args:
                _set_active(args, "ollama" if ":" in args else "groq")
                result = f"Switched to: {args}"
            elif cmd in ("/obliterated", "obliterated"):
                models = _get_working_llms()
                lib = [m for m in models if m.get("obliterated")]
                result = f"Obliterated models available: {len(lib)}\n" + "\n".join(m["model"] for m in lib)
            elif cmd in ("/normal", "normal"):
                models = _get_working_llms()
                std = [m for m in models if not m.get("obliterated")]
                result = f"Standard models available: {len(std)}\n" + "\n".join(m["model"] for m in std)
            elif cmd in ("/help",):
                result = "LLMClaw - Model Manager with A2A Routing\n  /llm <prompt> - Run inference\n  /models - List all models\n  /use <name> - Switch model\n  /obliterated /normal /help /stats\n  Uses: WebClaw + DataClaw + LiberateClaw"
            elif cmd in ("/stats",):
                active = _get_active()
                result = f"LLMClaw | Active: {active.get('model')} ({active.get('source')}) | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(task)
                if ctx:
                    task = f"Context from A2A specialists:\n{ctx}\n\nTask: {task}"
                result = self._run_llm(task)

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LLMClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
