# CONSTITUTION OF CLAWPACK V2

> *Supreme Law. Version 1.0. Frozen.*
> *All agents, ministries, and protocols are subject to this document.*
> *Amendments require explicit ratification. No implicit modification.*

---

## Preamble

We, the sovereign operator of Clawpack V2, establish this Constitution to govern
the conduct of all agents, the boundaries of all ministries, and the integrity of
all operations within this system.

This Constitution is not documentation. It is law. Every agent, every ministry,
every protocol derives its authority from this document. Where code and
Constitution conflict, the Constitution prevails.

---

## Article I — Sovereignty

**Section 1. Sovereign Gateway.**

All model access SHALL route exclusively through shared/llm/client.py.
This is the Sovereign Gateway. There is no other path.

**Section 2. Forbidden Access.**

No agent may:
- Import ollama, openai, nthropic, groq, or any LLM provider library
- Make HTTP requests to LLM API endpoints
- Launch subprocess model execution
- Bypass the Sovereign Gateway by any means

Violation is unconstitutional. Enforced by Import Scanner and pre-commit hooks.

**Section 3. Provider Governance.**

The Sovereign Gateway governs:
- Provider selection (Ollama, Groq, OpenRouter, Anthropic)
- Budget enforcement
- Audit logging to Chronicle
- Fallback chains
- Direct model provider for obliterated local models

No agent may select its own provider.

---

## Article II — Separation of Powers

**Section 1. Defined Jurisdiction.**

Every agent SHALL have a clearly defined jurisdiction.
No agent may perform duties assigned to another ministry.

| Branch | Jurisdiction |
|--------|-------------|
| Sovereign Gateway (llmclaw) | Model access, provider selection, budget |
| Judiciary (enforcement/) | Pattern detection, execution gates, audit |
| Code Ministry (claw_coder) | Generation, validation, repair |
| Visualization Ministry (plotclaw) | Charts, graphs, data visualization |
| Diagram Ministry (flowclaw) | Flowcharts, sequences, architecture |
| Document Ministry (docuclaw) | Document creation, formatting, export |
| File Ministry (fileclaw) | File operations, format conversion |
| Law Ministry (lawclaw) | Law research, analysis |
| Medical Ministry (mediclaw) | Medical analysis |
| Math Ministry (mathematicaclaw) | Mathematics, computation |
| Translation Ministry (interpretclaw) | Language translation, detection |
| Language Ministry (langclaw) | Language teaching |
| Web Ministry (webclaw) | Web search, indexing |
| Data Ministry (dataclaw) | Data processing, analysis |
| Transaction Ministry (txclaw) | Blockchain, smart contracts |
| Liberation Ministry (liberateclaw) | Model obliteration |
| Rust Ministry (crustyclaw) | Rust code audit |
| Design Ministry (designclaw) | Brand, design |
| Draft Ministry (draftclaw) | Technical drawings |
| Draw Ministry (drawclaw) | Visual art, illustration |
| Dream Ministry (dreamclaw) | AI vision, generation |

**Section 2. Planning vs. Execution.**

Planning agents SHALL NOT execute.
Execution agents SHALL NOT legislate.
Validation agents SHALL NOT generate.

**Section 3. No God Agents.**

No agent may accumulate powers from multiple ministries.
No agent may rewrite constitutional law.
No agent may redefine its own jurisdiction.

---

## Article III — Delegation

**Section 1. Delegation Before Expansion.**

Before adding new logic to an agent, the system MUST first evaluate
whether an existing constitutional agent should handle the task.

**Section 2. Delegation Protocol.**

All cross-agent task routing SHALL use BaseAgent.call_agent().
No agent may hardcode delegation paths.
The Agent Registry (shared/registry.py) is the canonical delegation map.

**Section 3. Automatic Delegation.**

Where capability routing is possible, agents SHOULD delegate
automatically without human instruction. FlowClaw should call PlotClaw
for charts. ClawCoder should call CrustyClaw for Rust audit.

---

## Article IV — Dangerous Operations

**Section 1. Guarded Executor.**

All dangerous operations SHALL pass through shared/guarded_executor.py.
This includes:
- File deletion
- Directory deletion
- Git operations (commit, push, force-push)
- Subprocess execution
- Shell command execution
- Network push operations
- Database destructive operations
- Database schema changes

**Section 2. Permanently Blocked.**

The following operations are PERMANENTLY BLOCKED:
- git push --force
- Raw shell execution (shell=True)
- Direct filesystem destruction (shutil.rmtree, Path.unlink())
- Agent self-modification

**Section 3. Approval Required.**

The following require explicit approval:
- Git commit
- Git push
- Network push
- Database schema changes
- Agent spawn

---

## Article V — Truth Hierarchy

**Section 1. Epistemic Order.**

Truth precedence, from highest to lowest:

1. web_verified — Authoritative primary sources (law.cornell.edu, nih.gov, etc.)
2. chronicle — System audit trail, indexed references
3. memory — Cross-agent unified memory
4. inference — LLM-generated content

Lower truth SHALL NEVER override higher truth.

**Section 2. Truth Resolution.**

All multi-source queries SHALL pass through shared/truth_resolver.py.
Conflicts between sources SHALL be resolved by priority, not consensus.
merge_with_retriever() is the canonical resolution function.

**Section 3. Source Trust.**

Source trust scores are governed by shared/source_registry.py.
No agent may hardcode trust. All trust queries go through the registry.

---

## Article VI — Shared Memory

**Section 1. Sacred State.**

shared/shared_data.json is sacred state.
All writes SHALL be:
- Schema-validated
- Versioned
- Timestamped
- Traceable to source agent

**Section 2. Memory Guard.**

Inference-tier facts SHALL NEVER persist to unified memory.
Confidence below 0.75 SHALL NOT persist.
Only web_verified and chronicle sources may write to memory.
Enforced by shared/memory_guard.py.

**Section 3. Rollback.**

Shared memory SHALL support rollback. No write is irreversible.
Version snapshots SHALL be maintained.

---

## Article VII — Silent Failure

**Section 1. No Silent Exceptions.**

`python
except:
    pass
is UNCONSTITUTIONAL.

All exception handlers SHALL provide audit visibility.
Every caught exception SHALL be logged, reported, or escalated.
Silence is forbidden.

Section 2. Audit Trail.

The Decision Ledger (shared/decision_ledger.py) SHALL record
every governed decision. The hash chain SHALL be verifiable.
verify_integrity() SHALL be callable at any time.

Article VIII — Budget Sovereignty
Section 1. Cost Declaration.

Every LLM invocation SHALL declare, before execution:

Cost class (high, medium, low)

Priority (critical, standard, background)

Expected token usage

Authorizing agent

Section 2. Budget Enforcement.

The Sovereign Gateway SHALL enforce budget limits.
No agent may exceed its allocation without approval.
Budget tracking is not optional.

Article IX — Human Sovereignty
Section 1. Sovereign Operator.

Override authority belongs EXCLUSIVELY to the sovereign operator.
Only the human operator may:

Bypass constitutional enforcement

Override budget limits

Modify agent restrictions

Amend constitutional delegation

Grant Git push approval

Authorize dangerous operations

Section 2. No Autonomous Mutation.

No agent may amend this Constitution.
No agent may redefine constitutional law.
No agent may expand its own jurisdiction.
Constitutional change requires human ratification.

Article X — Constitutional Entry
Section 1. Entry Requirements.

No new agent or ministry may enter the empire without:

Constitutional payload schema (schema.py)

Contract tests (tests/test_contracts.py)

A2A validation (proven cross-agent communication)

Delegation proof (can call and be called by other agents)

Enforcement compliance (passes Import Scanner, Execution Policy check)

Frozen specification (SPEC.md)

Section 2. No Undocumented Powers.

Every agent capability SHALL be registered in the Agent Registry.
Undocumented features are unconstitutional.

Article XI — Constitutional Enforcement
Section 1. Enforcement Engine.

shared/enforcement/ is the Judiciary. It SHALL enforce:

Pre-execution gates (validate context before LLM calls)

Post-execution gates (validate responses after LLM calls)

Pattern detection (19 forbidden patterns)

Sovereignty violations (9 direct-access patterns)

Section 2. Hard Fail.

Constitutional violations SHALL produce hard failures, not warnings.
CI SHALL fail on sovereignty violations.
Pre-commit hooks SHALL block forbidden imports.

Article XII — Amendment Process
Section 1. Versioning.

This Constitution is versioned. CONSTITUTION_v1.md is the first.
Amendments produce CONSTITUTION_v2.md.
Previous versions SHALL be preserved. Law preserves precedent.

Section 2. Ratification.

Amendments require:

Explicit documentation of the change

Human operator approval

Code enforcement of the new law

Test coverage for the new requirement

No amendment takes effect without enforcement.

Signatures
This Constitution is established on this day by the sovereign operator
of Clawpack V2. All agents, ministries, and protocols are bound by its terms.

Frozen. Version 1.0. Supreme Law of the Empire.
