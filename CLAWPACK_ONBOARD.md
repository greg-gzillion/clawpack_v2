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

---

## System-Wide Accessibility Toggles
| Toggle | Hotkey | Wake Word | Menu Key |
|--------|--------|-----------|----------|
| Voice mode | Ctrl+Shift+V | "start/stop listening" | v |
| Braille output | Ctrl+Shift+B | - | b |
| Neuralink | Ctrl+Shift+N | - | n |
| Eye tracking | Ctrl+Shift+E | - | e |
| Voice agent select | - | "switch to lawclaw" | s |

---

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

---

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

---

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
| shared/speech.py | TTS abstraction layer, voice profiles | Active |
| shared/accessibility_toggles.py | Braille/Neuralink/Eye toggles | Active |
| shared/status_bar.py | Accessibility status in responses | Active |
| shared/lifecycle.py | Agent cleanup supervisor | Active (0 errors) |
| shared/base_agent.py | Foundation class | Active |
| agents/lawclaw/agent_handler.py | Reference implementation | Gold standard |
| scripts/constitutional_test.py | 10-point compliance audit | Active |
| data/chronicle.db | 448MB SQLite FTS5 | Active |

---

## Session Log

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
