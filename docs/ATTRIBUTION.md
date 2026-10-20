# Attributions

## Chronicle System

Clawpack V2's Chronicle indexing system is inspired by the work of
**Liu Juanjuan** (@liujuanjuan1984) on
[Common Chronicle](https://github.com/Intelligent-Internet/Common_Chronicle)
(Apache 2.0).

The Chronicle system adopts Common Chronicle's core principles: structured
context, source attribution, temporal organization, and sourcing integrity.
Clawpack's implementation is independent (SQLite FTS5 vs. vector embeddings),
not a code-level derivation.

**Primary file:** `agents/webclaw/core/chronicle_ledger.py`

Apache 2.0 permits this conceptual derivation. This attribution is given
in good faith and respect for the original work.

---

We are grateful to Liu Juanjuan for his innovative work on structured
context management.

> *"Common Chronicle turns messy context into structured, sourced timelines"*
> - liujuanjuan1984
Save with Ctrl+S.

Step 2 — Verify it's on disk:

powershell
cd C:\Users\greg\dev\clawpack_v2
Test-Path docs\ATTRIBUTION.md
Expected: True

Step 3 — Verify the content:

powershell
cd C:\Users\greg\dev\clawpack_v2
Get-Content docs\ATTRIBUTION.md | Select-Object -First 5
Expected:

text
# Attributions

## Chronicle System

Clawpack V2's Chronicle indexing system is inspired by the work of
**Liu Juanjuan** (@liujuanjuan1984) on