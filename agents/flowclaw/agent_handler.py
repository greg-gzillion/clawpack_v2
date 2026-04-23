"""A2A Handler for FlowClaw - Diagram Generator with Viewer + Export"""
import sys
from pathlib import Path
from datetime import datetime

FLOWCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = FLOWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(FLOWCLAW_DIR))

from shared.base_agent import BaseAgent
from engine.diagram_engine import DiagramEngine
from viewer.diagram_viewer import DiagramViewer
from exporters.base_exporter import DocxExporter, PdfExporter

# Adapter so engine can use BaseAgent.ask_llm
class LLMAdapter:
    def __init__(self, agent): self.agent = agent
    def chat_sync(self, prompt, **kw): return self.agent.ask_llm(prompt)

class FlowClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('flowclaw')
        self.engine = DiagramEngine()
        self.viewer = DiagramViewer()
        self.docx_exporter = DocxExporter()
        self.pdf_exporter = PdfExporter()
        self.llm = LLMAdapter(self)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/flowchart", "flowchart"): diagram_type = "flowchart"
            elif cmd in ("/sequence", "sequence"): diagram_type = "sequence"
            elif cmd in ("/architecture", "architecture"): diagram_type = "architecture"
            else: diagram_type = "flowchart"

            code = self.engine.generate_with_llm(diagram_type, query, self.llm)

            if cmd in ("/view", "view"):
                self.viewer.view_in_browser(code, query[:50])
                result = f"Opened in browser.\n\n`mermaid\n{code}\n`"
            elif cmd in ("/export", "export"):
                output_dir = Path("C:/Users/greg/dev/clawpack_v2/agents/flowclaw/exports")
                output_dir.mkdir(exist_ok=True)
                path = output_dir / f"diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.docx_exporter.export(code, path, query[:50])
                result = f"Exported to {path}.docx\n\n`mermaid\n{code}\n`"
            elif cmd in ("/help",):
                result = "FlowClaw - Diagrams\n  /flowchart /sequence /architecture /view /export /stats"
            elif cmd in ("/stats",):
                result = f"FlowClaw | Engine+Viewer+Export | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = f"`mermaid\n{code}\n`"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = FlowClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
