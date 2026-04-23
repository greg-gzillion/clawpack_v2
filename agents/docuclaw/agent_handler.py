"""A2A Handler for DocuClaw - Document Processing & Generation"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('docuclaw')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/create", "create") and query:
                result = self.ask_llm(f"Create a professional document. Include title, sections, and content. Format in Markdown. Topic: {query}")
            elif cmd in ("/letter", "letter") and query:
                result = self.ask_llm(f"Write a professional business letter. Include date, addresses, subject, body, signature. For: {query}")
            elif cmd in ("/report", "report") and query:
                result = self.ask_llm(f"Write a formal report with executive summary, findings, conclusions. For: {query}")
            elif cmd in ("/proposal", "proposal") and query:
                result = self.ask_llm(f"Write a business proposal with problem statement, solution, timeline, budget. For: {query}")
            elif cmd in ("/resume", "resume") and query:
                result = self.ask_llm(f"Create a professional resume/CV in Markdown format. For: {query}")
            elif cmd in ("/memo", "memo") and query:
                result = self.ask_llm(f"Write a business memo. Include TO, FROM, DATE, SUBJECT, body. For: {query}")
            elif cmd in ("/convert", "convert") and query:
                result = f"[CONVERT] DocuClaw supports: CSV, DOCX, HTML, JSON, Markdown, ODT, PDF, RTF, Text, XML\nRequest: {query}"
            elif cmd in ("/help",):
                result = "DocuClaw - Document Processor\n  /create <topic> - Create document\n  /letter <context> - Business letter\n  /report <topic> - Formal report\n  /proposal <topic> - Business proposal\n  /resume <details> - CV/Resume\n  /memo <content> - Business memo\n  /convert <format> - Convert documents\n  /stats"
            elif cmd in ("/stats",):
                result = f"DocuClaw | Document Processing | 10 Import Formats | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.ask_llm(f"Create a professional document in Markdown format for: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = DocuClawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
