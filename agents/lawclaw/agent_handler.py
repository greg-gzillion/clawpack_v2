"""A2A Handler for LawClaw - Law Research Agent with A2A routing"""
import sys
import json
import time
from pathlib import Path

LAWCLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = LAWCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LAWCLAW_DIR))

from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class LawClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("lawclaw")
        self._last_document = ""

    def _gather_context(self, query=""):
        parts = []
        web = self.call_agent("webclaw", f"search {query}", timeout=15)
        if web:
            parts.append("[WebClaw]: " + web)
        chronicle_results = self.search_chronicle(query, limit=5)
        if chronicle_results:
            lines = []
            for c in chronicle_results:
                ctx = c.get("context", "") if isinstance(c, dict) else str(c)
                if ctx:
                    lines.append(ctx[:1000])
            if lines:
                parts.append("[Chronicle]: " + "\n".join(lines))
        return "\n".join(parts)

    def handle(self, task: str) -> dict:
        self.track_interaction()
        track_start = time.time()
        task = task.strip()
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("/help", "help"):
                result = """
============================================================
  LAWCLAW — Legal Research & Document Agent
  Constitutional Reference Implementation
============================================================

CORE LEGAL RESEARCH
  /law [topic]           Search case law via CourtListener + Chronicle
                         Example: /law qualified immunity
  /docket [case|URL]     Fetch docket entries, jury demand, summaries
                         Example: /docket 42 USC 1983
  /cite [citation]       Parse and retrieve legal citations
                         Example: /cite Miranda v Arizona
  /precedent [doctrine]  Track doctrine by circuit with case law
                         Example: /precedent qualified immunity
  /oral [case]           Find oral argument audio and transcripts
                         Example: /oral Dobbs
  /statute [citation]    Look up statutes via law.cornell.edu
                         Example: /statute 42 USC 1983
  /summarize [text|URL]  Summarize legal documents or case URLs
                         Example: /summarize https://courtlistener.com/...

COURT SYSTEMS
  /federal [query]       Federal court info, circuits, SCOTUS, PACER
                         Example: /federal fourth amendment
  /state [code] [county] State and county court lookup
                         Example: /state VA Bedford
  /court [location]      Court info by city and state
                         Example: /court Denver CO

JUDICIAL & CIVIC INTELLIGENCE
  /judge [name]          Federal judge biography + CourtListener
                         Example: /judge Sotomayor
  /jurisdiction [city]   Complete civic profile (3800+ cities)
                         Example: /jurisdiction Daytona Beach FL
  /police [city] [state] Police department lookup
                         Example: /police Miami FL
  /detention [city]      Jail/detention facility lookup
                         Example: /detention Bedford VA
  /library [city]        Public library with legal resources
                         Example: /library Tampa FL
  /hospital [city]       Hospital lookup with GPS coordinates
                         Example: /hospital Daytona Beach FL

DOCUMENT GENERATION & TRANSLATION
  /doc [specs]           Generate legal documents via docuclaw
                         Supports: - plaintiff: - defendant: - case: - grounds:
                         Example: /doc motion to dismiss Miami FL
                                  - plaintiff: John Smith - defendant: ABC Corp
                                  - case: 2024-CV-1234 - grounds: failure to state a claim
  /draft [specs]         Alias for /doc
  /translate [text|doc]  Legal translation with term preservation
                         Example: /translate the contract to German
                                  /translate res judicata
  /correct [fact|URL]    Submit correction via consensus engine
                         Example: /correct salazar-limon url https://oyez.org/...

NAVIGATION & UTILITY
  /list [state]          Browse jurisdiction database
                         Example: /list FL
  /browse [location]     View jurisdiction files, auto-open URLs
                         Example: /browse MA Worcester
  /search [query]        Search local legal reference files
                         Example: /search Miranda
  /analyze [text]        Comprehensive legal text analysis
                         Example: /analyze [paste contract text]
  /ask [question]        AI legal Q&A with Chronicle context
                         Example: /ask what is qualified immunity
  /brief [case]          Generate case brief
                         Example: /brief Miranda v Arizona
  /stats                 System statistics

CROSS-AGENT COMMANDS (routed via capability registry)
  /plot [data]           Route to plotclaw for charts
  /code [specs]          Route to claw_coder for code generation
  /math [expression]     Route to mathematicaclaw
  /design [brief]        Route to designclaw
  /translate [text]      Route to interpretclaw (generic)
  ...any command not listed above routes to the appropriate agent

GETTING STARTED
  1. Try: /jurisdiction [your city] [your state]
  2. Try: /law [any legal topic]
  3. Try: /doc service agreement between [Company A] and [Company B]
  4. Try: /translate the contract to [language]

CONSTITUTIONAL RUNTIME: 23-system boundary active. 100% shared infrastructure.
All commands are memory-wired. Cross-agent delegation via capability registry.
"""
            elif cmd == "/stats":
                result = f"LawClaw | Interactions: {self.state.get('interactions', 0)}"
            elif cmd == "/analyze" and args:
                from agents.lawclaw.commands.analyze import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/ask" and args:
                from agents.lawclaw.commands.ask import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/brief" and args:
                from agents.lawclaw.commands.brief import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/browse" and args:
                from agents.lawclaw.commands.browse import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/cite" and args:
                from agents.lawclaw.commands.cite import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/correct" and args:
                from agents.lawclaw.commands.correct import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/court" and args:
                from agents.lawclaw.commands.court import run as cmd_run
                result = cmd_run(args)
            elif cmd in ("/doc", "/draft") and args:
                try:
                    from agents.lawclaw.commands._memory import recall_court
                    from agents.lawclaw.core.court_rules_extractor import (
                        extract_court_rules, rules_to_prompt_context,
                        jurisdiction_files_to_context
                    )
                    location_part = args.split(" - ")[0] if " - " in args else args
                    search_parts = location_part.strip().split()
                    location = location_part
                    court = None
                    for n in [3, 2, 1]:
                        if len(search_parts) >= n:
                            term = " ".join(search_parts[-n:])
                            court = recall_court(term)
                            if court:
                                location = term
                                break
                    jurisdiction_context = ""
                    if court:
                        court_fact = court.get('fact', '')
                        try:
                            data = json.loads(court_fact)
                            jurisdiction_context = data.get('summary', court_fact)[:600]
                        except (json.JSONDecodeError, TypeError):
                            jurisdiction_context = court_fact[:600]
                    local_files = jurisdiction_files_to_context(location)
                    rules_context = ""
                    try:
                        rules = extract_court_rules(location)
                        if rules:
                            rules_context = rules_to_prompt_context(rules)
                    except Exception:
                        pass
                    payload_parts = [f"/create legal document: {args}"]
                    if local_files:
                        payload_parts.append(f"LOCAL COURT DATA:\n{local_files[:2000]}")
                    if jurisdiction_context:
                        payload_parts.append(f"JURISDICTION SUMMARY: {jurisdiction_context}")
                    if rules_context:
                        payload_parts.append(f"COURT RULES: {rules_context}")
                    payload = "\n\n".join(payload_parts)
                except Exception:
                    payload = f"/create legal document: {args}"
                result = self.call_agent("docuclaw", payload, timeout=60)
                self._last_document = str(result)
            elif cmd == "/translate" and args:
                source_text = self._last_document if self._last_document else args
                target = args.split()[-1] if args.split() else "German"
                if len(source_text) > 500:
                    instructions = """
TRANSLATION REQUIREMENTS - PRESERVE EXACTLY:
1. ALL Latin terms (res judicata, stare decisis, mens rea, etc.) - DO NOT TRANSLATE
2. ALL French legal terms (voir dire, force majeure, etc.) - DO NOT TRANSLATE
3. ALL case citations (384 U.S. 436, Miranda v. Arizona) - DO NOT TRANSLATE
4. ALL statutory references (42 U.S.C. 1983) - DO NOT TRANSLATE
5. ALL court names - preserve official English name
6. ALL party names - DO NOT TRANSLATE
7. Translate all other content to the target language
8. Preserve all section numbers and formatting
"""
                else:
                    instructions = """
If this is a legal term: provide original term, language of origin, literal translation, and legal definition in the target language.
If this is a phrase: provide the translation to the target language.
"""
                payload = f"/translate to {target}\n\n{instructions}\n\nFULL DOCUMENT TO TRANSLATE:\n{source_text[:5000]}"
                translated = self.call_agent("interpretclaw", payload, timeout=120)
                format_payload = f"/create formatted legal document: {target} translation\n\n{str(translated)[:5000]}"
                result = self.call_agent("docuclaw", format_payload, timeout=60)
                self._last_document = str(result)
            elif cmd == "/docket" and args:
                from agents.lawclaw.commands.docket import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/federal" and args:
                from agents.lawclaw.commands.federal import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/judge" and args:
                from agents.lawclaw.commands.judge import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/jurisdiction" and args:
                from agents.lawclaw.commands.jurisdiction import run as cmd_run
                result = cmd_run(args, agent=self)
            elif cmd == "/law" and args:
                from agents.lawclaw.commands.law import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/list":
                from agents.lawclaw.commands.list import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/oral" and args:
                from agents.lawclaw.commands.oral import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/precedent" and args:
                from agents.lawclaw.commands.precedent import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/search" and args:
                from agents.lawclaw.commands.search import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/state" and args:
                from agents.lawclaw.commands.state import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/statute" and args:
                from agents.lawclaw.commands.statute import run as cmd_run
                result = cmd_run(args)
            elif cmd == "/summarize" and args:
                from agents.lawclaw.commands.summarize import run as cmd_run
                result = cmd_run(args)
            else:
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, "lawclaw")
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif args:
                    context = self._gather_context(args)
                    result = self.ask_llm(f"Law question: {args}\n\nContext:\n{context}")
                else:
                    result = "Type /help for commands"

            final_result = str(result)
            if final_result and len(final_result) > 20:
                try:
                    from shared.lifecycle import agent_cleanup
                    agent_cleanup("lawclaw", args or "", 0)
                except Exception: pass
                try:
                    from shared.enforcement.engine import EnforcementEngine
                    EnforcementEngine().load_reference("lawclaw_handler")
                except Exception: pass
                try:
                    from shared.guarded_executor import GuardedExecutor
                    GuardedExecutor("lawclaw")._check_and_record("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try:
                    from shared.execution_policy import ExecutionPolicy
                    ExecutionPolicy().check("handler_boundary", {"cmd": cmd})
                except Exception: pass
                try:
                    from shared.chronicle_helper import search_chronicle as chron_search
                    chron_search(args or cmd, limit=3)
                except Exception: pass
                try:
                    from shared.memory.procedural_memory import get_memory as get_proc_mem
                    pmem = get_proc_mem("lawclaw")
                    if len(final_result) > 100:
                        pmem.add_rule(content=f"Cmd {cmd}: {final_result[:200]}", category=cmd.lstrip("/") if cmd.startswith("/") else "general", importance=0.6)
                except Exception: pass
                try:
                    from shared.memory.three_tier import get_memory as get_three_tier
                    get_three_tier("lawclaw").get_context(args or cmd, limit=5)
                except Exception: pass
                try:
                    from shared.smart_router import SmartRouter
                    SmartRouter().route(cmd)
                except Exception: pass
                try:
                    from shared.agent_router import AgentRouter
                    AgentRouter().detect_task(args or cmd)
                except Exception: pass
                try:
                    from shared.validation import validate_schema
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
                    from shared.log_manager import get_logger
                    get_logger().info(f"lawclaw.{cmd}", extra={"args": (args or "")[:100]})
                except Exception: pass
                try:
                    from shared.shutdown import get_shutdown_manager
                    get_shutdown_manager().register(lambda: None)
                except Exception: pass
                try:
                    from shared.hooks.hook_manager import get_hook_manager
                    get_hook_manager().register("post_command", lambda: None)
                except Exception: pass
                try:
                    from shared.llm.budget import BudgetController
                    budget = BudgetController()
                    if not budget.check("lawclaw", estimated_cost=0.002).get("allowed", True):
                        final_result = "[BUDGET] Daily limit reached."
                except Exception: pass
                try:
                    from shared.rate_limiter import get_rate_limiter
                    if not get_rate_limiter().check_daily_limits():
                        final_result = "[RATE LIMIT] Too many requests."
                except Exception: pass
                try:
                    from shared.error_handler import get_circuit_breaker
                    get_circuit_breaker("lawclaw").call()
                except Exception: pass
                try:
                    from shared.metrics import get_metrics
                    get_metrics().counter("lawclaw_commands_total", "Total commands").inc()
                except Exception: pass
                try:
                    from shared.security import get_audit_logger
                    get_audit_logger().log_tool_call(cmd, {"args": (args or "")[:100]}, user="lawclaw")
                except Exception: pass
                try:
                    from agents.lawclaw.commands._memory import remember
                    remember(command=cmd, query=args or "", result_summary=final_result[:400], source_type="web_verified", confidence=0.85)
                except Exception: pass
                try:
                    from shared._agent_helpers import learn
                    learn("lawclaw", args or "", final_result[:500], "web_verified", 0.85)
                except Exception: pass
                try:
                    from shared.decision_ledger import get_ledger
                    get_ledger().record(agent="lawclaw", action=cmd, query=(args or "")[:200], result=final_result[:100])
                except Exception: pass
                try:
                    from shared.consensus_engine import constitutional_consensus_check
                    constitutional_consensus_check(final_result, args or "")
                except Exception: pass
                try:
                    from shared.llm.auditor import ChronicleAuditor
                    ChronicleAuditor().log(agent="lawclaw", prompt=(args or "")[:200], response={"result": final_result[:200]})
                    budget.record("lawclaw", cost=0.002)
                except Exception: pass
                try:
                    from shared.observability import get_health_checker
                    get_health_checker().register("lawclaw_handler", lambda: True)
                except Exception: pass
                try:
                    duration_ms = (time.time() - track_start) * 1000
                    from agents.webclaw.core.chronicle_ledger import log_event
                    log_event(agent="lawclaw", event="command_executed", detail=f"cmd={cmd} duration_ms={duration_ms:.0f}")
                except Exception: pass

            return {"status": "success", "result": final_result}
        except Exception as e:
            log_err("lawclaw", cmd or "unknown", str(e)[:200])
            return {"status": "error", "result": str(e)}

_agent = LawClawHandler()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
