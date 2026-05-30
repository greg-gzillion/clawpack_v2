> **NOTE: This audit was conducted May 29, 2026. State has changed.**
> See CLAWPACK_ONBOARD.md for current agent constitutional status (May 30: 13 constitutional, 7 partial, 1 needs upgrade).
> Re-audit pending. Key changes since May 29: lifecycle contract drift resolved (0 cleanup errors), 13 agents now have shared memory, provider chain fixed (Groq primary), civic commands use Chronicle FTS5 direct.
# CONSTITUTIONAL COMPLIANCE AUDIT
## May 29, 2026

*This document measures every agent against the Constitution of Clawpack V2.
Where code and Constitution conflict, the Constitution prevails.
This audit exists to identify treason, not celebrate progress.*

---

## Article I â€” Sovereignty Compliance

**Requirement:** All LLM access SHALL route through shared/llm/client.py.

| Agent | Compliant? | Violation |
|-------|-----------|-----------|
| lawclaw | âœ… | â€” |
| llmclaw | âŒ | `own_llm=True` â€” bypasses its own Sovereign Gateway |
| All others | âœ… | Route through A2A |

**Article I Score: 20/21 compliant. llmclaw in violation.**

---

## Article III â€” Delegation Compliance

**Requirement:** All cross-agent routing SHALL use BaseAgent.call_agent().

| Agent | Delegates? | Violation |
|-------|-----------|-----------|
| lawclaw | âœ… | â€” |
| drawclaw | âŒ | 15 commands, zero cross-agent calls. Cannot export, cannot chart, cannot search web. |
| fileclaw | âŒ | 1 command, zero cross-agent calls. Isolated from all agents. |
| mathematicaclaw | âŒ | 10 commands, zero cross-agent calls. Cannot visualize, cannot export. |
| All others | âœ… | Delegate to at least one agent |

**Article III Score: 17/21 compliant. 3 agents in violation. 0 agents auto-delegate (Article III Section 3).**

---

## Article IV â€” Dangerous Operations Compliance

**Requirement:** All dangerous operations SHALL pass through shared/guarded_executor.py.

**Status: âŒ GUARDED EXECUTOR NOT ACTIVATED AT RUNTIME.**

No agent routes through guarded_executor. Subprocess calls, file operations, and git commands bypass constitutional review. The executor exists (150 lines) but is never called by a2a_server.py or any agent handler.

**Article IV Score: 0/21 compliant. Systemic violation.**

---

## Article V â€” Truth Hierarchy Compliance

**Requirement:** web_verified > chronicle > memory > inference.

| Component | Status |
|-----------|--------|
| source_registry.py | âœ… Active â€” .gov at 0.92, .us courts at 0.85 |
| truth_resolver.py | âš ï¸ Partial â€” classify_source() patched but merge_with_retriever() never called in command flow |
| consensus_engine.py | âœ… Active â€” scoring facts by source trust |
| memory_guard.py | âœ… Active â€” blocks inference and low-confidence writes |

**Article V Score: Partially compliant. Truth hierarchy defined but not enforced at all decision points.**

---

## Article VI â€” Shared Memory Compliance

**Requirement:** All writes schema-validated, versioned, timestamped, traceable.

| Agent | Writes to Memory? | Reads from Memory? |
|-------|------------------|-------------------|
| lawclaw | âœ… | âœ… |
| All others | âŒ | âŒ |

**Article VI Score: 1/21 compliant. Shared memory exists but only one agent uses it.**

---

## Article VII â€” Silent Failure Compliance

**Requirement:** except: pass is UNCONSTITUTIONAL.

| Agent | Status |
|-------|--------|
| lawclaw | âœ… All exceptions logged via log_err() |
| claw_coder, crustyclaw, dataclaw, designclaw, docuclaw, draftclaw, drawclaw, dreamclaw, fileclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, plotclaw, rustypycraw, txclaw, webclaw | âš ï¸ Unknown â€” not audited |
| llmclaw, mathematicaclaw | âš ï¸ Unknown â€” not audited |

**Article VII Score: 1/21 confirmed compliant. 20 agents unaudited.**

---

## Article XI â€” Constitutional Enforcement

**Requirement:** Enforcement engine SHALL enforce pre/post execution gates.

**Status: âŒ ENFORCEMENT ENGINE NOT ACTIVATED AT RUNTIME.**

shared/enforcement/engine.py exists. PreExecutionGate exists. PostExecutionGate exists. ForbiddenPatternDetector exists (19 patterns). None are called by a2a_server.py. Constitutional violations are voluntary.

**Article XI Score: 0/21 compliant. Systemic violation.**

---

## Summary

| Article | Compliance | Status |
|---------|-----------|--------|
| I â€” Sovereignty | 20/21 | llmclaw in violation |
| III â€” Delegation | 17/21 | 3 isolated, 0 auto-delegate |
| IV â€” Dangerous Ops | 0/21 | Guarded executor dormant |
| V â€” Truth Hierarchy | Partial | Resolver not enforced at all points |
| VI â€” Shared Memory | 1/21 | Only lawclaw participates |
| VII â€” Silent Failure | 1/21 audited | 20 unaudited |
| XI â€” Enforcement | 0/21 | Judiciary dormant |

**Overall: The Constitution is law. The system is not yet compliant.**

LawClaw is the reference implementation proving compliance is possible. The other 20 agents must follow. The enforcement engine must be activated. The guarded executor must be wired. This audit exists to ensure that happens.


---

## Audit Methodology

This audit was conducted on May 29, 2026 using the following reproducible scan
executed from the project root:

```powershell
Get-ChildItem "agents" -Directory | ForEach-Object {
    $name = $_.Name
    $handler = Join-Path $_.FullName "agent_handler.py"
    if (Test-Path $handler) {
        $content = Get-Content $handler -Raw
        $hasCallAgent = if ($content -match 'call_agent') {"delegates"} else {"isolated"}
        $hasOwnLLM = if ($content -match 'own_llm|anthropic|groq|ollama|openrouter') {"own_llm"} else {"sovereign"}
        $hasMemory = if ($content -match 'unified_memory|_memory|remember|recall_prior|learn_fact') {"memory"} else {"no_memory"}
        $hasChronicle = if ($content -match 'chronicle|Chronicle') {"chronicle"} else {"no_chronicle"}
        $commands = (Get-ChildItem (Join-Path $_.FullName "commands") -Filter "*.py" -ErrorAction SilentlyContinue).Count
        Write-Host "$name | $hasCallAgent | $hasOwnLLM | $hasMemory | $hasChronicle | $commands commands"
    }
}
What Each Marker Means
Marker	Constitutional Article	Detection Pattern
call_agent	Article III â€” Delegation	Agent handler calls call_agent() to delegate to other agents
own_llm	Article I â€” Sovereignty	Agent imports anthropic/groq/ollama/openrouter directly (violation)
memory	Article VI â€” Shared Memory	Agent imports UnifiedMemory or uses _memory bridge
chronicle	Article VII â€” Audit	Agent references Chronicle for indexing or search
How Scores Are Calculated
Article I (Sovereignty): sovereign = compliant. own_llm = violation.

Article III (Delegation): delegates = compliant. isolated = violation.

Article IV (Dangerous Ops): Requires runtime check of guarded_executor.py wiring in a2a_server.py. Not detectable from static agent scan alone.

Article VI (Memory): memory = compliant. no_memory = violation.

Article VII (Silent Failure): Requires manual audit of exception handlers. Only lawclaw has been fully audited.

Article XI (Enforcement): Requires runtime check of enforcement/engine.py activation in a2a_server.py. Not detectable from static agent scan alone.

Shared Infrastructure Scan
The shared folder was scanned for connectivity using:

powershell
Get-ChildItem "shared" -Recurse -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $relPath = $_.FullName -replace ".*\\shared\\", "shared\"
    $hasCall = if ($content -match 'call_agent|delegate') {"YES"} else {"-"}
    $hasLLM = if ($content -match 'ask_llm|smart_ask|def llm|def smart') {"YES"} else {"-"}
    $hasMem = if ($content -match 'UnifiedMemory|unified_memory|learn_fact|recall_prior|remember|recall_memory') {"YES"} else {"-"}
    $hasChron = if ($content -match 'chronicle|Chronicle') {"YES"} else {"-"}
    Write-Host "call:$hasCall llm:$hasLLM mem:$hasMem chron:$hasChron | $relPath"
}
Only 4 of 86 shared modules hit all four pillars: base_agent.py, _agent_helpers.py, registry.py, and unified_memory.py. The remaining 82 modules are built but not integrated into lawclaw's active execution path.

Re-audit Schedule
This audit SHALL be re-run after any session that:

Modifies an agent handler

Adds a new agent

Changes the shared infrastructure

Activates a dormant module

The Constitution is law. Compliance is not optional.
