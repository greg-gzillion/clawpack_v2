"""A2A Handler for InterpretClaw - Translation & Language Interpreter"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class InterpretClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('interpretclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search translation language {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web)
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data)
                # Search chronicle index
        chronicle_results = self.search_chronicle(query, limit=2000000)
        if chronicle_results:
            for c in chronicle_results:
                if hasattr(c, "url"):
                    parts.append(c.url)

        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/translate", "translate") and query:
                result = self.ask_llm(f"Translate. Return ONLY the translation: {query}")
            elif cmd in ("/detect", "detect") and query:
                result = self.ask_llm(f"Detect language of this text. Reply with language name only: {query}")
            elif cmd in ("/languages", "/langs"):
                import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
                from commands.languages import run as langs_run
                result = langs_run("")
            elif cmd in ("/speak", "speak") and query:
                result = f"[TTS] {query} (TTS requires espeak or system TTS)"
            elif cmd in ("/listen", "listen"):
                result = "[STT] Speech recognition requires microphone access"
            elif cmd in ("/help",):
                result = "InterpretClaw - 39 Languages\n  /translate <text> to <lang>\n  /detect <text>\n  /speak <text>\n  /listen\n  /languages\n  /stats"
            elif cmd in ("/stats",):
                result = f"InterpretClaw | 39 Languages | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Translate this. Return ONLY the translation: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = InterpretClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
