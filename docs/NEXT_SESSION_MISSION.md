# NEXT SESSION MISSION - Clawpack V2

## Read this before doing anything else
1. python scripts/scan.py
2. python scripts/onboard.py
3. docs/KNOWN_TRAPS.md
4. docs/READ_THIS_FIRST.md

## Mission: Build the AI Onboarding Infrastructure

These are the 8 deliverables suggested by the June 4 external audit.
Complete them in order. Each one makes the next easier.

### 1. Dependency Map Generator (scripts/dependency_map.py)
Script that prints import trees for all 21 agents.
python scripts/dependency_map.py
Output shows which files each agent_handler.py actually imports.
Purpose: Immediately identifies dead code safe to archive.
Reference: FlowClaw inventory already done (agents/flowclaw/ - 13 variants, 0 imported).

### 2. Agent Jurisdiction Registry (shared/jurisdiction_registry.json)
{
  "lawclaw": {"domain": "legal", "can_call": ["webclaw","docuclaw","interpretclaw"]},
  "docuclaw": {"domain": "documents", "can_call": ["webclaw","lawclaw"]},
  ...
}
Purpose: Executable jurisdiction map. Verify agents stay in bounds.

### 3. Technical Debt Dashboard (docs/TECHNICAL_DEBT.md)
One-page report listing remaining issues by severity.
HIGH: Security review, prompt injection testing
MEDIUM: FlowClaw variants (13), DocuClaw variants (3), MedicLaw provider duplication
LOW: STATE_NAMES deduplication, LangClaw backup directory
Purpose: Next agent knows exactly where to work.

### 4. Architecture Decision Log (docs/ARCHITECTURE_LOG.md)
Chronological record of major irreversible decisions.
Include: date, decision, reason, what breaks if reversed.
Key entries: May 30 handler injection ban, June 4 Chronicle removal, June 4 namespace scoping.
Purpose: Prevent future agents from undoing deliberate architecture.

### 5. Milestone Record (docs/MILESTONES.md)
Named milestones, not just dates.
WebClaw Isolation Refactor (June 4, 2026)
Sovereign Gateway Stabilization (June 2-4, 2026)
LLM Consolidation (June 4, 2026)
Purpose: Future agents understand WHY the architecture looks this way.

### 6. Runtime Architecture Diagram (docs/ARCHITECTURE_DIAGRAM.md)
One-screen ASCII art diagram:
User -> Menu -> A2A Server -> Agent -> BaseAgent -> WebClaw -> Sovereign Gateway -> Provider Chain -> Response
Purpose: 30-second mental model for any AI agent.

### 7. Expand scan.py with Status Dashboard
Add sections: ARCHITECTURE (pass/fail), TECHNICAL DEBT (counts), SECURITY (status), BETA GATE (x/10)
Purpose: One-command executive summary.

### 8. Update READ_THIS_FIRST.md
After building all the above, update the Essential Files section to include them.
Purpose: Next next agent has everything.

## Rules (from KNOWN_TRAPS.md)
- NEVER inject code into agent handlers. Use command files.
- NEVER python -c with multi-line code in PowerShell. Write to scripts/_temp.py.
- NEVER use PowerShell heredocs with Python code.
- ALWAYS clear __pycache__ after shared module changes.
- ALWAYS scope WebClaw searches with namespace.
- NEVER add Chronicle context to ask_llm().

## Current State (June 4, 2026)
- Version: 3.2.0
- Agents: 21/21 operational
- Active model: gemma3:4b (Ollama, GTX 970 4GB)
- Beta gates: 5/10 complete
- FlowClaw: 13 variants inventoried, ready to archive
- Scripts: cleaned to 17 files
- Next commit should be one of the deliverables above
