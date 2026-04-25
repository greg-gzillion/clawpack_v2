"""A2A Handler for DrawClaw - AI Image Prompt Generator"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shared.base_agent import BaseAgent

class DrawClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('drawclaw')

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search art reference {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        return "\n".join(parts)

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ''
        args = parts[1] if len(parts) > 1 else ''
        query = args if args else task
        try:
            ctx = ''
            try: ctx = self._gather_context(query)
            except: pass

            if cmd == '/prompt' and query:
                result = self.ask_llm(f'Create a detailed AI image generation prompt. Include: subject, style, lighting, composition, colors, mood, camera angle. References: {ctx}\n\nTopic: {query}')
            elif cmd == '/describe' and query:
                result = self.ask_llm(f'Describe this visual concept in rich detail suitable for an artist or AI generator. Context: {ctx}\n\nConcept: {query}')
            elif cmd == '/style' and query:
                result = self.ask_llm(f'Recommend art styles, techniques, and reference artists for: {query}. Include specific style names and why they fit.')
            elif cmd == '/compose' and query:
                result = self.ask_llm(f'Describe an image composition with rule of thirds, leading lines, depth of field, focal point, and framing for: {query}')
            elif cmd == '/export' and query:
                import requests
                try:
                    r = requests.post(self.A2A + '/v1/message/fileclaw', json={'task': f'/export {query}'}, timeout=30)
                    result = r.json().get('result', 'Export failed') if r.status_code == 200 else 'FileClaw unavailable'
                except:
                    result = 'FileClaw A2A unavailable'
            elif cmd == '/help':
                result = 'DrawClaw - AI Image Prompt Studio\n  /prompt <concept> - Generate Midjourney/DALL-E prompt\n  /describe <visual> - Rich visual description\n  /style <concept> - Art style recommendations\n  /compose <scene> - Composition guide\n  /export <fmt> <content> - Export via FileClaw\n  Connected: A2A + WebClaw + LLMClaw + FileClaw'
            elif cmd == '/stats':
                result = f'DrawClaw | Prompt Studio | WebClaw + LLMClaw + FileClaw | Interactions: {self.state.get("interactions", 0)}'
            else:
                result = self.ask_llm(f'Act as a professional digital artist and art director. Context: {ctx}\n\nQuery: {query}')
            return {'status': 'success', 'result': str(result)}
        except Exception as e:
            return {'status': 'error', 'result': str(e)}

_agent = DrawClawAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
