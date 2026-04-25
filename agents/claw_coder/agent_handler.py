"""A2A Handler for ClawCoder - 39 Languages Full Stack"""
import sys, os
from pathlib import Path
from datetime import datetime
CODER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CODER_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(CODER_DIR))
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "llmclaw"))
from shared.base_agent import BaseAgent
from commands.llm_enhanced import run as llm_run

LANG_EXT = {"python":".py","rust":".rs","go":".go","javascript":".js","typescript":".ts","java":".java","c":".c","cpp":".cpp","csharp":".cs","ruby":".rb","php":".php","swift":".swift","kotlin":".kt","scala":".scala","r":".r","julia":".jl","lua":".lua","perl":".pl","haskell":".hs","clojure":".clj","elixir":".ex","erlang":".erl","dart":".dart","bash":".sh","powershell":".ps1","sql":".sql","html":".html","css":".css","yaml":".yaml","json":".json","xml":".xml","assembly":".asm","fortran":".f90","cobol":".cbl","groovy":".groovy","nim":".nim","zig":".zig","matlab":".m","makefile":".mk"}

def _detect_lang(task):
    t = task.lower()
    for lang in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if lang in t: return lang
    return "python"

class ClawCoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("claw_coder")

    def _save_code(self, code, lang, task):
        EXPORTS.mkdir(exist_ok=True)
        if "\`\`\`" in code:
            blocks = code.split("\`\`\`")
            for i, block in enumerate(blocks):
                if i % 2 == 1:
                    block = block.split("\n", 1)[1] if "\n" in block else block
                    code = block
                    break
        ext = LANG_EXT.get(lang, ".txt")
        name = task[:40].replace(" ", "_").replace(chr(92), "").replace("/", "")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = name + "_" + ts + ext
        (EXPORTS / fn).write_text(code, encoding="utf-8")
        return fn

    def handle(self, task):
        self.track_interaction()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task
        try:
            ctx = ""
            try: ctx = self.search_web("programming " + query, max_results=3)
            except: pass
            if cmd in ("/code",) and query:
                lang = _detect_lang(query)
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nWrite clean " + lang + " code. " + query)
                fn = self._save_code(result, lang, query)
                result = "Saved: " + fn + "\n\n" + result[:800]
            elif cmd in ("/explain",) and query:
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nExplain this code: " + query)
            elif cmd in ("/debug",) and query:
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nDebug and fix: " + query)
            elif cmd in ("/review",) and query:
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nCode review: " + query)
            elif cmd in ("/tutorial",) and query:
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nTutorial on: " + query)
            elif cmd in ("/find",) and query:
                result = self.search_web(query, max_results=10)
            elif cmd == "/help":
                result = "ClawCoder - 39 Languages\n  /code <lang> <task> - Generate + auto-save\n  /explain /debug /review /tutorial /find\n  BaseAgent + LLMClaw + WebClaw"
            elif cmd == "/stats":
                result = "ClawCoder | 39 Languages | BaseAgent + LLMClaw + WebClaw | Interactions: " + str(self.state.get("interactions", 0))
            else:
                result = llm_run("Indexed References:\n" + ctx[:2000] + "\n\nProgramming: " + query)
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

_agent = ClawCoderAgent()
def process_task(task, agent=None):
    return _agent.handle(task)
