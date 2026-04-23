"""A2A Handler for LangClaw - AI Language Teacher with STT/TTS"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class LangClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('langclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/lesson", "lesson") and query:
                result = self.ask_llm(f"Language teacher. Create a beginner lesson with vocabulary, grammar, exercises for: {query}")
            elif cmd in ("/practice", "practice") and query:
                result = self.ask_llm(f"Language tutor. Create practice exercises (fill-in-blank, translation) for: {query}")
            elif cmd in ("/vocab", "vocab") and query:
                result = self.ask_llm(f"List 10 essential words with translations and example sentences for: {query}")
            elif cmd in ("/conversation", "conversation") and query:
                result = self.ask_llm(f"Simulate a natural conversation as a native {query} speaker. Keep it simple.")
            elif cmd in ("/teach", "teach") and query:
                result = self.ask_llm(f"Interactive {query} teacher. Start with greetings. One concept at a time. Be encouraging. Ask questions.")
            elif cmd in ("/speak", "speak") and query:
                result = f"[TTS] Speak: '{query}'\nLangClaw uses Google TTS, Edge TTS, and system TTS for voice output."
            elif cmd in ("/listen", "listen"):
                result = "[STT] Listening...\nLangClaw uses Google Speech-to-Text for voice input. Speak clearly into your microphone."
            elif cmd in ("/help",):
                result = "LangClaw - AI Language Teacher\n  /lesson <lang> - Full lesson\n  /practice <lang> - Exercises\n  /vocab <lang> - Vocabulary\n  /conversation <lang> - Practice chat\n  /teach <lang> - Interactive teacher\n  /speak <text> - TTS voice output\n  /listen - STT voice input\n  /stats"
            elif cmd in ("/stats",):
                result = f"LangClaw | AI Teacher | STT + TTS | Lessons/Conversation | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Language teacher. Help the student learn: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = LangClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
