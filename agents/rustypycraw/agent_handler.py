"""A2A Handler for RustyPyCraw - Python/Rust Interop Analyzer with A2A Routing"""
import sys
from pathlib import Path

RUSTYPYCRAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RUSTYPYCRAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(RUSTYPYCRAW_DIR))

from shared.base_agent import BaseAgent
from modules.scanner.code_scanner import CodeScanner
from modules.analyzer.code_analyzer import CodeAnalyzer

class RustyPyCrawAgent(BaseAgent):
    def __init__(self):
        super().__init__("rustypycraw")
        self.scanner = CodeScanner()
        self.analyzer = CodeAnalyzer()

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search rust python interop {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + web[:600])
        data = self.call_agent("dataclaw", f"search {query}", timeout=15)
        if data: parts.append("[DataClaw]: " + data[:600])
        rust = self.call_agent("crustyclaw", f"/explain {query}", timeout=15)
        if rust: parts.append("[CrustyClaw]: " + rust[:600])
        coder = self.call_agent("claw_coder", f"/explain {query}", timeout=15)
        if coder: parts.append("[ClawCoder]: " + coder[:600])
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            if cmd in ("/scan", "scan") and query:
                result = self.scanner.scan(query)
                result_str = f"Scanned: {query}\n"
                if "error" in result:
                    result_str = str(result)
                elif "languages" in result:
                    for lang, stats in result.get("languages", {}).items():
                        result_str += f"  {lang}: {stats['files']} files, {stats['lines']} lines, {stats['functions']} functions\n"
                    result_str += f"\nTotal: {result['files']} files, {result['lines']} lines"
                else:
                    result_str = f"File: {result.get('file')}\nLanguage: {result.get('language')}\nLines: {result.get('lines')}\nFunctions: {result.get('functions', 0)}"
                result = result_str
                
            elif cmd in ("/analyze", "analyze") and query:
                analysis = self.analyzer.analyze(query, "interop")
                result = f"Analysis: {query}\n"
                if "results" in analysis:
                    for r in analysis["results"]:
                        result += f"\n--- {r.get('file')} ---\n"
                        if "rust_portable" in r:
                            result += f"Rust-portable: {r['rust_portable'].get('portable')}\n"
                            for issue in r['rust_portable'].get('issues', []):
                                result += f"  - {issue}\n"
                        if "unsafe_patterns" in r:
                            for p in r['unsafe_patterns']:
                                result += f"  - {p}\n"
                else:
                    result = str(analysis)
                    
            elif cmd in ("/compare", "compare") and query:
                paths = query.split()
                if len(paths) >= 2:
                    comparison = self.scanner.compare(paths[0], paths[1])
                    result = f"Python ({paths[0]}): {comparison.get('python', {}).get('lines', 0)} lines, {comparison.get('python', {}).get('functions', 0)} functions\n"
                    result += f"Rust ({paths[1]}): {comparison.get('rust', {}).get('lines', 0)} lines, {comparison.get('rust', {}).get('functions', 0)} functions"
                else:
                    result = "Usage: /compare <python_file> <rust_file>"
                    
            elif cmd in ("/help",):
                result = "RustyPyCraw - Python/Rust Interop\n  /scan <path> - Scan codebase\n  /analyze <path> - Analyze interop\n  /compare <py> <rs> - Compare Python/Rust\n  /stats\n  Uses: WebClaw + DataClaw + CrustyClaw + ClawCoder -> LLMClaw -> FileClaw"
            elif cmd in ("/stats",):
                result = f"RustyPyCraw | Python/Rust Interop | Scanner + Analyzer | Interactions: {self.state.get('interactions', 0)}"
            else:
                ctx = self._gather_context(query)
                result = self.ask_llm(f"Context from specialists:\n{ctx}\n\nPython/Rust interop analysis: {query}")

            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = RustyPyCrawAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
