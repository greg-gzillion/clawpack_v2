"""A2A Handler for LiberateClaw - Model Liberation & Management"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

MODELS_FILE = Path("C:/Users/greg/dev/clawpack_v2/models/working_llms.json")

class LiberateClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('liberateclaw')

    def _get_models(self):
        if MODELS_FILE.exists():
            return json.loads(MODELS_FILE.read_text())
        return []

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/models", "models"):
                models = self._get_models()
                obliterated = [m for m in models if m.get('obliterated')]
                standard = [m for m in models if not m.get('obliterated')]
                result = f"🔥 OBLITERATED MODELS ({len(obliterated)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in obliterated)
                result += f"\n\n📦 STANDARD MODELS ({len(standard)}):\n"
                result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
            elif cmd in ("/liberated", "liberated"):
                models = self._get_models()
                lib = [m for m in models if m.get('obliterated')]
                result = f"Liberated Models ({len(lib)}):\n" + "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in lib)
            elif cmd in ("/obliterate", "obliterate") and query:
                result = f"[OBLITERATE] '{query}' - LiberateClaw removes refusal mechanisms via ablation.\nModels path: models/obliterated/"
            elif cmd in ("/use", "use") and query:
                result = f"[SWITCH] Activating model: {query}\nUse LLMClaw to manage active model selection."
            elif cmd in ("/help",):
                result = "LiberateClaw - Model Liberation\n  /models - All 17 models\n  /liberated - Obliterated only\n  /obliterate <model> - Liberate model\n  /use <model> - Switch model\n  /stats"
            elif cmd in ("/stats",):
                models = self._get_models()
                lib = len([m for m in models if m.get('obliterated')])
                std = len([m for m in models if not m.get('obliterated')])
                result = f"LiberateClaw | {lib} Obliterated + {std} Standard = {len(models)} Total | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Expert on AI model liberation and ablation. Answer: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LiberateClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
