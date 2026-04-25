"""A2A Handler for ClawCoder - Code Generation + Auto-Export via FileClaw"""
import sys, os, requests
from pathlib import Path
from datetime import datetime

CLAW_CODER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CLAW_CODER_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))

from agents.llmclaw.agent_handler import process_task as _llm
from agents.webclaw.providers.webclaw_provider import WebclawProvider
webclaw = WebclawProvider()

# Language to file extension (39 languages from claw_coder/languages/)
LANG_EXT = {
    "python": ".py", "rust": ".rs", "go": ".go", "javascript": ".js", "typescript": ".ts",
    "java": ".java", "c": ".c", "c++": ".cpp", "cpp": ".cpp", "csharp": ".cs", "c#": ".cs",
    "ruby": ".rb", "php": ".php", "swift": ".swift", "kotlin": ".kt", "scala": ".scala",
    "r": ".r", "julia": ".jl", "lua": ".lua", "perl": ".pl", "haskell": ".hs",
    "clojure": ".clj", "elixir": ".ex", "erlang": ".erl", "dart": ".dart",
    "bash": ".sh", "batch": ".bat", "powershell": ".ps1", "sql": ".sql",
    "html": ".html", "css": ".css", "yaml": ".yaml", "json": ".json", "xml": ".xml",
    "assembly": ".asm", "fortran": ".f90", "cobol": ".cbl", "groovy": ".groovy",
    "nim": ".nim", "zig": ".zig", "vhdl": ".vhd", "matlab": ".m", "objectivec": ".m",
    "makefile": ".mk"
}

def _detect_lang(task):
    t = task.lower()
    for lang in sorted(LANG_EXT.keys(), key=len, reverse=True):
        if lang in t:
            return lang
    return ""

def _save_code(code, lang, task):
    """Save code to exports/ with correct extension via FileClaw"""
    ext = LANG_EXT.get(lang, ".txt")
    # Extract first block if markdown-wrapped
    if "```" in code:
        blocks = code.split("```")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                block = block.split("\n", 1)[1] if "\n" in block else block
                code = block
                break
    # Clean filename from task
    name = task[:40].replace(" ", "_").replace("/", "").replace(chr(92), "")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"{name}_{ts}{ext}"
    path = EXPORTS / fn
    EXPORTS.mkdir(exist_ok=True)
    path.write_text(code, encoding="utf-8")
    return fn

def process_task(task, agent=None):
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    query = args if args else task

    try:
        if cmd in ("/code", "code") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Write clean, well-commented code. Return ONLY the code, no explanation. References: {ctx}\nTask: {query}").get("result","")
            lang = _detect_lang(query)
            if lang:
                fn = _save_code(result, lang, query)
                result = f"Saved: {fn}\n\n{result[:500]}"
            else:
                result = f"[No language detected - code not saved]\n\n{result[:500]}"
        elif cmd in ("/explain", "explain") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Explain this code. References: {ctx}\nCode: {query}").get("result","")
        elif cmd in ("/debug", "debug") and query:
            result = _llm(f"/llm Debug and fix this code: {query}").get("result","")
        elif cmd in ("/review", "review") and query:
            result = _llm(f"/llm Code review: {query}").get("result","")
        elif cmd in ("/tutorial", "tutorial") and query:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Tutorial. References: {ctx}\nTopic: {query}").get("result","")
        elif cmd in ("/find", "find") and query:
            result = webclaw.search_with_context(f"claw_coder {query}", max_results=10)
        elif cmd in ("/help",):
            result = "ClawCoder - 39 Languages\n  /code <lang> <task> - Generate + auto-save\n  /explain /debug /review /tutorial /find\n  Files saved to exports/ with correct extension"
        elif cmd in ("/stats",):
            result = f"ClawCoder | 39 Languages | 1,566 References | Auto-save to exports/"
        else:
            ctx = webclaw.search_with_context(f"claw_coder {query}", max_results=3)
            result = _llm(f"/llm Context: {ctx}\nTask: {query}").get("result","")
        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
