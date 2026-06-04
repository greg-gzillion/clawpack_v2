# KNOWN TRAPS - Clawpack V2
## Read this before writing any code. These are hard-won lessons.

### TRAP 1: Never inject code into agent handlers
**Result:** Corrupted all 21 agents with indentation errors (May 30, 2026).
**Fix:** Write command files in agents/<name>/commands/, Copy-Item to deploy.
**Pattern:** name = '/commandname' + def run(args, agent=None)
**Reference:** POWERSHELL_SURVIVAL_GUIDE.md

### TRAP 2: Never use python -c with multi-line code in PowerShell
**Result:** Nested quotes mangle, backslashes eaten, strings terminate mid-execution.
**Fix:** Write to scripts/_temp.py, execute it, delete it.
**Pattern:** Set-Content -Path scripts/_temp.py, then python scripts/_temp.py

### TRAP 3: Never use PowerShell heredocs with Python code
**Result:** Single quotes terminate early. Double quotes expand variables.
**Fix:** Write Python scripts that construct other Python files.
**Pattern:** Python builds content as list of lines, joins, writes.

### TRAP 4: All LLM access MUST route through shared/llm/client.py
**Constitutional:** Article I. No direct API calls. No provider imports.
**Enforced:** 6 sovereignty patterns blocked at HTTP boundary (403).
**Reference:** shared/CONSTITUTION_v1.md

### TRAP 5: Always scope WebClaw searches by agent namespace
**Result without:** DocuClaw generated FOIA requests instead of business letters.
**Fix applied June 4, 2026:** ns:{agent} prefix on all _gather_context() calls.
**Mechanism:** webclaw_provider.py search_with_context(query, namespace=agent_name)

### TRAP 6: Never add Chronicle context to ask_llm()
**Result without:** Cross-agent contamination. LawClaw data in DocuClaw output.
**Fix applied June 4, 2026:** Chronicle context removed from BaseAgent.ask_llm().
**Chronicle purpose:** Audit trail and jurisdiction lookup, NOT LLM context.

### TRAP 7: Always clear __pycache__ after changing shared modules
**Result without:** Stale bytecode. Changes appear not to take effect.
**Fix:** Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force

### TRAP 8: Never pipe to Out-File for files over ~100 lines
**Result:** PowerShell silently truncates.
**Fix:** Write via Python: open(path,'w').writelines(lines)

### TRAP 9: echo writes UTF-16 with BOM in PowerShell
**Result:** Null bytes break Python imports.
**Fix:** Use Set-Content for small files, Python for large files.

### TRAP 10: Never delete files without checking imports first
**Result:** ModuleNotFoundError cascades across agents.
**Fix:** Select-String -Path agents -Recurse -Pattern 'from.*filename' before deleting.
