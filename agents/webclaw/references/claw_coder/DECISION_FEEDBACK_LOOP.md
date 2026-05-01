# DECISION_FEEDBACK_LOOP.md
## Self-Improving Retrieval Architecture

### Core Principle
Every major engineering decision must leave a scar.
If the system made a choice, it must create an artifact.
No invisible decisions. No repeated mistakes.

---

### Decision Logging Triggers

| Event | Required Artifact | Destination |
|-------|-------------------|-------------|
| Architecture decision | Decision record with trade-offs | `decision_logs/` |
| Production failure | Postmortem | `truth_sources/incident_reports/` |
| Rollback required | Failure mode analysis | `failure_modes/` |
| Performance fix applied | Before/after analysis | `debugging/performance_bottlenecks/` |
| Security incident | Breach analysis | `truth_sources/security_breaches/` |
| Scaling failure | Scaling postmortem | `truth_sources/scaling_failures/` |
| Build vs buy outcome | Decision outcome (6-month review) | `engineering_decisions/build_vs_buy/` |
| Refactor completed | Refactor outcome report | `golden_examples/excellent_refactors/` |
| API breaking change | Migration incident report | `truth_sources/why_systems_died/` |

---

### Forced Postmortem Protocol

Every failure triggers a structured postmortem answering:
What failed?

Exact error, behavior, or outcome

Why did it fail?

Root cause, not symptom

Why did existing references fail to prevent this?

Which reference was wrong or incomplete?

Which reference was ignored?

Which reference didn't exist?

What retrieval trigger should have fired?

Should a new trigger keyword exist?

Should an existing trigger be modified?

What must be updated?

truth_sources/ (mandatory)

failure_modes/ (if new failure pattern)

REFERENCE_SELECTION_PROTOCOL.md (if new trigger needed)

TRUTH_HIERARCHY.md (if authority conflict found)

text

---

### Reference Mutation Rules

#### Rule 1: Never Overwrite History
WRONG:
Delete old assumption and replace with new one

RIGHT:
Append new finding with date and context
Preserve original assumption for historical record

text

#### Rule 2: Always Add—Never Delete
Add: failure cases, contradictions, exceptions, edge cases
Never delete: prior assumptions, prior recommendations

Pattern: "As of [DATE], this approach has been validated/falsified by..."

text

#### Rule 3: Contradiction Format
When truth_sources contradicts golden_examples:

File: golden_examples/excellent_backend/excellent_backend.md
Append:
⚠️ CONTRADICTION [DATE]
Pattern X was recommended here, but postmortem Y shows it failed
at [COMPANY] under [CONDITIONS]. See truth_sources/incident_reports/Y.md.

APPLICABILITY: This pattern is valid EXCEPT when [CONDITIONS].

text

#### Rule 4: Edge Case Addition
When a pattern works 99% of the time but fails in specific cases:

File: constraints/high_scale/high_scale.md
Append:
⚠️ EDGE CASE [DATE]
This constraint does not apply when:

[SPECIFIC CONDITION 1]

[SPECIFIC CONDITION 2]
Source: [INCIDENT/POSTMORTEM REFERENCE]

text

---

### Retrieval Upgrade Trigger (Repeat Failure Protocol)
IF same class of failure occurs TWICE:

MANDATORY ACTIONS:

New failure_mode entry created

REFERENCE_SELECTION_PROTOCOL.md updated with new trigger

TRUTH_HIERARCHY.md reviewed for authority conflicts

RETRIEVAL_BUDGET_POLICY.md - consider upgrading priority

Repeat failures are architecture failures.
Not user failures.

text

---

### Automatic Reference Scoring Updates

| Outcome | Scoring Change |
|---------|----------------|
| Pattern prevents failure | Reference weight +1 |
| Pattern fails in production | Reference weight -2 |
| Pattern fails twice | Reference flagged ⚠️ UNRELIABLE |
| New pattern discovered | Initial weight = 3, review in 6 months |
| Pattern validated by 3+ sources | Reference weight +2, marked ✅ VALIDATED |
| Pattern contradicted by truth_sources | Reference flagged ❌ CONTRAINDICATED |

---

### Knowledge Accumulation Cycle
User Task
↓
Retrieval (governed by protocol)
↓
LLM Execution
↓
OUTCOME DETECTED:
├── Success → Log pattern effectiveness
├── Failure → Forced postmortem
├── Rollback → Failure mode analysis
├── Performance fix → Bottleneck documentation
└── Security incident → Breach analysis
↓
Reference Mutation (append, never overwrite)
↓
Retrieval Protocol Updates (if repeat failure)
↓
System is smarter for next task

text

---

### Why This Exists

Without feedback loop:
- The system retrieves wisdom but cannot accumulate it
- Patterns that fail are repeated indefinitely
- The same mistakes require the same human intervention

With feedback loop:
- Every failure improves the retrieval system
- Scar tissue accumulates automatically
- The system becomes a principal engineer, not a librarian

---

### Initial State

This file activates on first major decision event.

Until then, the retrieval protocols operate as designed.

On first failure, the postmortem template is invoked.

On second failure of the same class, the escalation protocol triggers.

The system is now learning.