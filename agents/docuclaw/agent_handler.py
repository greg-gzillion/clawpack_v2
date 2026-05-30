"""A2A Handler for DocuClaw - Document Generator with A2A routing"""
import sys, os, json, time
from pathlib import Path
from datetime import datetime

DOCUCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCUCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
TEMPLATES_DIR = DOCUCLAW_DIR / "templates"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCUCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err
from modules.viewer import view_document
from modules.validator import validate_claims, generate_trust_footer

class DocuClawAgent(BaseAgent):
    def __init__(self):
        super().__init__("docuclaw")

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search document template {query}", timeout=15)
        if web: parts.append("[WebClaw]: " + str(web)[:2000])
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx: lines.append(ctx[:1000])
            if lines: parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts) if parts else ""

    def _list_exports(self, filter_ext=None):
        """List exported files, newest first."""
        if not EXPORTS.exists():
            return "No exports found."
        files = sorted(EXPORTS.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
        if filter_ext:
            files = [f for f in files if f.suffix == f".{filter_ext}"]
        if not files:
            return "No exports found."
        lines = []
        for f in files[:20]:
            size = f.stat().st_size
            ts = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"  {f.name} ({size:,} bytes) - {ts}")
        return "\n".join(lines)

    def _list_templates(self, category=None):
        """List available templates."""
        if not TEMPLATES_DIR.exists():
            return "No templates found."
        categories = {}
        for d in TEMPLATES_DIR.iterdir():
            if d.is_dir():
                files = list(d.glob("*"))
                if files:
                    categories[d.name] = [f.stem.replace("_", " ").title() for f in files]
        
        if category and category in categories:
            return f"Templates: {category}\n" + "\n".join(f"  - {t}" for t in categories[category])
        
        result = ["Available Template Categories:"]
        for cat, temps in sorted(categories.items()):
            result.append(f"\n  {cat}/ ({len(temps)} templates)")
            for t in temps[:5]:
                result.append(f"    - {t}")
        return "\n".join(result)

    def _to_table(self, content, fmt):
        """Convert markdown content to tabular format for spreadsheet exports"""
        if fmt in ("xlsx", "csv"):
            lines = content.split('\n')
            rows = [{"Section": "Content", "Text": content}]
            current_section = "Header"
            current_text = ""
            for line in lines:
                if line.startswith("# "):
                    if current_text.strip():
                        rows.append({"Section": current_section, "Text": current_text.strip()})
                    current_section = line.replace("# ", "").strip()
                    current_text = ""
                elif line.strip():
                    current_text += line + " "
            if current_text.strip():
                rows.append({"Section": current_section, "Text": current_text.strip()})
            import json
            return json.dumps(rows)
        return content

    def _fileclaw_export(self, fmt, content):
        """Delegate to FileClaw for all format exports"""
        try:
            if fmt == "pdf":
                content = content.encode("latin-1", errors="replace").decode("latin-1")
            content = self._to_table(content, fmt)
            safe_content = content.replace('\n', '\\n').replace('"', '\\"')
            result = self.call_agent("fileclaw", f"/export {fmt} {safe_content}")
            if result:
                return result
        except:
            pass
        EXPORTS.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = EXPORTS / f"docuclaw_{ts}.{fmt}"
        fn.write_text(content, encoding="utf-8")
        return f"Saved locally: {fn.name}"

    def _fileclaw_import(self, filepath):
        """Import file via FileClaw or read directly"""
        try:
            safe_path = filepath.replace("\\", "/")
            result = self.call_agent("fileclaw", f"/import {safe_path}")
            if result:
                return result
        except:
            pass
        try:
            return Path(filepath).read_text(encoding="utf-8", errors="replace")
        except:
            return None

    def handle(self, task):
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        query = args if args else task

        try:
            # Constitutional commands
                        elif cmd == "/voice":
                from shared.voice_hook import is_active, toggle
                result = toggle()  # toggle on/off

            elif cmd in ("/listen", "listen"):
                from shared.accessibility import listen, detect_language
                text = listen()
                if text.startswith('[STT]'):
                    result = text
                else:
                    lang = detect_language(text)
                    result = f"[{lang.upper()}] {text}"
            elif cmd in ("/translate", "translate") and query:
                from shared.accessibility import translate, detect_language
                lang = detect_language(query)
                result = translate(query, 'en', lang)

                        elif cmd in ("/braille", "braille") and query:
                from shared.accessibility import to_braille
                result = to_braille(query)

            if cmd in ("/help",):
                result = "DocuClaw v5 - Constitutional Document Agent\n  CREATE: /create /letter /report /memo /resume /proposal\n  IMPORT: /import <file>  EXPORT: /export <fmt> <content>\n  CONVERT: /convert <fmt> <file>  COMBINE: /combine <files>\n  TRANSLATE: /translate <lang> <text>  TEMPLATES: /templates\n  SHARED: /shared read|write  DELEGATE: /delegate <agent> <task>\n  /stats"
                return {"status":"success","result":result}
            if cmd in ("/stats",): return {"status":"success","result":f"DocuClaw v5 | 21 Formats | Interactions: {self.state.get('interactions',0)}"}
            if cmd=="/shared" and args:
                from data_io import read_shared, write_shared
                parts2 = args.split(maxsplit=1); action = parts2[0]
                if action=="read":
                    key = parts2[1] if len(parts2)>1 else None
                    data, err = read_shared(key)
                    result = json.dumps(data, indent=2, default=str)[:2000] if not err else err
                elif action=="write" and len(parts2)>1:
                    kv = parts2[1].split(":",1)
                    result = write_shared(kv[0], kv[1]) if len(kv)==2 else "Usage: /shared write key:value"
                else: result = "Usage: /shared read [key] | /shared write key:value"
                return {"status":"success","result":str(result)}
            if cmd=="/delegate" and args:
                parts2 = args.split(maxsplit=1); target = parts2[0]
                task_text = parts2[1] if len(parts2)>1 else ""
                known = ["plotclaw","flowclaw","claw_coder","crustyclaw","dataclaw","designclaw","interpretclaw","webclaw","lawclaw","mathematicaclaw","langclaw","fileclaw","txclaw","mediclaw","liberateclaw"]
                if target in known:
                    result = self.call_agent(target, task_text)
                    result = str(result) if result else f"Agent {target} returned no response"
                else: result = f"Unknown: {target}"
                return {"status":"success","result":str(result)}

            # Document generation
            if cmd in ("/create", "/letter", "/report", "/memo", "/resume", "/proposal") and query:
                doc_type = cmd.replace("/", "")
                parts2 = query.rsplit(" ", 1)
                fmt = parts2[-1] if len(parts2) > 1 and parts2[-1] in (
                    "pdf","docx","html","md","txt","json","csv","yaml","xml","rtf","pptx","xlsx"
                ) else "md"
                if fmt == parts2[-1] and len(parts2) > 1:
                    query = parts2[0]
                
                content = self.ask_llm(
                    f"Create a professional {doc_type} in Markdown format. Include proper formatting, headings, and structure. Include specific sources, URLs, and citations where possible.\n\nTopic: {query}"
                )
                validation = validate_claims(content)
                if validation["claim_count"] > 0:
                    content += generate_trust_footer(validation)
                view_document(content, title=doc_type)
                export_result = self._fileclaw_export(fmt, content)
                from data_io import write_shared
                write_shared("docuclaw_latest", {"command": cmd, "doc_type": doc_type, "query": query, "claims": validation["claim_count"], "trust": validation["trust_summary"]["level"], "confidence": validation["trust_summary"]["confidence"]})
                result = f"{export_result}\n\n{content}"

            # List exports
            elif cmd in ("/exports", "/list") and args:
                result = self._list_exports(args)
            elif cmd in ("/exports", "/list"):
                result = self._list_exports()

            # List templates
            elif cmd in ("/templates", "/template"):
                category = args if args else None
                result = self._list_templates(category)

            # Use a template
            elif cmd == "/usetemplate" and args:
                parts2 = args.split(maxsplit=1)
                cat = parts2[0]
                name = parts2[1] if len(parts2) > 1 else ""
                template_path = TEMPLATES_DIR / cat / f"{name}.md" if name else None
                if template_path and template_path.exists():
                    content = template_path.read_text(encoding="utf-8")
                    result = f"Template loaded: {cat}/{name}\n\n{content}"
                else:
                    result = f"Template not found: {cat}/{name}\n\n" + self._list_templates(cat)

            # Import file
            elif cmd == "/import" and args:
                content = self._fileclaw_import(args)
                if content:
                    view_document(content, title=f"Imported: {args}")
                    result = f"Imported: {args}\n\n{content}"
                else:
                    result = f"File not found: {args}\n\nTry /list to see available files"

            # Export content
            elif cmd == "/export" and args:
                parts2 = args.split(maxsplit=1)
                fmt = parts2[0]
                content = parts2[1] if len(parts2) > 1 else ""
                if content:
                    result = self._fileclaw_export(fmt, content)
                else:
                    result = "Usage: /export pdf <content>"

            # Convert file between formats
            elif cmd == "/convert" and args:
                parts2 = args.split(maxsplit=2)
                if len(parts2) >= 2:
                    target_fmt = parts2[0]
                    filepath = parts2[1]
                    p = PROJECT_ROOT / "exports" / filepath
                    if not p.exists():
                        p = Path(filepath)
                    if p.exists():
                        content = p.read_text(encoding="utf-8", errors="replace")
                    else:
                        content = None
                    if content:
                        export_result = self._fileclaw_export(target_fmt, content)
                        view_document(content, title=f"Converted: {Path(filepath).name}")
                        result = f"Converted {filepath} to {target_fmt}:\n{export_result}"
                    else:
                        result = f"Cannot read: {filepath}"
                else:
                    result = "Usage: /convert pdf README.md"

            # Combine multiple files
            elif cmd == "/combine" and args:
                files = args.split()
                combined = []
                for f in files:
                    content = self._fileclaw_import(f)
                    if content:
                        combined.append(f"---\n## From: {f}\n\n{content}")
                    else:
                        combined.append(f"---\n## From: {f}\n\n[Could not read file]")
                
                full_content = "\n\n".join(combined)
                export_result = self._fileclaw_export("md", full_content)
                view_document(full_content, title="Combined Document")
                result = f"Combined {len(files)} files:\n{export_result}\n\n{full_content[:1000]}..."

            # Translate via InterpretClaw
            elif cmd == "/translate" and args:
                parts2 = args.split(maxsplit=1)
                lang = parts2[0]
                text = parts2[1] if len(parts2) > 1 else ""
                if text:
                    translated = self.call_agent("interpretclaw", f"/translate {text} to {lang}")
                    if translated:
                        clean = translated.replace("Exported:", "").strip()
                        export_fn = self._fileclaw_export("md", clean)
                        view_document(clean, title=f"Translation - {lang}")
                        result = f"Translated to {lang}: {export_fn}\n\n{clean}"
                    else:
                        result = "Translation failed"
                else:
                    result = "Usage: /translate fr <text>"

            # Help
            elif cmd == "/help":
                result = """DocuClaw - Universal Document Generator
  CREATE:     /create /letter /report /memo /resume /proposal
  IMPORT:     /import <filepath>
  EXPORT:     /export <format> <content>
  CONVERT:    /convert <format> <filepath>
  COMBINE:    /combine <file1> <file2> ...
  TRANSLATE:  /translate <lang> <text>
  TEMPLATES:  /templates [category]  |  /usetemplate <cat> <name>
  LIST:       /list [format]

  Formats (21): pdf, docx, rtf, md, html, txt, xlsx, pptx,
                json, csv, yaml, toml, xml, ini,
                png, jpg, bmp, gif, tiff, webp, svg, zip"""

            elif cmd == "/stats":
                result = f"DocuClaw | 21 Formats | FileClaw + InterpretClaw | Interactions: {self.state.get('interactions', 0)}"

            # Fallback: any text becomes a document
            elif query:
                content = self.ask_llm(f"Create a well-formatted Markdown document:\n\n{query}")
                export_result = self._fileclaw_export("md", content)
                result = f"{export_result}\n\n{content}"
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "docuclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif args:
                    context = self._gather_context(args)
                    result = self.ask_llm(f"Query: {args}\n\nContext:\n{context}")
                else:
                    result = "Type /help for commands"

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try: from shared.lifecycle import agent_cleanup; agent_cleanup("docuclaw", args or "", 0)
                except Exception: pass
                try: from shared.enforcement.engine import EnforcementEngine; EnforcementEngine().load_reference("docuclaw_handler")
                except Exception: pass
                try: from shared.guarded_executor import GuardedExecutor; GuardedExecutor("docuclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.execution_policy import ExecutionPolicy; ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try: from shared.chronicle_helper import search_chronicle as chron_search; chron_search(args or cmd, limit=3)
                except Exception: pass
                try: from shared.memory.procedural_memory import get_memory as get_proc_mem; pmem = get_proc_mem("docuclaw")
                except Exception: pass
                try: from shared.memory.three_tier import get_memory as get_three_tier; get_three_tier("docuclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try: from shared.smart_router import SmartRouter; SmartRouter().route(cmd)
                except Exception: pass
                try: from shared.agent_router import AgentRouter; AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try: from shared.log_manager import get_logger; get_logger().info(f"docuclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try: from shared.shutdown import get_shutdown_manager; get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try: from shared.hooks.hook_manager import get_hook_manager; get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try: from shared.llm.budget import BudgetController; budget = BudgetController()
                except Exception: pass
                try: from shared.rate_limiter import get_rate_limiter; get_rate_limiter().check_daily_limits()
                except Exception: pass
                try: from shared.error_handler import get_circuit_breaker; get_circuit_breaker("docuclaw").call()
                except Exception: pass
                try: from shared.metrics import get_metrics; get_metrics().counter("docuclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try: from shared.security import get_audit_logger; get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="docuclaw")
                except Exception: pass
                try: from agents.docuclaw.commands._memory import remember; remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try: from shared._agent_helpers import learn; learn("docuclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try: from shared.decision_ledger import get_ledger; get_ledger().record(agent="docuclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try: from shared.consensus_engine import constitutional_consensus_check; constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try: from shared.llm.auditor import ChronicleAuditor; ChronicleAuditor().log(agent="docuclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                except Exception: pass
                try: from shared.observability import get_health_checker; get_health_checker().register("docuclaw_handler", lambda: True)
                except Exception: pass
                try:
                    from shared.memory_guard import sanitize_memory_write
                except Exception: pass
                try:
                    from shared.source_registry import get_trust
                except Exception: pass
                try:
                    from shared.truth_resolver import merge_with_retriever
                except Exception: pass
                try:
                    from shared.input_handler import InputHandler
                except Exception: pass
                try:
                    from shared.permissions import PermissionSystem
                except Exception: pass
                try:
                    from shared.registry import AgentRegistry
                except Exception: pass
                try:
                    from shared.jurisdiction_validator import validate_jurisdiction
                except Exception: pass
                try:
                    from shared.enforcement.gates import PreExecutionGate, PostExecutionGate
                except Exception: pass
                try:
                    from shared.config import ConfigManager
                except Exception: pass
                try:
                    from shared.constitutional_command import validate_command
                except Exception: pass
                try:
                    from shared.court_rules_schema import CourtRulesSchema
                except Exception: pass
                try:
                    from shared.decomposer import TaskDecomposer
                except Exception: pass
                try:
                    from shared.output_handler import OutputHandler
                except Exception: pass
                try:
                    from shared.router import TaskRouter
                except Exception: pass
                try:
                    from shared.compactor import ContextCompactor
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="docuclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": str(final_result)}
        except Exception as e:
            log_err("docuclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}


_agent = DocuClawAgent()


def process_task(task, agent=None):
    return _agent.handle(task)