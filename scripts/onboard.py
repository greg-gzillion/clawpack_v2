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
print("Chronicle FTS5. Sovereign Gateway. Advanced Alpha. 5/10 Beta gates.")

header("CRITICAL RULES")
print("1. NEVER python -c with multi-line code")
print("2. NEVER PowerShell heredocs with Python")
print("3. Deploy: write command file once, Copy-Item to all agents")
print("4. NEVER batch-inject into handlers (May 30 disaster)")
print("5. ALWAYS clear __pycache__ after shared changes")
print("6. All LLM through Sovereign Gateway only")
print("7. except: pass is UNCONSTITUTIONAL")

header("SERVER MANAGEMENT")
print("Start: python a2a_server.py")
print("Kill all: taskkill /F /IM python.exe")
print("Clear cache: remove __pycache__ directories recursively")

header("GETTING STARTED")
print("1. Start Ollama: ollama serve")
print("2. Start server: python a2a_server.py")
print("3. Launch menu: python clawpack.py")
print("4. Select agent 1 (lawclaw): /court Denver CO")

header("ARCHITECTURE")
print("Layer 1: A2A Server - Circuit breaker, sovereignty enforcement")
print("Layer 2: Shared Infrastructure - 93+ modules, Sovereign Gateway")
print("Layer 3: 21 Specialized Agents - Each with defined jurisdiction")

header("WEBCLAW - CENTRAL KNOWLEDGE SYSTEM")
print("Citation manager and intelligence layer for all 21 agents.")
print("Three layers: Live Fetch, SQLite Index (280MB), BM25 Retrieval.")
print("35,000+ reference files. 50 states, 3,000+ counties, 3,800+ cities.")
print("CRITICAL BUG: Searches not namespace-scoped. Causes contamination.")
print("READ: docs/WEBCLAW_MANUAL.md for complete documentation.")

header("PROVIDER CHAIN")
print("Ollama (gemma3:4b, priority 1) -> Groq -> OpenRouter -> Anthropic")
print("GPU: GTX 970, 4GB VRAM.")

header("KNOWN ISSUES")
print("CRITICAL: WebClaw cross-domain contamination")
print("HIGH: FlowClaw 13 variants, 6 agents with duplicates")
print("MEDIUM: Obliterated models not via standard Ollama")

header("NEXT MISSION")
print("Priority 6: Codebase consolidation")
print("Priority 7: Security assessment")
print("Infrastructure: WebClaw namespace-scoped search")
print("Beta gates: 5 of 10 passed")

header("REQUIRED READING")
docs = [
    ("POWERSHELL_SURVIVAL_GUIDE.md", "How to work in this environment"),
    ("CLAWPACK_ONBOARD.md", "Architecture, rules, session log, next mission"),
    ("docs/WEBCLAW_MANUAL.md", "WebClaw complete guide - READ THIS FIRST"),
    ("shared/CONSTITUTION_v1.md", "Supreme law - NON-NEGOTIABLE"),
    ("BASEAGENT_GUIDE.md", "What every agent inherits from BaseAgent"),
    ("AGENT_CAPABILITIES.md", "Which agent owns which capability"),
    ("CHRONICLE_GUIDE.md", "How the 448MB knowledge database works"),
    ("DECISION_LOG.md", "Why architectural decisions were made"),
    ("docs/reports/STATE_OF_CLAWPACK_V2_2026_06_02.md", "Frozen audit snapshot"),
]
for i, (fp, desc) in enumerate(docs, 1):
    print(f"  {i}. {fp} - {desc}")

print()
print("KEY SOURCE FILES: shared/base_agent.py, shared/_agent_helpers.py,")
print("  shared/llm/client.py, shared/capabilities.py, shared/query_normalizer.py,")
print("  a2a_server.py, clawpack.py")
print()
print("AGENT READMEs: agents/<name>/README.md (21 files, one per agent)")

print()
print("=" * 70)
print("  PRINTING ALL REQUIRED DOCUMENTS")
print("=" * 70)
for filepath, desc in docs:
    show_file(filepath, desc)

header("ONBOARDING COMPLETE")
print("Run: python scripts/onboard.py > onboarding_output.txt")
print("to save everything for sharing with a new session.")