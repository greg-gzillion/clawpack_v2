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

    def _gather_context(self, query="", diagram_type="flowchart"):
        """Gather domain-specific context from specialists based on diagram type"""
        parts = []
        # Always search web for Mermaid syntax and examples
        web = self.call_agent("webclaw", f"search mermaid {diagram_type} diagram {query}", timeout=15)
        if web: parts.append("[WebClaw Examples]: " + web)
        # Local data references
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw References]: " + data)
        # Domain-specific specialists
        if any(w in query.lower() for w in ["blockchain", "smart contract", "tx.org", "cosmwasm"]):
            tx = self.call_agent("txclaw", f"/contract {query}", timeout=15)
            if tx: parts.append("[TXClaw Blockchain]: " + tx)
        if any(w in query.lower() for w in ["code", "architecture", "system", "api", "database"]):
            coder = self.call_agent("claw_coder", f"/explain {query}", timeout=15)
            if coder: parts.append("[ClawCoder Architecture]: " + coder)
        if any(w in query.lower() for w in ["legal", "law", "contract", "compliance"]):
            law = self.call_agent("lawclaw", f"/legal {query}", timeout=15)
            if law: parts.append("[LawClaw Legal]: " + law)
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
            if cmd in ("/flowchart", "flowchart"): diagram_type = "flowchart"
            elif cmd in ("/sequence", "sequence"): diagram_type = "sequence"
            elif cmd in ("/architecture", "architecture"): diagram_type = "architecture"
            else: diagram_type = "flowchart"

            ctx = self._gather_context(query, diagram_type)
            enhanced_query = f"Context from specialists:\n{ctx}\n\nTask: {query}" if ctx else query
            code = self.engine.generate_with_llm(diagram_type, enhanced_query, self.llm)

            if cmd in ("/view", "view"):
                self.viewer.view_in_browser(code, query)
                result = f"Opened in browser.\n\n`mermaid\n{code}\n`"
            elif cmd in ("/export", "export"):
                # Export via FileClaw for all formats (PNG, SVG, PDF, DOCX, MD)
                parts2 = args.split(maxsplit=1) if args else ["md", query]
                fmt = parts2[0] if parts2[0] in ("png","svg","pdf","docx","md","html") else "md"
                export_result = self.call_agent("fileclaw", f"/export {fmt} Mermaid Diagram: {query}\n\n```mermaid\n{code}\n```", timeout=30)
                if export_result:
                    result = f"{export_result}\n\n`mermaid\n{code}\n`"
                else:
                    # Fallback to local docx export
                    output_dir = Path("C:/Users/greg/dev/clawpack_v2/agents/flowclaw/exports")
                    output_dir.mkdir(exist_ok=True)
                    path = output_dir / f"diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    self.docx_exporter.export(code, path, query)
                    result = f"Exported to {path}.docx\n\n`mermaid\n{code}\n`"
            elif cmd in ("/help",):
                result = "FlowClaw - Diagrams with Specialists\n  /flowchart /sequence /architecture /view /export /stats\n  Uses: WebClaw + DataClaw + TXClaw + ClawCoder + LawClaw -> DiagramEngine -> FileClaw"
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
