# CLAWPACK V2 ? AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at runtime/chronicle.db. Constitutional governance.
Built by Greg.

## CRITICAL: PowerShell Environment (Windows)
- NEVER use python -c with multi-line code. Write to scripts/_temp.py and run it.
- NEVER pipe to Out-File for files over 100 lines. PowerShell silently truncates.
- Avoid PowerShell heredocs for large Python scripts; they have previously caused escaping issues. For small files under 10 lines, echo works reliably.
- ECHO WORKS for small files. Copy-Item WORKS for deployment.
- ALWAYS verify writes: python -c "print(len(open("path").read()))"
- ALWAYS kill Python: taskkill /F /IM python.exe
- ALWAYS clear __pycache__ after changing shared modules.
- READ POWERSHELL_SURVIVAL_GUIDE.md for full failure patterns and fixes.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None) at module level.
No manual registration - just drop the .py file in the directory.
This is the preferred pattern for adding features to all agents.
Do NOT batch-inject code into handlers. It corrupts indentation.
Write a command file once, then Copy-Item to all agents.

## CRITICAL LESSON: Command Files vs Handler Injection
On May 30, batch-injecting /voice code into 21 agent handlers via string replacement
corrupted indentation in ALL 21 agents. Required git revert to clean state.
The fix: write command files in agents/lawclaw/commands/, then Copy-Item to all others.
Zero handler changes. Zero indentation risk. The system was designed for this.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

---

## Current State - June 2, 2026

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median /help latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,000+ interactions (runtime/chronicle.db) |
| LLM providers | Groq + OpenRouter confirmed working |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Lifecycle cleanup errors | 0 |
| Enforcement | Active - 6 sovereignty patterns blocked at HTTP boundary |
| Civic commands | Chronicle FTS5 direct (0.03-0.28s) |
| Memory filtering | Geographic scoring bonus active (city +5, state +3) |

### Agent Accessibility (all via command files, no handler changes)
| Feature | Agents | How to use |
|---------|--------|------------|
| /voice | 21/21 | Toggle system-wide voice mode |
| /listen | 21/21 | One-shot microphone transcription |
| /translate | 21/21 | Detect language and translate to English |
| /braille | 21/21 | Convert text to Braille Unicode output |
| /speak | 21/21 | Speak text aloud in current language |
| /read | 21/21 | TTS reader with voice profiles, file reading, speed control |
| /language | 21/21 | Set system-wide language preference |
| /interpret | 21/21 | Live bidirectional interpreter mode |
| /access | 21/21 | Toggle Braille/Neuralink/Eye tracking on/off |

### Provider Chain (Sovereign Gateway)
| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free |
| 2 | Ollama | deepseek-r1:8b | 0.8s GPU / 30-120s CPU | Free |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

GPU: NVIDIA GeForce GTX 970, 4GB VRAM (~2.8GB available).
Fits GPU: tinyllama (0.6GB), gemma3:1b (0.8GB), gemma3:4b (3.3GB), smollm2-liberated (3.4GB).
Does NOT fit: deepseek-r1:8b (5.2GB), codellama:7b (3.8GB), gemma3:12b+.
Obliterated models (6): codellama_7b, deepseek_coder_6.7b, phi2, qwen_coder_7b, smollm2_1.7b, tinyllama.
Current preferred GPU-fit model: phi2 (2.7GB).

### System-Wide Accessibility Toggles
| Toggle | Hotkey | Wake Word | Menu Key |
|--------|--------|-----------|----------|
| Voice mode | Ctrl+Alt+V | start/stop listening | v |
| Braille output | Ctrl+Alt+B | - | b |
| Neuralink | Ctrl+Alt+N | - | n |
| Eye tracking | Ctrl+Alt+E | - | e |

### Quick Reference: Files That Matter
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active |
| shared/base_agent.py | Foundation class for all 21 agents | Active |
| shared/enforcement/detector.py | ForbiddenPatternDetector | Active |
| shared/enforcement/engine.py | Full EnforcementEngine | Dormant |
| shared/memory/unified_memory.py | Cross-agent shared memory | Active |
| shared/accessibility.py | TTS/STT/Braille/Translate | Active |
| shared/query_normalizer.py | Canonical location extraction + command stripping | Active |
| shared/lifecycle.py | Agent cleanup supervisor | Active (0 errors) |
| agents/lawclaw/agent_handler.py | Reference implementation | Gold standard |
| agents/lawclaw/commands/_memory.py | Memory bridge with geo-filtering | Active |
| agents/webclaw/core/chronicle_ledger.py | Chronicle FTS5 index | Active |
| agents/llmclaw/agent_handler.py | Model manager + orchestrator | Active |
| runtime/chronicle.db | 448MB SQLite FTS5 | Active |
| runtime/ledgers/ | Constitutional ledger, budget, chronicle | Active |
| runtime/indexes/ | Memory and consensus indexes | Active |
| data/ | Static reference data only (jurisdictions, schemas) | Active |

---

## Session Log

### June 2, 2026 - ENFORCEMENT + RUNTIME SEPARATION + GEO-FILTERING

Priority 1 - Enforcement blocking: DONE
- Sovereignty enforcement activated at HTTP boundary in a2a_server.py.
- ForbiddenPatternDetector.scan_task() runs before every agent dispatch.
- 6 patterns return 403: import anthropic, from groq import, import ollama,
  openrouter.ai, api.groq.com, localhost:11434.
- Normal commands (/help, /stats) pass through unaffected.
- except:pass anti-pattern removed. Enforcement failures are logged.
- Architectural decision: lightweight HTTP firewall. Full engine preserved for later.

Priority 2 - Ledger repair: RESOLVED
- Constitutional ledger verified: 36 entries, valid JSON, hash chain intact.
- Malformed JSON was in old data/ path, removed during runtime migration.

Priority 3 - Geographic memory filtering: DONE
- _extract_location() extracts city/state from queries including full state names.
- recall() applies +5 bonus for same-city, +3 for same-state matches.
- Strips command prefixes (/court, /jurisdiction, /law, bare court/law etc).
- 8/8 test cases pass. Bedford VA contamination prevented.
- Patched: agents/lawclaw/commands/_memory.py and shared/_agent_helpers.py.

Priority 4 - Provider fallback validation: DONE
- test_fallback_chain.py created for repeatable validation.
- Groq (0.5s) and OpenRouter (1.1s) both confirmed working.
- Fallback chain functional. Ollama offline, Anthropic disabled (paid).

Runtime state separation: DONE
- All mutable files moved from data/ to runtime/. runtime/ is gitignored.
- 10 source files patched. 2 absolute path bugs fixed in draftclaw.
- Permanently eliminates stash contamination and rebase conflicts.

Obliterated models listing: FIXED
- /models now reads from models/obliterated/ directory.
- Shows 6 real obliterated models with source and technique metadata.
- /use smollm2_1.7b verified working.

claw_coder handler cleanup: DONE
- 75 lines of dead 23-system boundary block removed.

State audit published at docs/reports/STATE_OF_CLAWPACK_V2_2026_06_02.md
Scores: Enforcement 3.0->6.0, Infrastructure 8.5->9.0, Overall 6.6->7.0

### May 31 / June 1, 2026
- Court resolver: city-first traversal. Georgetown CO resolves in ~500ms.
- Accessibility layer unified. Event bus created.
- a2a_server.py Tier 2 wiring: rate limiter, enforcement gate, metrics, logging.
- Voice pipeline functional inside agents.

### May 30, 2026
- Handler injection failure: batch script corrupted all 21 agents. Git revert.
- Command-file deployment adopted as the only safe extension mechanism.
- Lifecycle contract drift resolved (3 errors -> 0).
- Provider chain fixed (Groq primary, was Anthropic hardcoded).
- Civic commands -> Chronicle FTS5 direct (0.03s, was 45-90s).
- Accessibility commands deployed to all 21 agents.
- All 21 agents tested: 21/21 responsive.

### May 27-29, 2026
- 12 lawclaw commands built. Cross-agent flow established.
- Constitutional boundary activated. Consensus engine deployed.
- Capability registry + lifecycle supervisor + memory staleness deployed.

---



### June 2, 2026 (afternoon) - AGENT VALIDATION + QUERY NORMALIZER

Priority 5 - Agent validation: DONE
- All 21 agents respond to /help (21/21).
- 17/21 respond to domain commands.
- 4 timeouts (lawclaw, docuclaw, interpretclaw, claw_coder) due to Groq+OpenRouter rate limiting.
- rustypycraw and dataclaw /stats verified working (prior timeouts were false negatives).
- All 11 "untested" agents now tested and confirmed responsive.

Infrastructure - Query normalizer: DONE
- Created shared/query_normalizer.py as single canonical source for location extraction.
- _memory.py and _agent_helpers.py now import from shared module.
- Eliminates duplication risk. 8/8 tests pass.

---

## NEXT SESSION AGENDA - June 3, 2026

### Step 0: Ollama Recovery (RUN FIRST)
Before touching any agent files, restore the local provider to get clean validation baselines.
- Start ollama serve
- Verify with: ollama list
- Update models/active_model.json to use gemma3:4b (3.3GB, fits GTX 970 GPU)
- Test all 4 previously-timing-out agents: lawclaw, docuclaw, interpretclaw, claw_coder
- If any still time out, provider chain is broken ? fix before consolidating
- This eliminates false negatives during consolidation testing

### Priority 6: Codebase Consolidation (HIGHEST PRIORITY)
Duplicate implementations create maintenance burden and confusion about canonical code.

| Agent | Variants | Action | Risk |
|-------|----------|--------|------|
| flowclaw | 13 flowclaw*.py files | Keep the one imported by agent_handler.py, move rest to _archive/ | Medium - verify engine/ modules still work |
| docuclaw | 3 implementations (docuclaw_clean.py, agent_handler.py, core/) | Keep agent_handler.py, merge unique functionality, archive others | Medium - test all 31 commands |
| mediclaw | 3 Ollama providers, 2 OpenRouter | Keep one of each, verify they route through Sovereign Gateway | Low - providers are interchangeable |
| llmclaw | 4 llm*.py command variants | Keep the one imported by handler, archive llm_backup/llm_enhanced/llm_smart | Low - check which one handler uses |
| webclaw | 2 A2A server implementations | Keep a2a_server.py, remove a2a/integrated_server.py | Low - verify no imports reference it |
| langclaw | langclaw_backup/ directory | Delete entirely | Low - already has langclaw/ |

Approach: One agent at a time. Check which file agent_handler.py imports. Keep that one. Archive the rest. Test /help after each.

### Infrastructure: Ollama Recovery
- Start ollama serve (currently not running)
- Switch active model to gemma3:4b (3.3GB, fits GTX 970 GPU)
- Verify Ollama fallback works in provider chain
- This eliminates the 4-agent timeout problem (lawclaw, docuclaw, interpretclaw, claw_coder)

### Priority 7: Security Assessment (IF TIME)
- Run ForbiddenPatternDetector against all agent handlers for Article I violations
- Test prompt injection: 10 known patterns against webclaw, lawclaw, claw_coder
- Document any direct LLM imports found (rustypycraw/groq_client.py is known)

### Beta Gate Progress (5 of 10 passed)
| # | Requirement | Status |
|---|-------------|--------|
| 1 | Enforcement blocks violations | DONE |
| 2 | Constitutional ledger repaired | DONE |
| 3 | Memory geographic filtering | DONE |
| 4 | All 21 agents tested | DONE |
| 5 | Provider fallback validated | DONE |
| 6 | Duplicate implementations reduced | NOT STARTED |
| 7 | Coverage tests added | NOT STARTED |
| 8 | Installation tested clean Windows | NOT STARTED |
| 9 | Installation tested clean Linux | NOT STARTED |
| 10 | Security review completed | NOT STARTED |



A few things I want locked in before the next session starts:

The consolidation ladder is set:

text
1. langclaw_backup     → delete (zero risk, no imports reference it)
2. llmclaw variants    → identify which llm*.py the handler imports, archive rest
3. mediclaw providers  → keep one Ollama + one OpenRouter, verify Sovereign Gateway routing
4. webclaw duplicate   → check which A2A server a2a_server.py actually imports
5. docuclaw merge      → inventory 3 implementations, keep agent_handler.py
6. flowclaw inventory  → READ-ONLY. Map imports. Find canonical file. No deletions.
The flowclaw rule is explicit:

No deletions in the first session. Only inventory:

Which flowclaw*.py does agent_handler.py import?

Do any of the 13 variants contain logic not present in the canonical file?

What do the engine/ modules actually do vs the standalone files?

Build the dependency map, then decide what moves to _archive/.

The May 30 lesson applies here directly:

Making broad structural changes before establishing the actual runtime path.

That's exactly what caused the handler-injection disaster. Flowclaw gets the inventory treatment because it's the highest-risk consolidation target.

Current state before next session:

5 of 10 Beta gates passed

Working tree clean, all commits pushed

Onboarding doc updated as operational runbook

shared/query_normalizer.py is canonical source for location extraction

All 21 agents tested and responsive

Provider chain: Groq primary, OpenRouter fallback, Ollama offline, Anthropic disabled

The project is in a good place to start consolidation work tomorrow.

