"""A2A Handler for FlowClaw - Diagram & Flowchart Generator"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class FlowClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('flowclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/flowchart", "flowchart") and query:
                result = self.ask_llm(f"Generate a valid Mermaid flowchart TD diagram. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/mindmap", "mindmap") and query:
                result = self.ask_llm(f"Generate a valid Mermaid mindmap diagram. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/sequence", "sequence") and query:
                result = self.ask_llm(f"Generate a valid Mermaid sequenceDiagram. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/gantt", "gantt") and query:
                result = self.ask_llm(f"Generate a valid Mermaid gantt chart. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/class", "class") and query:
                result = self.ask_llm(f"Generate a valid Mermaid classDiagram. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/architecture", "architecture") and query:
                result = self.ask_llm(f"Generate a valid Mermaid architecture diagram. Return ONLY Mermaid code:\n\n{query}")
            elif cmd in ("/help",):
                result = "FlowClaw - Diagram Generator\n  /flowchart <desc>\n  /mindmap <desc>\n  /sequence <desc>\n  /gantt <desc>\n  /class <desc>\n  /architecture <desc>\n  /stats"
            elif cmd in ("/stats",):
                result = f"FlowClaw | Mermaid Diagrams | Flowchart/Mindmap/Sequence/Gantt | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Generate a Mermaid diagram for this. Return ONLY valid Mermaid code:\n\n{query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = FlowClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
