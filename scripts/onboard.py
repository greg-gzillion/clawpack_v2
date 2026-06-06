#!/usr/bin/env python3
"""Clawpack V2 - Complete System Onboarding. Run this first."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def header(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()

def show_file(filepath, description):
    sep = chr(9472) * 70
    print(f"\n{sep}")
    print(f"  FILE: {filepath}")
    print(f"  {description}")
    print(f"{sep}\n")
    full_path = ROOT / filepath
    if full_path.exists():
        print(full_path.read_text(encoding="utf-8", errors="replace"))
    else:
        print(f"  [FILE NOT FOUND: {filepath}]")

header("CLAWPACK V2 - COMPLETE SYSTEM ONBOARDING")
print("21-agent local AI runtime. A2A on port 8766. Constitutional governance.")
print("Chronicle FTS5 (448MB). Sovereign Gateway. BM25 retrieval. 21/21 agents pass.")

header("CURRENT STATE — June 5, 2026")
print("Validation: 21/21 agents PASS")
print("Provider: Groq primary (llama-3.3-70b-versatile, 0.7s)")
print("Cache: Infrastructure exists, only lawclaw populated")
print("BM25: 9 agents show markers, 12 route through LLM")
print("Ledger: Repaired, no corruption")
print("TxClaw: 135 docs.tx.org URLs, 529 local files, cached_search wired")
print("Mediclaw: 91 specialties, /hospital with GPS/URLs, cached_search wired")

header("CRITICAL RULES")
print("1. NEVER python -c with multi-line code (quotes mangle)")
print("2. NEVER PowerShell heredocs with Python (quotes conflict)")
print("3. Use Pattern B: Python builder script -> run -> verify -> delete")
print("4. NEVER batch-inject into handlers (May 30 disaster)")
print("5. ALWAYS clear __pycache__ after shared module changes")
print("6. All LLM through Sovereign Gateway only (Article I)")
print("7. except: pass is UNCONSTITUTIONAL (Article VII)")
print("8. Command files for deployment, never handler injection")

header("SERVER MANAGEMENT")
print("Start: python a2a_server.py")
print("Menu: python clawpack.py")
print("Validate: python scripts/validate_agents.py")
print("Kill all: taskkill /F /IM python.exe")
print("Clear cache: Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force")

header("ARCHITECTURE")
print("Layer 1: A2A Server (port 8766) — Circuit breaker, sovereignty enforcement")
print("Layer 2: Shared Infrastructure — 93+ modules, Sovereign Gateway")
print("Layer 3: 21 Specialized Agents — Each with defined jurisdiction")

header("RETRIEVAL ARCHITECTURE")
print("User Query -> Agent Handler -> _gather_context() -> cached_search()")
print("  -> DataClaw Cache -> (miss) WebClaw BM25 -> Chronicle FTS5")
print("  -> final_score = bm25_score * source_weight")
print("  -> Context -> ask_llm() -> Response")
print("")
print("BM25 agents (9): lawclaw, claw_coder, crustyclaw, designclaw,")
print("  dreamclaw, interpretclaw, langclaw, liberateclaw, webclaw")
print("Non-search agents (12): route through ask_llm(), markers stripped")
print("Both paths WORK — different output format.")

header("WEBCLAW - CENTRAL NERVOUS SYSTEM")
print("WebClaw is the intelligence layer for all 21 agents.")
print("Three-layer retrieval: SQLite index -> Chronicle FTS5 -> BM25 ranking")
print("Namespace scoping (ns:agent) active on all agents.")
print("Contamination problem RESOLVED (June 4).")
print("")
print("REFERENCES: agents/webclaw/references/")
print("  lawclaw/    - 3,800+ city jurisdictions (courts, police, hospitals)")
print("  mediclaw/   - 91 medical specialties")
print("  txclaw/     - 135 docs.tx.org URLs, 11 domains")
print("  claw_coder/ - 80+ technology categories")
print("  + 15 more agent namespaces")
print("")
print("DATACLAW: Local data retrieval + cache storage")
print("  agents/dataclaw/references/{agent}/ - 21 agent directories")
print("  agents/dataclaw/cache/{agent}/ - WebClaw result cache")

header("PROVIDER CHAIN")
print("Groq (llama-3.3-70b-versatile, 0.7s, free) [PRIMARY]")
print("  -> Ollama (gemma3:4b, 0.8s GPU, free)")
print("  -> OpenRouter (gemma-4-26b, 0.7s, free)")
print("  -> Anthropic (claude-haiku, 1.2s, paid)")
print("Switch: llmclaw> /use groq")

header("KNOWN ISSUES — June 5, 2026")
print("HIGH: Cache population — only lawclaw has entries")
print("MEDIUM: 12 agents still use raw call_agent(webclaw) vs cached_search()")
print("MEDIUM: FlowClaw 13 variants — inventory done, consolidation pending")
print("MEDIUM: Enforcement blocking dormant — detection active")
print("LOW: claw_coder WebClawClient dead code (port 5000)")
print("LOW: BM25 visibility inconsistent across agents")

header("NEXT MISSION")
print("1. Cache population — investigate why cache writes not creating directories")
print("2. BM25 visibility — split /search (raw) from normal requests (LLM)")
print("3. _gather_context() migration — 12 agents to cached_search()")
print("4. FlowClaw consolidation — 13 variants -> 1")
print("5. Enforcement activation — blocking, not just detection")

header("BETA GATES (5/10)")
print("1. Enforcement blocks violations — DONE")
print("2. 21 agents online — DONE")
print("3. Constitutional ledger stable — DONE")
print("4. WebClaw BM25 operational — DONE")
print("5. Validation harness operational — DONE")
print("6. Cache population working — IN PROGRESS")
print("7. Retrieval standardization — IN PROGRESS")
print("8. FlowClaw consolidation — TODO")
print("9. Enforcement activation — TODO")
print("10. Beta readiness review — TODO")

header("REQUIRED READING")
docs = [
    ("CLAWPACK_ONBOARD.md", "Architecture, rules, session log, next mission"),
    ("docs/KNOWN_TRAPS.md", "Mistakes that cost hours — read before coding"),
    ("POWERSHELL_SURVIVAL_GUIDE.md", "How to work in this environment"),
    ("docs/WEBCLAW_MANUAL.md", "WebClaw complete guide"),
    ("docs/WEBCLAW_ARCHITECTURE.md", "WebClaw system design"),
    ("shared/CONSTITUTION_v1.md", "Supreme law — NON-NEGOTIABLE"),
]
for i, (fp, desc) in enumerate(docs, 1):
    print(f"  {i}. {fp} — {desc}")

print()
print("KEY FILES: shared/base_agent.py, shared/search_cache.py,")
print("  shared/llm/client.py, agents/webclaw/agent_handler.py,")
print("  agents/webclaw/core/retriever.py, a2a_server.py, clawpack.py")
print()
print("VALIDATION: python scripts/validate_agents.py")
print("CACHE CHECK: python -c \"from shared.search_cache import get_cache_stats; print(get_cache_stats())\"")

print()
print("=" * 70)
print("  PRINTING ALL REQUIRED DOCUMENTS")
print("=" * 70)
for filepath, desc in docs:
    show_file(filepath, desc)

header("ONBOARDING COMPLETE")
print("Run: python scripts/onboard.py > onboarding_output.txt")
print("to save everything for sharing with a new session.")
