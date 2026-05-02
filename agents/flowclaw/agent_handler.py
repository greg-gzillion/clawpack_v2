"""A2A Handler for FlowClaw v5 - Constitutional contract + cross-agent delegation"""
import sys
import json
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

class LLMAdapter:
    def __init__(self, agent): self.agent = agent
    def chat_sync(self, prompt, **kw): return self.agent.ask_llm(prompt)

class FlowClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("flowclaw")
        self.engine = DiagramEngine()
        self.viewer = DiagramViewer()
        self.docx_exporter = DocxExporter()
        self.pdf_exporter = PdfExporter()
        self.llm = LLMAdapter(self)

    def _gather_context(self, query="", diagram_type="flowchart"):
        parts = []
        web = self.call_agent("webclaw", f"search mermaid {diagram_type} diagram {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web))
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + str(data))
        return "\n".join(parts)

    def _generate_diagram(self, diagram_type, query, ctx=None):
        enhanced = f"Context:\n{ctx}\n\nTask: {query}" if ctx else query
        return self.engine.generate_with_llm(diagram_type, enhanced, self.llm)

    def handle(self, task):
        self.track_interaction()

        # Dict payload (agent-to-agent)
        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]:
                return {"status": "error", "result": f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        # String (CLI)
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Shared memory
            if cmd == "/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1)
                action = parts2[0]
                if action == "read" and len(parts2) > 1:
                    data, err = read_shared(parts2[1])
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action == "write" and len(parts2) > 1:
                    kv = parts2[1].split(":", 1)
                    if len(kv) == 2:
                        result = write_shared(kv[0], kv[1])
                    else:
                        result = "Usage: /shared write key:value"
                elif action == "read":
                    data, err = read_shared()
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                else:
                    result = "Usage: /shared [read [key]] [write key:value]"
                return {"status": "success", "result": str(result)}

            # Cross-agent delegation
            elif cmd == "/delegate" and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw", "interpretclaw", "docuclaw", "dataclaw", "webclaw",
                        "lawclaw", "mathematicaclaw", "langclaw", "claw_coder", "fileclaw",
                        "txclaw", "mediclaw", "liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else:
                    result = f"Unknown agent: {target}. Known: {', '.join(known)}"
                return {"status": "success", "result": str(result)}

            # List exports
            elif cmd == "/exports":
                from data_io import list_exports
                result = "Exported diagrams:\n" + list_exports()
                return {"status": "success", "result": str(result)}

            # Help and stats BEFORE diagram generation (no LLM needed)
            if cmd in ("/help",):
                result = "FlowClaw v5 - Constitutional Diagram Agent\n  DIAGRAMS:  /flowchart /sequence /architecture /mindmap\n  VIEW:      /view <query>\n  EXPORT:    /export <fmt> <query>  (png, svg, pdf, docx, md, html)\n  SHARED:    /shared read [key]  |  /shared write key:value\n  DELEGATE:  /delegate <agent> <task>\n  FILES:     /exports\n  /stats"
            elif cmd in ("/stats",):
                result = f"FlowClaw v5 | Engine+Viewer+Export+Delegate | Interactions: {self.state.get('interactions', 0)}"
            else:
                # Diagram generation
                if cmd in ("/flowchart", "flowchart"): diagram_type = "flowchart"
                elif cmd in ("/sequence", "sequence"): diagram_type = "sequence"
                elif cmd in ("/architecture", "architecture"): diagram_type = "architecture"
                elif cmd in ("/mindmap", "mindmap"): diagram_type = "mindmap"
                else: diagram_type = "flowchart"

                ctx = self._gather_context(query, diagram_type)
                code = self._generate_diagram(diagram_type, query, ctx)

                if cmd in ("/view", "view"):
                    self.viewer.view_in_browser(code, query)
                    result = f"Opened in browser.\n\n`mermaid\n{code}\n`"
                elif cmd in ("/export", "export"):
                    parts2 = args.split(maxsplit=1) if args else ["md", query]
                    fmt = parts2[0] if parts2[0] in ("png","svg","pdf","docx","md","html") else "md"
                    export_result = self.call_agent("fileclaw", f"/export {fmt} Mermaid: {query}\n\n`mermaid\n{code}\n`", timeout=30)
                    if export_result:
                        result = f"{export_result}\n\n`mermaid\n{code}\n`"
                    else:
                        output_dir = FLOWCLAW_DIR / "exports"
                        output_dir.mkdir(exist_ok=True)
                        path = output_dir / f"diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        self.docx_exporter.export(code, path, query)
                        result = f"Exported to {path}.docx\n\n`mermaid\n{code}\n`"
                else:
                    result = f"`mermaid\n{code}\n`"

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type") == "delegate":
                target = payload["target_agent"]
                cmd = payload.get("command", "")
                task_text = payload.get("payload", cmd)
                if isinstance(task_text, dict):
                    task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status": "success", "result": str(result or f"Delegated to {target}")}

            diag_type = payload.get("diagram_type", "flowchart")
            query = payload.get("query", "")
            flags = payload.get("flags", {})
            code = self._generate_diagram(diag_type, query)
            if flags.get("view"):
                self.viewer.view_in_browser(code, flags.get("title", query))
            if flags.get("export_format"):
                fmt = flags["export_format"]
                export_result = self.call_agent("fileclaw", f"/export {fmt} Mermaid: {query}\n\n`mermaid\n{code}\n`", timeout=30)
                result = f"{export_result}\n\n`mermaid\n{code}\n`" if export_result else f"`mermaid\n{code}\n`"
            else:
                result = f"`mermaid\n{code}\n`"
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = FlowClawAgent()

def process_task(task, agent=None):
    return _agent.handle(task)
