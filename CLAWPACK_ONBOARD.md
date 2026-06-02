# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg.

## CRITICAL: PowerShell Environment (Windows)
- NEVER use python -c with multi-line code. Write to scripts/_temp.py and run it.
- NEVER pipe to Out-File for files over 100 lines. PowerShell silently truncates.
- NEVER use PowerShell heredocs with Python code. They eat escape characters.
- **ECHO WORKS for small files.** echo "line" > file.py then echo "line2" >> file.py
  This is the ONLY reliable way to write Python command files under 10 lines.
- **Copy-Item WORKS for deployment.** Write once, copy to all targets.
- ALWAYS verify writes: python -c "print(len(open('path').read()))"
- ALWAYS kill Python before restarting: taskkill /F /IM python.exe 2>\
- ALWAYS clear __pycache__ after changing shared modules.
- READ POWERSHELL_SURVIVAL_GUIDE.md for full failure patterns and fixes.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None): at module level.
No manual registration - just drop the .py file in the directory.
**This is the preferred pattern for adding features to all agents.**
Do NOT batch-inject code into handlers. It corrupts indentation.
Write a command file once, then Copy-Item to all agents.

## CRITICAL LESSON: Command Files vs Handler Injection
On May 30, batch-injecting /voice code into 21 agent handlers via string replacement
corrupted indentation in ALL 21 agents. Required git revert to clean state.
The fix: write voice.py, listen.py, translate.py, braille_cmd.py as command files
in agents/lawclaw/commands/, then Copy-Item to all other agents.
Zero handler changes. Zero indentation risk. The system was designed for this.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

---

## Current State - May 30, 2026

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median /help latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Lifecycle cleanup errors | 0 (contract drift resolved) |
| Civic commands | Chronicle FTS5 direct (0.03-0.28s) |

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
| 2 | Ollama | deepseek-r1:8b | 0.8s | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |


## System-Wide Accessibility Toggles
| Toggle | Hotkey | Wake Word | Menu Key |
|--------|--------|-----------|----------|
| Voice mode | Ctrl+Shift+V | "start/stop listening" | v |
| Braille output | Ctrl+Shift+B | - | b |
| Neuralink | Ctrl+Shift+N | - | n |
| Eye tracking | Ctrl+Shift+E | - | e |
| Voice agent select | - | "switch to lawclaw" | s |


## Resolved This Session (May 30, 2026)

### Lifecycle Contract Drift - ALL FIXED
Three errors fired on every agent invocation, now eliminated. 0 cleanup errors.

### Civic Commands - Now Chronicle FTS5 Direct
/detention /police /library /hospital: 0.03-0.28s (was 45-90s via LLM).

### Provider Order Fixed
Groq primary (was Anthropic hardcoded in base_agent.py).

### Dreamclaw Timeout Fixed
/help 0.2s (was >20s). Skips _gather_context() for trivial commands.

### MathematicaClaw Fixed
/help and /stats work. Plots use interactive windows. Complex calculus: 12/18 passing.

### Accessibility Layer Built
shared/accessibility.py: TTS, STT, Braille, Translate, voice agent selection.
shared/voice_hook.py: System-wide toggle, Ctrl+Shift+V, wake words, background listener.
shared/io_adapter.py: Neuralink, eye tracker, switch device, sip-puff stubs.
shared/status_bar.py: Persistent accessibility status in agent responses.

### Enforcement Engine Activated
Pre-execution gate now fires on every A2A request. Tasks triggering constitutional
violations are blocked before agent processing. Currently non-blocking during
activation phase (try/except). Post-gate validation pending.

### Voice/Listen/Translate/Braille in All 21 Agents
Deployed as command files. Zero handler modifications. Zero indentation risk.


## Known Active Work (Not Blocking)
| Area | Scope |
|------|-------|
| Chronicle recover_by_context | RESOLVED - single-line fix in chronicle_helper.py |
| Capability routing | 7 partial agents need get_capable_agent() |
| Shared memory | fileclaw needs memory bridge |
| Enforcement engine | Pre-gate active in A2A path. Post-gate + policy content pending. |
| Guarded executor | Dormant |
| Registry | 5 agents outside AGENT_REGISTRY dict |
| pip install keyboard | Required for hotkeys to work |


## Quick Reference: Files That Matter
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active |
| shared/accessibility.py | TTS/STT/Braille/Translate | Active |
| shared/voice_hook.py | System-wide voice toggle + wake words | Active |
| shared/io_adapter.py | Neuralink/Eye/Switch input adapters | Active |
| shared/speech.py | TTS abstraction layer, voice profiles | Active |
| shared/accessibility_toggles.py | Braille/Neuralink/Eye toggles | Active |
| shared/status_bar.py | Accessibility status in responses | Active |
| shared/lifecycle.py | Agent cleanup supervisor | Active (0 errors) |
| shared/base_agent.py | Foundation class | Active |
| agents/lawclaw/agent_handler.py | Reference implementation | Gold standard |
| scripts/constitutional_test.py | 10-point compliance audit | Active |
| data/chronicle.db | 448MB SQLite FTS5 | Active |


## Session Log

2026-06-01 (evening): OBLITERATED MODELS + GPU TUNING + AGENT OUTPUTS
- /obliterated command fixed: now reads from models/obliterated/ directory instead of working_llms.json.
  Shows 6 real obliterated models (refusal_direction_ablation) with source model and technique metadata.
  Previously conflated Ollama -liberated models with true obliterated models.
- /models command still has labeling bug: shows -liberated models under "OBLITERATED" header.
- Active model switched to gemma3:4b (3.3GB, fits GPU). deepseek-r1:8b (5.2GB) too large for GTX 970.
- Ollama GPU: NVIDIA GeForce GTX 970, 4GB VRAM (~2.8GB available). CUDA enabled.
  OLLAMA_MAX_LOADED_MODELS=1 set to prevent multi-model VRAM exhaustion.
  Models that fit GPU: tinyllama (0.6GB), gemma3:1b (0.8GB), gemma3:4b (3.3GB), smollm2-liberated (3.4GB).
  Models that DO NOT fit: deepseek-r1:8b (5.2GB), codellama:7b (3.8GB), gemma3:12b+.
  Obliterated models in models/obliterated/: codellama_7b, deepseek_coder_6.7b, phi2, qwen_coder_7b, smollm2_1.7b, tinyllama.
  phi2 (2.7GB) recommended for best quality that fits GPU.
- Groq rate-limited all session. Fallback chain: Groq -> Ollama -> OpenRouter -> Anthropic.
  Ollama works but deepseek-r1:8b times out on CPU. gemma3:4b works on GPU.
  OpenRouter and Anthropic API keys set but untested this session.
- 15 agent output demos generated in docs/agent_outputs/ for screenshots:
  lawclaw (help, court Denver CO), claw_coder (help, python code gen),
  interpretclaw (help, Spanish contract translation), mediclaw (help),
  mathematicaclaw (help, derivative solved), docuclaw (help),
  flowclaw (help), plotclaw (help), dreamclaw (help),
  llmclaw (obliterated models, stats).
- Voice pipeline: works inside agents via event bus. Menu voice navigation needs non-blocking input.
  Hotkeys changed to Ctrl+Alt (Ctrl+Shift conflicts with Windows paste).
- X post published promoting multi-agent runtime. 11,240 clones/840 unique cloners in 14 days organic.
  May 30 spike: 408 unique cloners in single day. GitHub topics added for discoverability.
- LANDING.md, TECHNICAL_GUIDE.md, BEGINNERS_GUIDE.md added to docs/. install.bat and install.sh created.
 5 outdated auto-generated docs deleted. CLAWPACK_ONBOARD.md updated to June 1 state.

2026-05-31 / 2026-06-01: COURT RESOLVER + ACCESSIBILITY UNIFICATION + TIER 2 WIRING
- /court resolver: city-first traversal with all-county fallback search.
  Georgetown CO now resolves Clear_Creek/Georgetown/municipal_court.md in ~500ms.
  Previously returned entire state court_system.md (15k chars). Fix in court.py find_jurisdiction_files().
- shared/accessibility.py unified: voice toggle, braille, neuralink, eye tracking, TTS, STT,
  wake words ("start/stop listening"), auto-sleep after 2min silence, USB mic preference,
  / prefix auto-detection for voice commands, state name?code mapping (Nevada?NV),
  flexible command detection (finds command word anywhere in utterance).
- shared/event_bus.py: canonical event bus for all system input (voice, keyboard, API, system).
  CommandEvent dataclass with EventSource, EventIntent enums. Queue-based cross-thread delivery.
- a2a_server.py Tier 2 wiring: rate limiter on every POST, enforcement engine pre-execution gate,
  metrics counter per agent request, structured JSON logging, /metrics endpoint.
- agent=self passed to all 19 lawclaw command dispatches (previously all commands ran with agent=None,
  silently skipping Chronicle, A2A, cache, and jurisdiction lookups).
- jurisdiction.py: undefined variables fixed (sections?all_entities, final?structured).
  Cache now stores raw entity data + URLs, not LLM output. Cache re-renders from source on hit.
- 34 Miami-Dade reference files: mdcourts.gov (Maryland) ? jud11.flcourts.org (Florida 11th Circuit).
- chronicle_helper.py: safe dict/object access for Chronicle cards, stderr debug noise removed.
- llm/providers/__init__.py: Ollama now reads active model from active_model.json instead of hardcoded deepseek-r1:8b.
- 49 files across all 21 agents updated to import from unified shared.accessibility.
- clawpack.py: v key voice toggle with persistent VOICE ACTIVE banner, event bus poll in agent loop
  for hands-free voice commands inside agents, natural language command mapping.
- Voice pipeline functional: speech?transcribe?intent?prefix?A2A?response.
  Accuracy limited by speech_recognition library (not architecture). PWA uses native Web Speech API.
  Desktop voice is dev tooling; PWA is the production voice interface.

KNOWN ISSUES:
- Memory recall is jurisdiction-unaware. Bedford VA bleeds into Colorado queries because
  keyword index has no geographic filtering. Fix: add state/county/city metadata to memory writes
  and filter before semantic ranking in recall.
- Some remember() calls missing command= kwarg, causing "unknown" command tag in memory.
- Menu voice navigation works via event bus poll but requires msvcrt for non-blocking keyboard
  input on Windows (currently falls back to blocking input()).
- Ledger JSON corruption (Extra data: line 10373) from malformed append operations.
- LawClaw commands print at module level - loads for every agent, not just lawclaw.
- Missing cities in jurisdiction dataset (Greeley CO under Weld County, etc.).

2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. First cross-agent flow.

2026-05-29: Constitutional boundary activated. Consensus engine deployed.
Capability registry + lifecycle supervisor + memory staleness deployed.
PlotClaw schema imports fixed. Registry syntax repaired. /translate pipeline built.

2026-05-30: RUNTIME STABILIZATION + ACCESSIBILITY.
- Civic commands: Chronicle FTS5 direct (0.03-0.28s, was 45-90s).
- Provider order: Groq primary (was Anthropic hardcoded).
- Lifecycle contract drift: RESOLVED. 0 cleanup errors, all 21 agents.
- Dreamclaw: /help 0.2s (was >20s timeout).
- All 21 agents tested: 21/21 responsive, median /help 0.2s.
- All 4 LLM providers tested: all operational.
- MathematicaClaw: /help fixed, plots interactive, 12/18 calculus passing.
- Accessibility layer: TTS, STT, Braille, Translate, voice mode.
- System-wide toggles: Ctrl+Shift+V/B/N/E, wake words, menu keys.
- Voice/listen/translate/braille: 60 command files across all 21 agents.
- CRITICAL BUG: Batch handler injection corrupted all 21 agents. Reverted.
  Lesson: Use command files, never inject into handlers.
- README rewritten. Onboarding doc current. PowerShell survival guide created.
- System-wide language preference (/language es) with auto-translate at A2A boundary.
- Live bidirectional interpreter mode (/interpret) on all agents.
- Mobile PWA with voice input, agent discovery, offline support, PWA manifest.
- LawClaw handler cleaned: log_event and DecisionLedger.record replaced.
- CHRONICLE_GUIDE.md updated: removed stale get_timeline/log_event references.
- chronicle_helper.py fix: recover_by_context() now receives query argument.
  Single-line fix eliminated noise across all 21 agents.
- Enforcement engine wired: pre-execution gate active in A2A request path.
- shared/accessibility.py rewritten: escaped-quote corruption repaired (broken since creation).
- shared/speech.py: TTS abstraction with voice profiles, language routing, fallback chain.
- /speak command deployed to all 21 agents.
- /read refactored to use shared/speech.py.
- shared/accessibility_toggles.py: Braille, Neuralink, Eye tracking toggles.
- Menu banner shows VOICE ON/LANG/accessibility toggle status.
- Accessibility namespace collision resolved: flat naming (no package directory).
- recover_by_context signature drift FIXED (chronicle_helper.py single-line fix).
- UTF-16 encoding issue: echo writes produce null bytes. Fix script created.
  84 files fixed. Lesson: always run UTF-16 check after echo writes.
  84 files fixed. Lesson: always run UTF-16 check after echo writes.
