# SESSION HANDOFF — October 5, 2026

**Purpose:** Fresh-session reference. Read this before doing anything
else next time. It captures what was done, what was discovered, and
what the next three priorities are.

**Primary reference (always):** `CLAWPACK_ONBOARD.md`
**Traps reference:** `docs/KNOWN_TRAPS.md`
**Environment reference:** `POWERSHELL_SURVIVAL_GUIDE.md`

---

## What This Session Accomplished

Six commits, all pushed to origin/main (except #6, pending — see below).
The retrieval pipeline is measurably better. A significant data-hygiene
issue was discovered and documented for the next session.

### Commits Pushed Today

| # | Hash | What |
|---|------|------|
| 1 | `2b8f1c106` | Article VII — 15 bare `except:pass` fixed across 5 agents |
| 2 | `c2fc9df51` | scan.py — reports all Article VII violations, not just first per file |
| 3 | `4e97dccd9` | Article VI — mem0-backed memory for all 21 agents |
| 4 | `f3f05efd9` | Cache hygiene — error-string guard in cached_search() |
| 5 | `7418f9160` | gitignore scripts/_*.py (Pattern B one-off builders) |
| 6 | (pending) | WebclawProvider.search_structured → query Chronicle instead of frozen web_cache.db |

**Note on #6:** The provider fix is written and tested but not yet committed.
Commit it at the start of the next session (see 'First Action Next Session').

---

## Constitutional Progress

| Article | Before | After |
|---------|--------|-------|
| Article VI (Shared Memory) | 1/21 (lawclaw only) | 21/21 (mem0-backed) |
| Article VII (Silent Failure) | 15 violations | Clean |

---

## Key Discoveries

### 1. mem0 Memory Is Working

`shared/memory/unified_memory_mem0.py` provides working cross-agent memory.
`shared/memory/unified_memory.py` is now a redirect. Legacy preserved at
`shared/memory/unified_memory_legacy.py`.

- Qdrant embedded storage at `runtime/mem0/qdrant/`
- fastembed ONNX embedder (no torch dependency)
- `infer=False` — no LLM calls, Article I compliant
- All 21 agents use it automatically via `BaseAgent.memory` property
- New deps added to requirements.txt: mem0ai>=2.2.0, fastembed>=0.8.0

### 2. Cache Write Path Was Poisoned by Error Strings

`BaseAgent.cached_search()` had a `len(result) > 20` threshold that let
network-error strings get cached. On subsequent queries, the poisoned
cache returned garbage instead of retrying.

**Fix applied:** raises threshold to 100, rejects 'timed out' / 'connection' /
'error' in first 50 chars / 'traceback'.

### 3. The April web_cache.db Was Contaminating Retrieval

`agents/webclaw/cache/web_cache.db` (280 MB, frozen April 22, 2026) contained
20,211 URLs — a duplicate index of the same corpus. Every WebClaw search
merged April content with current Chronicle content, polluting BM25 rankings
with stale frequency weights.

**Fix applied:** `WebclawProvider.search_structured()` now queries Chronicle
(`runtime/chronicle.db`) instead of `web_cache.db`. Same corpus, current index,
no duplication.

**Verified:** `ns:lawclaw court Denver` now returns current Colorado content
instead of April snapshot content or Iowa courts.

**Backup:** `agents/webclaw/cache/web_cache.db.bak` (280 MB safety net).

### 4. Two URL Conventions in Chronicle

Chronicle has 237,812 records. Two indexing conventions coexist:

| Convention | Count | Format | Status |
|-----------|-------|--------|--------|
| `http*` | 111,634 | Web fetches | Current |
| `reference://*` | 82,572 | Agent-namespace (new) | Current |
| `file://*` | **43,497** | Filesystem-path (old) | **Superseded, still present** |
| `local://*` | 66 | Local file links | Current |

**The file:// records are NOT identical duplicates.** Content comparison
showed:
- `file://` format: condensed, single-line preview (18-800+ chars)
- `reference://` format: structured with `AGENT:` / `PATH:` headers, richer

Both index the same source files. The `reference://` format supersedes the
`file://` format for retrieval quality (proper attribution, preserved markdown).

### 5. Orphaned Cache Files Removed

385 MB recovered by removing:
- `agents/webclaw/cache/webclaw_references.pkl` (381 MB, no code references)
- `agents/webclaw/cache/url_index.json` (3.9 MB, no code references)

**Important:** These were in `cache/`, NOT `references/`. The 41K-file corpus
in `agents/webclaw/references/` is completely intact and untouched.

---

## First Action Next Session

### 1. Commit the pending provider fix

```powershell
cd C:\Users\greg\dev\clawpack_v2
git status
# Should show: modified: agents/webclaw/providers/webclaw_provider.py
git add agents/webclaw/providers/webclaw_provider.py
git commit -m "WebclawProvider.search_structured: query Chronicle instead of frozen web_cache.db"
git push
```

### 2. Restart the server

Terminal 1: `Ctrl+C`, then `python a2a_server.py`

Confirm 21 agents register.

### 3. Validate

```powershell
python scripts\validate_agents.py
```

Expected: 21/21 pass.

---

## Priority 1: Chronicle Cleanup (Deferred)

### What needs to happen

Purge the superseded `file://` records from Chronicle. This is the completing
step of a re-indexing effort that started in May — the new `reference://`
format was introduced to fix broken URLs, but the old records were never removed.

### The precise purge

**Safe to purge:** 42,897 `file://` records that have a `reference://` twin
(same source file, richer content in new format).

**Keep:** 600 unmatched `file://` records with no `reference://` twin.
These were never re-indexed. Sample:
- `txclaw/TX-project/CLAUDE.md`
- `txclaw/TX-project/PROJECT_STATE.md`
- `txclaw/TX-project/.github/*`
- `claw_coder/objective-c/*`
- `mediclaw/oncology/targeted_therapy/*`
- `mediclaw/rheumatology/biologics_targeted_therapies/*`
- `cloud_computing/cloud_computing_references.md`
- `unified/MASTER_INDEX.md`

**Also consider purging:** `file://` records containing `node_modules` —
third-party library junk from the old indexing run. Sample:
```
245032 chars  file://...\txclaw\TX-project\apps\backend\node_modules\rxjs\CHANGELOG
108192 chars  file://...\txclaw\TX-project\services\crf-service\node_modules\express...
```

### The purge plan (write fresh script next session)

1. Backup `runtime/chronicle.db` to `chronicle.db.bak-pre-purge` (588 MB copy)
2. Build set of `file://` URLs that HAVE `reference://` twins
3. Build set of unmatched `file://` URLs to keep (600 records)
4. Delete `file://` records not in the keep set
5. Run `VACUUM` to reclaim disk
6. Test: `ns:lawclaw court Denver` → should return only `reference://` URLs
7. Validate: `python scripts\validate_agents.py` → 21/21
8. Commit if chronicle.db is tracked in git; otherwise note as local-only change

### Expected outcome

- Chronicle: 237,812 → ~194,315 records (~18% reduction)
- Disk: ~50-80 MB reclaimed after VACUUM
- Retrieval: clean URLs, no format-based ranking pollution

---

## Priority 2: _gather_context() Migration (Gate 7)

### Current state

| Agent | Uses `cached_search()` | Uses raw `call_agent("webclaw", ...)` |
|-------|----------------------|--------------------------------------|
| claw_coder | YES | — |
| docuclaw | YES | — |
| mediclaw | YES | — |
| txclaw | YES | — |
| **17 others** | NO | YES |

### The migration pattern

For each agent, change `_gather_context()`:

```python
# Before
web = self.call_agent("webclaw", f"search ns:{self.name} {query}", timeout=15)

# After
web = self.cached_search(f"ns:{self.name} {query}")
```

### Migration order

| Batch | Agents |
|-------|--------|
| 1 | crustyclaw, designclaw, draftclaw |
| 2 | drawclaw, dreamclaw, flowclaw, interpretclaw |
| 3 | langclaw, liberateclaw, llmclaw, mathematicaclaw |
| 4 | plotclaw, rustypycraw, lawclaw |
| Skip | fileclaw (no retrieval), webclaw (is the fetcher), dataclaw (cache owner) |

### Test after each batch

```powershell
python scripts\validate_agents.py
# Expected: 21/21
```

---

## Priority 3: Documentation Refresh

### Files that need updating

- `CLAWPACK_ONBOARD.md` — session log, mem0 activation, cache state
- `docs/NEXT_SESSION_MISSION.md` — replace stale June 5 priorities
- `BASEAGENT_GUIDE.md` — add memory section (mem0), mention Chronicle cleanup
- `docs/READ_THIS_FIRST.md` — update current state

### Known drift in current docs

| Doc | Says | Reality |
|-----|------|---------|
| `NEXT_SESSION_MISSION.md` | 'Only lawclaw has cache entries' | mediclaw + txclaw do; lawclaw has 0 |
| `NEXT_SESSION_MISSION.md` | '12 agents need migration' | Actually 17 |
| `CLAWPACK_ONBOARD.md` | 'Article VI: only lawclaw' | Now 21/21 via mem0 |
| `CHRONICLE_GUIDE.md` | '448 MB' | Now 588 MB |

---

## System State Summary

| Component | Status |
|-----------|--------|
| 21 agents | All register, all respond |
| A2A server | Running (port 8766) |
| Sovereign Gateway | Groq primary, working |
| Memory (mem0) | 21/21 agents, Qdrant embedded |
| Article VI | Compliant |
| Article VII | Clean |
| Cache (cached_search) | Working, error-guard in place |
| WebClaw retrieval | Provider now reads Chronicle |
| Chronicle | 237,812 records, ~43K need purge |
| Enforcement (Article XI) | Detection active, engine dormant |
| Guarded executor (Article IV) | Dormant |
| fileclaw delegation | Scan warning (one-line fix available) |

---

## Known Issues to Watch

### The file:// records stay until purged

Until the purge, queries return mixed results (both `file://` and
`reference://` URLs for the same content). Cosmetic — retrieval works —
but wastes tokens and may affect ranking.

### The web_cache.db.bak safety net

280 MB backup at `agents/webclaw/cache/web_cache.db.bak`. Once the purge is
verified and retrieval is stable for a week, this can be deleted.

### The Qdrant shutdown error

Non-fatal warning at Python shutdown:
```
ModuleNotFoundError: import of msvcrt halted; None in sys.modules
```
Windows-specific bug in Qdrant's local client. Data is fine. Can be silenced
later with an atexit handler if it becomes annoying.

### The spaCy warning from mem0

Non-fatal:
```
Failed to load spaCy lemma model: spaCy is not installed.
```
mem0 tries to load an NLP model for fact extraction. Since we use `infer=False`,
it's not needed. Cosmetic.

---

## Reference Commands

```powershell
# Start server
cd C:\Users\greg\dev\clawpack_v2
python a2a_server.py

# Validate agents
python scripts\validate_agents.py

# Check cache stats
python -c "from shared.search_cache import get_cache_stats; import json; print(json.dumps(get_cache_stats(), indent=2))"

# Test retrieval quality
python -c "from agents.webclaw.providers.webclaw_provider import WebclawProvider; p = WebclawProvider(); r = p.search_structured('court Denver', namespace='lawclaw'); [print(x['url']) for x in r[:5]]"

# Clear pycache (after shared/ module changes)
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Kill all Python
taskkill /F /IM python.exe
```

---

## Session Logistics

- **Session date:** October 5, 2026
- **Session focus:** Memory activation + retrieval diagnosis
- **Commits pushed:** 5 (plus 1 pending)
- **Next session focus:** Chronicle cleanup + _gather_context migration

---

## The One-Sentence Summary

**Clawpack V2 gained working memory for all 21 agents today, and we
diagnosed why retrieval was returning odd results — a frozen April index
plus 43K superseded records in Chronicle. The fix for the first is in place;
the cleanup for the second is planned and documented.**

