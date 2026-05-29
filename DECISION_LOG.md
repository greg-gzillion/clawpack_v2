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
