# DECISION_LOG.md — Architectural Decisions Record

## Why This Exists
This log documents WHY architectural decisions were made. It prevents future AI agents (or humans) from "fixing" something that was deliberately designed a certain way. Read this before modifying any constitutional pattern.

---

## 2026-05-29: /doc Route Lives in LawClaw, Not DocuClaw

**Decision:** /doc is a specialized lawclaw handler route, not a generic capability registry delegation.

**Why:** LawClaw enriches document requests with jurisdiction context (court addresses, filing rules, judge info) before delegating to docuclaw. This is domain enrichment — lawclaw doing legal research (its domain) and passing structured results to docuclaw (its domain). Moving /doc to pure capability routing would lose the enrichment layer.

**Constitutional basis:** Article II (Separation of Powers) — each agent performs its own domain function. Article III (Delegation) — enrichment before delegation is constitutional.

---

## 2026-05-29: /translate Route Lives in LawClaw, Not Just the Capability Registry

**Decision:** /translate is a specialized lawclaw handler route that chains through interpretclaw then docuclaw.

**Why:** Generic translation via the capability registry sends a bare string to interpretclaw. Legal translation requires preservation of Latin terms, French legal terms, case citations, statutory references, court names, and party names. LawClaw adds these preservation instructions before delegating. The docuclaw re-formatting step ensures translated documents have the same professional formatting as originals.

**Constitutional basis:** Same as /doc — domain enrichment before delegation.

---

## 2026-05-29: 23-System Constitutional Boundary (Not 13)

**Decision:** The handler boundary was expanded from 13 to 23 systems to achieve 100% shared infrastructure utilization.

**Why:** The original 13-system boundary covered core operational checks. The additional 10 systems (lifecycle, enforcement, guarded executor, execution policy, chronicle helper, procedural memory, three-tier memory, smart router, agent router, validation, log manager, shutdown, hooks) were built and tested but dormant. Activating them in the boundary ensures every command benefits from the full constitutional infrastructure without per-command edits.

**Constitutional basis:** Article XI (Enforcement) — the boundary is the enforcement point for constitutional compliance.

---

## 2026-05-29: Provider Priority Order (Ollama First, Anthropic Last)

**Decision:** active_model.json provider priorities: Ollama (1), OpenRouter (2), Groq (3), Direct Model (4), Anthropic (5).

**Why:** Anthropic credits are paid and limited. Ollama runs locally for free. OpenRouter has a free tier. Groq is cheap. Direct models are obliterated and free. The priority chain ensures paid APIs are only used when all free options are exhausted. Large translation tasks were burning Anthropic credits when local models could handle them.

**Constitutional basis:** Article VIII (Budget Sovereignty) — cost optimization is a constitutional concern.

---

## 2026-05-29: Shared Folder Cleanup — fork/, skills/, search/, batcher.py, latches.py Deleted

**Decision:** Deleted 11 files/folders from shared/ that were Claude Code-specific patterns not applicable to Clawpack's distributed architecture.

**Why:** Claude Code is a monolithic TypeScript process. Clawpack is a distributed federation of 21 Python agents. Patterns like fork agents (prompt cache sharing across parallel API calls), skills (markdown slash-command system), batcher (tool call batching), and latches (cache preservation) assume a single process with shared memory. They have no equivalent in Clawpack's A2A message-passing architecture.

**What was preserved:** hooks/types (the type definitions are useful; only the Claude Code-specific runners were deleted). compactor.py and decomposer.py (future-proofing for when context windows become a bottleneck).

---

## 2026-05-29: Capability Registry Instead of Master Agent

**Decision:** Universal command routing via shared/capabilities.py rather than a centralized "MasterClaw" agent.

**Why:** A master agent would centralize authority, collapse agent boundaries, and violate Article II (Separation of Powers). The capability registry preserves agent sovereignty — each agent recognizes when a command belongs to another ministry and delegates constitutionally. The registry is data, not an agent. It cannot accumulate power.

**Constitutional basis:** Article II Section 3 (No God Agents) — no agent may accumulate powers from multiple ministries.

---

## 2026-05-29: Citation Doctrine — WebClaw Owns Sources, DocuClaw Reflects Citations, Boundary Enforces Completeness

**Decision:** Citation attribution is distributed across existing ministries rather than centralized in a new subsystem.

**Why:** WebClaw already fetches and indexes all URLs to Chronicle. DocuClaw already renders the Constitutional Source Validation block. The boundary already checks command output. Adding a new attribution subsystem would duplicate these responsibilities. Instead, the boundary enforces that the existing ministries cooperate — checking that DocuClaw's validation block is present and source URLs are included.

**Constitutional basis:** Article V (Truth Hierarchy) — sources must be attributed. Article II (Separation of Powers) — each ministry has defined citation responsibilities.

---

## 2026-05-29: Consensus Engine Structured Claims (Not Raw Markdown)

**Decision:** The consensus engine extracts structured claims (citation:, concept:, source_url:) rather than storing raw LLM output.

**Why:** Raw markdown responses are noisy and incomparable across agents. Structured claims enable cross-agent consensus scoring. A citation confirmed by multiple agents across multiple sources builds a higher truth score than a single-agent claim. This prevents consensus pollution from verbose LLM output.

**Constitutional basis:** Article V (Truth Hierarchy) — structured claims enable verifiable truth scoring.

---

## 2026-05-29: _last_document Storage for Cross-Command Reference

**Decision:** The handler stores the last generated document in self._last_document for use by subsequent commands like /translate.

**Why:** The /translate command needs access to the previously generated contract or motion to translate it. Without storage, the translation would receive only the phrase "the contract" instead of the full document. This is session-scoped storage — it does not persist across sessions.

**Constitutional basis:** Article VI (Shared Memory) — cross-command context sharing within constitutional boundaries.

---

## Template for Future Decisions

When making architectural decisions, document:
1. **What** was decided
2. **Why** (the reasoning, not just the outcome)
3. **Constitutional basis** (which Article supports or constrains the decision)
4. **Alternatives considered** (what else was evaluated and why it was rejected)
5. **Date** (for chronological context)

## 2026-05-29: Consensus Engine — Domain-Aware Claim Extraction Needed for Non-Legal Agents

**Decision:** The consensus engine's _extract_claims() function currently uses US-legal-specific regex patterns (Bluebook citations, U.S. reporter format). When wiring mediclaw, txclaw, or other agents to the consensus engine, their claim extraction must be domain-aware.

**Why:** The current patterns match:
- Case citations: "Miranda v. Arizona, 384 U.S. 436 (1966)"
- Statutory references: "42 U.S.C. 1983"
- Legal concepts: lines starting with ** or ##

Medical claims, blockchain transactions, code patterns, and mathematical proofs have completely different structures. Running medical diagnoses through legal citation regex will produce zero matches and fall back to raw text extraction — causing consensus pollution.

**What needs to happen before wiring non-legal agents:**
1. Add agent_type parameter to _extract_claims(result, args, agent_type="legal")
2. Implement agent-specific extraction patterns:
   - "medical" — diagnoses, treatments, drug names, ICD codes, study citations
   - "blockchain" — transaction hashes, contract addresses, token amounts, block numbers
   - "code" — function signatures, file paths, error patterns, language-specific syntax
   - "math" — equations, theorems, proofs, numerical results
3. Each domain gets its own claim prefix namespace (diagnosis:, tx_hash:, function:, theorem:)
4. Cross-domain facts (like source_url:) remain universal

**Constitutional basis:** Article V (Truth Hierarchy) — claims must be comparable across agents to build consensus. Article II (Separation of Powers) — each agent's domain knowledge should inform how it extracts truth claims.
Circuit Breaker on All Cross-Agent Calls

**Decision:** Wired shared/error_handler.py CircuitBreaker into BaseAgent.call_agent(). 5 consecutive failures opens circuit for 60 seconds, then half-open with 3 test calls.

**Why:** Without circuit breakers, a failed agent could cause infinite retry loops across the mesh. The circuit breaker fails fast ? after 5 failures, subsequent calls return immediately with "[agent] unavailable" rather than retrying.

**Constitutional basis:** Article VIII (Budget Sovereignty) and Article VII (Silent Failure).

---

## 2026-05-29 (evening): lookup_jurisdiction() on BaseAgent via Chronicle FTS5

**Decision:** Added lookup_jurisdiction(city_state, resource_type) to BaseAgent. All 21 agents inherit library, hospital, police, and building code lookup from 3,800+ city jurisdiction files via Chronicle FTS5.

**Why:** Files organized by county, not city. Chronicle FTS5 searches across boundaries automatically.

**Constitutional basis:** Article VI (Shared Memory) ? one canonical data source for all agents.

---

## 2026-05-29 (evening): Command Migration from Direct HTTP to Agent Context

**Decision:** All lawclaw commands migrated from direct HTTP to agent context methods (agent.ask_llm(), agent.call_agent(), agent.search_chronicle()).

**Why:** Direct HTTP bypasses circuit breaker, task state tracking, and budget enforcement.

**Constitutional basis:** Article I (Sovereignty) and Article III (Delegation).

---

## 2026-05-29 (evening): 36-System Constitutional Boundary

**Decision:** Expanded handler boundary from 23 to 36 systems across 19/21 agents.

**Why:** Added systems were built but dormant. Activating them ensures full constitutional coverage.

**Constitutional basis:** Article XI (Enforcement).

---

## 2026-05-29 (evening): Task State Machine on All Cross-Agent Calls

**Decision:** Every call_agent() creates trackable task (pending->running->completed/failed/killed) with persistent storage. Pattern from Claude Code Ch8-10.

**Why:** Operational visibility, failure analysis, performance metrics. Foundation for async delegation.

**Constitutional basis:** Article VII (Silent Failure).

---

## 2026-05-29 (evening): Memory Staleness Warnings

**Decision:** Facts from _memory.recall() carry age warnings. Pattern from Claude Code Ch11.

**Why:** Stale facts need staleness metadata. Human-readable age triggers appropriate skepticism.

**Constitutional basis:** Article V (Truth Hierarchy).

---

## 2026-05-29 (evening): Search Cache via DataClaw

**Decision:** cached_search() on BaseAgent. 24hr TTL, organized by agent in dataclaw/cache/.

**Why:** Repeat searches waste tokens. DataClaw becomes canonical cache layer.

**Constitutional basis:** Article VIII (Budget Sovereignty).


---

## 2026-05-30: Groq as Primary Provider (Not Anthropic)

**Decision:** Changed provider priority order to Groq (1), Ollama (2), OpenRouter (3), Anthropic (4). Previously Anthropic was hardcoded as primary in base_agent.py ask_llm().

**Why:** Anthropic credits are paid and limited. Groq is free and faster (0.7s vs 1.2s). The hardcoded provider='anthropic' in ask_llm() bypassed the entire provider chain configuration. Removing it allows the Sovereign Gateway to use its natural priority order from detect_providers().

**Constitutional basis:** Article I (Sovereignty) and Article VIII (Budget Sovereignty).

---

## 2026-05-30: Civic Commands Use Chronicle FTS5 Direct (No LLM)

**Decision:** /detention, /police, /library, /hospital now query Chronicle FTS5 directly via agent.lookup_jurisdiction(). Previously they called _gather_context() -> webclaw -> LLM (45-90s latency).

**Why:** These commands were missing from lawclaw's handler if/elif dispatch chain. They fell through to the else block which called the full LLM pipeline. The data already exists in the 3,800-city Chronicle index. Direct FTS5 lookup returns in 0.03-0.28s with zero API calls.

**Lesson:** Always check if a command is in the handler dispatch chain. Missing commands silently fall to the expensive else path.

**Constitutional basis:** Article V (Truth Hierarchy) ? chronicle data should be used directly when available, not re-synthesized through inference.

---

## 2026-05-30: Lifecycle Contract Drift Resolution

**Decision:** Fixed three API contract mismatches that caused errors on every agent invocation:
- log_event: symbol removed from chronicle_ledger, replaced with get_chronicle().record_fetch()
- DecisionLedger.record(action=): signature changed to record_action(agent, action, policy_result)
- ChronicleLedger.record_fetch(agent=): kwarg changed to url=

**Why:** The shared API layer had drifted from its callers. These errors fired on every single agent invocation but were caught by except blocks, making them silent but noisy in logs. Centralized fix in shared/lifecycle.py and shared/_agent_helpers.py cleaned all 21 agents simultaneously.

**Constitutional basis:** Article VII (Silent Failure) ? exceptions must not be silenced without audit visibility.

---

## 2026-05-30: Command Files Instead of Handler Injection

**Decision:** Accessibility commands (/voice, /listen, /translate, /braille) deployed as command files in each agent's commands/ directory. Zero handler modifications.

**Why:** A batch Python script attempted to inject these commands into 21 agent handlers via string replacement. Result: ALL 21 agents corrupted with indentation errors. Required git revert. The system was designed for commands/ directory loading ? dropping a .py file with name="/commandname" and def run(args, agent=None) is the intended extension mechanism.

**Lesson:** Write once with echo, Copy-Item to deploy. Never batch-inject into handlers.

**Constitutional basis:** Article II (Separation of Powers) ? command files preserve agent handler integrity.

---

## 2026-05-30: System-Wide Voice Toggle (Not Per-Agent)

**Decision:** Voice mode is a global toggle (shared/voice_hook.py), not per-agent state. Ctrl+Shift+V toggles system-wide. Wake words ("start listening"/"stop listening") provide hands-free control. The background listener routes to whichever agent is currently active via A2A.

**Why:** Per-agent voice toggles would require activation in every agent separately. A Spanish speaker navigating between agents would need to re-enable voice each time. Global state with persistent banner ensures continuity.

**Constitutional basis:** Article III (Delegation) ? accessibility is infrastructure, not an agent domain.

---

## 2026-05-30: Accessibility as Shared Infrastructure (Not Agent Feature)

**Decision:** TTS, STT, Braille, translation, and IO adapters live in shared/ (accessibility.py, voice_hook.py, io_adapter.py, status_bar.py). No agent owns accessibility. Every agent inherits it.

**Why:** Accessibility is universal infrastructure, not a domain specialty. interpretclaw handles translation quality but the pipeline itself is shared. This prevents duplication and ensures consistent behavior across all 21 agents.

**Constitutional basis:** Article VI (Shared Memory) ? accessibility is a shared capability, not a ministry.

---

## 2026-05-30: PowerShell Environment Constraints

**Decision:** All file writes in this environment must use echo for small files (<10 lines) or Python scripts executed from disk for larger files. Never use python -c with multi-line code, never use PowerShell heredocs with Python, never use Out-File for files over ~100 lines.

**Why:** Approximately 2 hours were lost to PowerShell-specific failures. These constraints are documented in POWERSHELL_SURVIVAL_GUIDE.md and CLAWPACK_ONBOARD.md.

**Constitutional basis:** Operational ? not constitutional, but necessary for any agent to function in this environment.
 
 # #   2 0 2 6 - 0 6 - 0 2 :   S o v e r e i g n t y   E n f o r c e m e n t   A c t i v a t e d   a s   H T T P   F i r e w a l l   ( N o t   F u l l   E n g i n e )  
  
 * * D e c i s i o n : * *   A c t i v a t e d   F o r b i d d e n P a t t e r n D e t e c t o r . s c a n _ t a s k ( )   a t   t h e   H T T P   b o u n d a r y   i n   a 2 a _ s e r v e r . p y   r a t h e r   t h a n   w i r i n g   t h e   f u l l   E n f o r c e m e n t E n g i n e . e x e c u t e _ w i t h _ e n f o r c e m e n t ( )   p i p e l i n e .  
  
 * * W h y : * *   T h e   E n f o r c e m e n t E n g i n e   r e q u i r e s   m a n d a t o r y   r e f e r e n c e   f i l e s   ( O P E R A T I N G _ R U L E S . m d ,   R E F E R E N C E _ R A N K I N G . m d ,   S Y S T E M _ O V E R V I E W . m d )   t h a t   d o   n o t   e x i s t   i n   C l a w p a c k .   A t t e m p t i n g   t o   w i r e   i t   c a u s e d   a l l   r e q u e s t s   t o   b e   b l o c k e d   a f t e r   3   r e c u r s i v e   a t t e m p t s .   T h e   d e t e c t o r   p r o v i d e s   i m m e d i a t e   s o v e r e i g n t y   p r o t e c t i o n   w i t h o u t   t h e   r e f e r e n c e - l o a d i n g   d e p e n d e n c y .  
  
 * * T r a d e : * *   G a i n e d   r e l i a b l e   4 0 3   b l o c k i n g   o f   6   s o v e r e i g n t y   v i o l a t i o n   p a t t e r n s .   L o s t :   r e f e r e n c e - d r i v e n   v a l i d a t i o n ,   e s c a l a t i o n   l o g i c ,   c o n f i d e n c e   s c o r i n g ,   r e c u r s i v e   e n f o r c e m e n t   l o o p ,   p o s t - e x e c u t i o n   r e s p o n s e   s c a n n i n g .   T h e s e   r e m a i n   i n   s h a r e d / e n f o r c e m e n t /   f o r   f u t u r e   a c t i v a t i o n   w h e n   r e f e r e n c e   f i l e s   a r e   c r e a t e d .  
  
 * * C o n s t i t u t i o n a l   b a s i s : * *   A r t i c l e   I   ( S o v e r e i g n t y )   -   d i r e c t   L L M   p r o v i d e r   a c c e s s   i s   b l o c k e d   b e f o r e   a g e n t   d i s p a t c h .   A r t i c l e   X I   ( E n f o r c e m e n t )   -   t h e   e n f o r c e m e n t   e n g i n e   e x i s t s   b u t   o p e r a t e s   i n   s i m p l i f i e d   m o d e   p e n d i n g   r e f e r e n c e   i n f r a s t r u c t u r e .  
  
 * * P a t h   t o   f u l l   e n g i n e : * *   C r e a t e   d a t a / e n f o r c e m e n t / O P E R A T I N G _ R U L E S . m d ,   R E F E R E N C E _ R A N K I N G . m d ,   S Y S T E M _ O V E R V I E W . m d ,   t h e n   r e p l a c e   t h e   d e t e c t o r - o n l y   g a t e   w i t h   t h e   f u l l   e x e c u t e _ w i t h _ e n f o r c e m e n t ( )   p i p e l i n e .  
 