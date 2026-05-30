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
# POWERSHELL_SURVIVAL_GUIDE.md
## Why This File Exists
On May 30, 2026, approximately 2 hours were lost to PowerShell-specific failures
when trying to write files, execute Python, and restart the A2A server.
This document exists so no future session repeats those failures.

## What FAILED (Do Not Repeat)

### 1. python -c with multi-line code
FAILED EVERY TIME. PowerShell mangles nested quotes, eats backslashes,
and randomly terminates strings mid-execution.

Example of FAILURE:
```powershell
python -c "
import sys
print('hello')
"
PowerShell interprets the double quotes as PowerShell string delimiters,
not Python string delimiters. The code never reaches Python intact.

2. PowerShell heredocs containing Python code
FAILED EVERY TIME. Single-quoted heredocs (@'...'@) terminate early when
they encounter Python single quotes. Double-quoted heredocs (@"..."@)
expand PowerShell variables and break Python syntax.

Example of FAILURE:

powershell
@'
python_code = 'this breaks the heredoc'
'@
The middle single quote closes the heredoc. Everything after is executed
as raw PowerShell, which locks up the terminal.

3. Out-File for files over ~100 lines
FAILED SILENTLY. The file appears to write but is silently truncated.
Only discovered by checking GitHub or counting lines after the fact.

Example of FAILURE:

powershell
@"
[200+ lines of content]
"@ | Out-File -FilePath "target.md" -Encoding UTF8
# File on disk: only ~80 lines. No error message.
4. echo appending for multi-line content
FAILED. Cannot handle special characters, newlines in strings, or any
content more complex than a single plaintext sentence.

What WORKED (Use These Patterns)
Pattern A: Write a Python script to disk, then execute it
This is the ONLY method that reliably wrote files over 50 lines.
The Python script itself must be under ~50 lines (Out-File limit).

powershell
@"
with open(r'target_file.md', 'w', encoding='utf-8') as f:
    f.write('''content here''')
print('Done')
"@ | Out-File -FilePath "scripts/_fix.py" -Encoding ASCII
python scripts/_fix.py
Remove-Item scripts/_fix.py -Force
Pattern B: For large files, construct content in Python programmatically
Instead of embedding the file content in the PowerShell script (which
triggers escaping issues), have the Python script build the content
as a list of lines, then join and write.

powershell
@"
lines = []
lines.append('# Title')
lines.append('')
lines.append('Content line 1')
lines.append('Content line 2')
with open('target.md', 'w') as f:
    f.write('\n'.join(lines))
print(f'Written: {len(lines)} lines')
"@ | Out-File -FilePath "scripts/_build_file.py" -Encoding ASCII
python scripts/_build_file.py
Remove-Item scripts/_build_file.py -Force
Pattern C: Verify every file write immediately
powershell
python -c "print(len(open('target.md').read().splitlines()))"
Compare against expected line count. Several May 30 fixes appeared
to work but files were truncated on disk.

Pattern D: Read a file before modifying it
powershell
Get-Content "path/to/file.py" | Select-Object -First 5
Or:

powershell
python -c "print(open('path/to/file.py').read()[:200])"
Server Management Commands
Kill all Python processes
powershell
taskkill /F /IM python.exe 2>$null
Clear Python bytecode cache (REQUIRED after any shared/ module change)
powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Start A2A server
powershell
cd C:\Users\greg\dev\clawpack_v2
python a2a_server.py
Or in background:

powershell
Start-Process python -ArgumentList "a2a_server.py" -NoNewWindow
Start-Sleep 4
Test if server is running
powershell
python -c "import requests; r=requests.post('http://127.0.0.1:8766/v1/message/lawclaw',json={'task':'/stats'},timeout=10); print(r.status_code)"
Check what's listening on A2A port
powershell
netstat -ano | findstr "8766.*LISTENING"
Why Python Files Are the Only Reliable Method
The core issue: PowerShell and Python have conflicting string delimiters.

PowerShell: @'...'@ (single-quote heredoc), @"..."@ (double-quote heredoc)

Python: '''...''' (triple single), """...""" (triple double)

When Python code is embedded in PowerShell:

Single quotes in Python terminate PowerShell single-quote heredocs

Double quotes in Python get variable-expanded by PowerShell double-quote heredocs

Backslashes in Python are interpreted as PowerShell escape characters

The ONLY safe boundary is a .py file on disk. Write it. Execute it. Delete it.
Never try to inline Python in PowerShell. It will fail.

Quick Test Matrix
Task	Method	Works?
Read file	Get-Content	YES
Read file	python -c "print(open('f').read()[:100])"	YES (short)
Write small file	@"..."@ | Out-File	YES (<50 lines)
Write large file	@"..."@ | Out-File	NO (truncates silently)
Write any file	Python script on disk	YES (always)
Multi-line Python	python -c "..."	NO
Python heredoc in PS	@'...python...'@	NO (locks terminal)
Python script on disk	python scripts/_fix.py	YES (always)
"@	Out-File -FilePath "POWERSHELL_SURVIVAL_GUIDE.md" -Encoding UTF8