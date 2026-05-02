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
from exporters.base_exporter import DocxExporter, PdfExporter, HtmlExporter, MarkdownExporter, JsonExporter

class LLMAdapter:
    def __init__(self, agent):
        self.agent = agent
    def chat_sync(self, prompt, task_type="orchestration", **kw):
        return self.agent.ask_llm(prompt, task_type=task_type)

class FlowClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("flowclaw")
        self.engine = DiagramEngine()
        self.viewer = DiagramViewer()
        self.exporters = {
            "docx": DocxExporter(), "pdf": PdfExporter(),
            "html": HtmlExporter(), "md": MarkdownExporter(),
            "json": JsonExporter(),
        }
        self.llm = LLMAdapter(self)

    def _gather_context(self, query="", diagram_type="flowchart"):
        parts = []
        web = self.call_agent("webclaw", f"search mermaid {diagram_type} {query}", timeout=10)
        if web: parts.append(str(web)[:500])
        data = self.call_agent("dataclaw", f"search {query}", timeout=10)
        if data: parts.append(str(data)[:500])
        return "\n".join(parts)

    def _generate_diagram(self, diagram_type, query, ctx=None):
        enhanced = f"Context:\n{ctx}\n\nTask: {query}" if ctx else query
        return self.engine.generate_with_llm(diagram_type, enhanced, self.llm)

    def handle(self, task):
        self.track_interaction()

        if isinstance(task, dict):
            from schema import validate
            validated = validate(task)
            if not validated["valid"]:
                return {"status": "error", "result": f"Schema: {validated['error']}"}
            return self._execute(validated["payload"])

        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/help",):
                return {"status": "success", "result": "FlowClaw v5\n  DIAGRAMS: /flowchart /sequence /architecture /mindmap\n  EXPORT: /export <fmt> <query>\n  SHARED: /shared read|write\n  DELEGATE: /delegate <agent> <task>\n  /stats"}

            if cmd in ("/stats",):
                return {"status": "success", "result": f"FlowClaw v5 | Interactions: {self.state.get('interactions', 0)}"}

            if cmd == "/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1)
                action = parts2[0]
                if action == "read":
                    key = parts2[1] if len(parts2) > 1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action == "write" and len(parts2) > 1:
                    kv = parts2[1].split(":", 1)
                    result = write_shared(kv[0], kv[1]) if len(kv) == 2 else "Usage: /shared write key:value"
                else:
                    result = "Usage: /shared read [key] | /shared write key:value"
                return {"status": "success", "result": str(result)}

            if cmd == "/delegate" and args:
                parts2 = args.split(maxsplit=1)
                target = parts2[0]
                task_text = parts2[1] if len(parts2) > 1 else ""
                known = ["plotclaw","interpretclaw","docuclaw","dataclaw","webclaw","lawclaw","mathematicaclaw","langclaw","claw_coder","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else:
                    result = f"Unknown: {target}"
                return {"status": "success", "result": str(result)}

            if cmd == "/exports":
                from data_io import list_exports
                return {"status": "success", "result": "Exports:\n" + list_exports()}

            # Diagram generation - opens browser by default
            diagram_type = "flowchart"
            if cmd in ("/flowchart",): diagram_type = "flowchart"
            elif cmd in ("/sequence",): diagram_type = "sequence"
            elif cmd in ("/architecture",): diagram_type = "architecture"
            elif cmd in ("/mindmap",): diagram_type = "mindmap"

            code = self._generate_diagram(diagram_type, query)

            if cmd in ("/export",):
                parts2 = args.split(maxsplit=1) if args else ["md", query]
                fmt = parts2[0] if parts2[0] in ("png","svg","pdf","docx","md","html","json") else "md"
                er = self.call_agent("fileclaw", f"/export {fmt} Mermaid: {query}\n\n`mermaid\n{code}\n`", timeout=30)
                result = f"{er}\n\n`mermaid\n{code}\n`" if er else f"`mermaid\n{code}\n`"
            else:
                try:
                    import subprocess, tempfile
                    html = self.viewer._build_html(code, query)
                    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
                    tmp.write(html)
                    tmp.close()
                    subprocess.Popen(['cmd', '/c', 'start', '', tmp.name], shell=True)
                    result = f"Opened in browser.\n\n`mermaid\n{code}\n`"
                except Exception as e:
                    result = f"`mermaid\n{code}\n`"

            from data_io import write_shared
            write_shared("flowclaw_latest", {"type": diagram_type, "query": query, "code": code})

            return {"status": "success", "result": str(result)}

        except Exception as e:
            return {"status": "error", "result": str(e)}

    def _execute(self, payload):
        try:
            if payload.get("type") == "delegate":
                target = payload["target_agent"]
                task_text = payload.get("payload", payload.get("command", ""))
                if isinstance(task_text, dict):
                    task_text = json.dumps(task_text)
                result = self.call_agent(target, str(task_text))
                return {"status": "success", "result": str(result or f"Delegated to {target}")}

            diag_type = payload.get("diagram_type", "flowchart")
            query = payload.get("query", "")
            flags = payload.get("flags", {})
            code = self._generate_diagram(diag_type, query)

            if not flags.get("export_format"):
                try:
                    import subprocess, tempfile
                    html = self.viewer._build_html(code, flags.get("title", query))
                    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
                    tmp.write(html)
                    tmp.close()
                    subprocess.Popen(['cmd', '/c', 'start', '', tmp.name], shell=True)
                except:
                    pass

            result = f"`mermaid\n{code}\n`"
            return {"status": "success", "result": str(result)}

        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = FlowClawAgent()

def process_task(task, agent=None):
    return _agent.handle(task)
