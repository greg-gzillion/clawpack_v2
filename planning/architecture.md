CLAWPACK V2 — CONSTITUTIONAL ARCHITECTURE (v3.0)

CORE LOOP:
  clawpack.py → A2A (port 8766) → agent_handler.process_task()
    → BaseAgent.smart_ask()
      → PILLAR I: WebClaw Retriever (BM25, 123K indexed references)
      → PILLAR II: Truth Resolver (web_verified > chronicle > memory > inference)
      → PILLAR III: Execution Policy (permission boundaries)
      → Sovereign Gateway (shared/llm/)
        → Chronicle audit (35K+ interactions)
        → Unified memory (with poisoning defense)
      → Decision Ledger (tamper-evident hash chain)
    → Guarded Executor (only legal path for dangerous ops)

SHARED MINISTRIES:
  shared/llm/               Sovereign Gateway — 4 providers, 25 models, budget, audit
  shared/enforcement/        Judiciary — 19 forbidden patterns, pre/post gates
  shared/memory/             Unified Knowledge — cross-agent recall
  shared/files/              Imperial Documents — 52 formats, 8 categories
  shared/truth_resolver.py   Epistemic Constitution — source hierarchy
  shared/source_registry.py  Trust Registry — 40+ sources, domain overrides
  shared/execution_policy.py Executive Boundaries — delete blocked, shell blocked
  shared/guarded_executor.py Operational Lock — only legal dangerous ops path
  shared/decision_ledger.py  Judicial Record — tamper-evident, cryptographically chained
  shared/import_scanner.py   Enforcement Scanner — detects bypass attempts
  shared/memory_guard.py     Memory Defense — inference never persists
  shared/docuclaw_api.py     Document Creation — one function for all agents
  shared/registry.py         Agent Registry — 14 agents, capability map, delegation
  shared/base_agent.py       Universal Choke Point — all 21 agents inherit this

CONSTITUTIONAL LAW:
  "No agent may speak to a model directly."
  All model access routes through shared/llm/client.py
  Enforced by: pre-commit hook, enforcement engine, import scanner, guarded executor
