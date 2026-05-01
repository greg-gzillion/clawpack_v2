# EXECUTION_ENFORCEMENT_LAYER.md
## Mandatory Pre/Post Execution Validation Gates

### Core Principle
If retrieval law exists, execution must be unable to bypass it.
The system must fail closed, not fail open.
Doctrine without enforcement is philosophy.
Doctrine with enforcement is operating law.

---

### PRE-EXECUTION VALIDATION GATE

#### Gate Check: Before Any LLM Call
EXECUTION BLOCKED UNTIL ALL CHECKS PASS:

[ ] Mandatory References Loaded

OPERATING_RULES.md

REFERENCE_RANKING.md

SYSTEM_OVERVIEW.md

[ ] Trigger Retrieval Completed

REFERENCE_SELECTION_PROTOCOL.md triggers evaluated

All triggered references retrieved

[ ] Budget Policy Enforced

RETRIEVAL_BUDGET_POLICY.md applied

References trimmed if over budget

Priority injection order followed

[ ] Truth Hierarchy Checked

TRUTH_HIERARCHY.md applied to all retrieved references

Conflicts resolved per protocol

Contradicted patterns flagged

[ ] Domain Safety Gates Passed

Financial → regulatory_constraints retrieved

Security → cybersecurity retrieved

Architecture → distributed_systems reviewed

Scale → high_scale constraints reviewed

If ANY check fails:
→ EXECUTION BLOCKED
→ Missing references force-retrieved
→ Gate re-run from start

text

---

### FORBIDDEN FAILURE STATES

#### Hard Blocks (No Exceptions)

These patterns, if detected in agent reasoning, force execution rejection:

| Forbidden Pattern | Why Blocked | Mandatory Retrieval |
|-------------------|-------------|---------------------|
| "We should optimize this early" | Premature optimization killed countless projects | `failure_modes/premature_optimization/` |
| "Let's rewrite from scratch" | Rewrites have >70% failure rate | `engineering_decisions/kill_decisions/` + `truth_sources/why_systems_died/` |
| "Microservices will solve this" | Distributed monolith risk | `architecture/distributed_systems/` + `failure_modes/distributed_system_traps/` |
| "We'll add that later" (security/financial) | Deferred safety = no safety | Domain-specific constraints |
| "It works on my machine" | Production reality ignored | `truth_sources/production_incidents/` |
| "Just use [trendy new thing]" | No production validation | `truth_sources/` + validation gate |
| "The framework handles that" | Abstication without understanding | `failure_modes/abstraction_leaks/` |
| "We don't need tests for this" | Testing is not optional | `key_guidelines/testing_guidelines/` |
| Financial system without regulatory review | Illegal or catastrophic | `constraints/regulatory_constraints/` |
| Security recommendation without cyber review | Reckless | `cybersecurity/` + `truth_sources/security_breaches/` |

#### Detection Mechanism
POST-REASONING SCAN:

Parse agent output for forbidden patterns

If pattern detected → check if corresponding constraint was retrieved

If constraint NOT in context → BLOCK RESPONSE

Force retrieval of missing constraint

Re-run reasoning with constraint injected

text

---

### POST-EXECUTION RESPONSE VALIDATION GATE

#### Gate Check: Before Response Returned to User
RESPONSE BLOCKED UNTIL ALL CHECKS PASS:

[ ] Constraint Compliance

Recommendation does not violate any retrieved constraint

Financial/security domains explicitly addressed

[ ] Failure Mode Consideration

Retrieved failure_modes explicitly referenced in reasoning

Alternative approaches acknowledged where failure risks exist

[ ] Truth Source Alignment

Recommendation does not contradict known production outcomes

If truth_sources warns against pattern → pattern not recommended

If no truth_sources exist → warning injected

[ ] Confidence Classification Applied

Response labeled: VALIDATED / REASONED / UNTESTED

UNTESTED responses include mandatory warning

No silent uncertainty allowed

[ ] Escalation Checked

If UNTESTED + financial/security/architecture → flagged for review

If pattern failed twice before → blocked, alternative required

If ANY check fails:
→ RESPONSE REJECTED
→ Missing analysis forced
→ Gate re-run from start

text

---

### CONFIDENCE CLASSIFICATION SYSTEM

#### Every Major Recommendation Must Be Labeled

| Classification | Criteria | Required In Response |
|----------------|----------|---------------------|
| ✅ VALIDATED | Supported by truth_sources AND constraints | Explicit citation of validating sources |
| 📋 REASONED | Supported by engineering_decisions AND failure_modes | Explicit explanation of reasoning path |
| ⚠️ UNTESTED | No production validation exists | Mandatory warning: "This approach lacks production validation. Proceed with caution." |

#### Mandatory Warning Format
⚠️ CONFIDENCE: UNTESTED
This recommendation has not been validated against production incidents.
No truth_sources entry confirms or denies this approach.
Consider:

Testing in isolation before production use

Adding findings to truth_sources/ after validation

Reviewing if a VALIDATED alternative exists

text

---

### ESCALATION PROTOCOL

#### Auto-Escalation Triggers

| Condition | Action |
|-----------|--------|
| UNTESTED + financial domain | Flag for human review, response includes explicit risk statement |
| UNTESTED + security domain | Flag for human review, response includes threat model gaps |
| UNTESTED + architecture decision | Flag for human review, response includes rollback plan |
| Same failure pattern twice | ESCALATE: System-level review required, update all protocols |
| 3+ forbidden patterns in one task | ESCALATE: Task may be malformed or outside system capability |
| truth_sources contradicts response | BLOCK: Response must be regenerated with truth priority |

#### Escalation Output Format
🔴 ESCALATION REQUIRED
Domain: [FINANCIAL/SECURITY/ARCHITECTURE]
Reason: [UNTESTED recommendation in critical domain]
Risk: [Specific risk statement]
Action Required: Human review before implementation
Reference Gaps: [Missing truth_sources, missing constraints]

text

---

### ENFORCEMENT INTEGRATION

#### Where This File Sits in the Stack
Task Received
↓
PRE-EXECUTION GATE ← EXECUTION_ENFORCEMENT_LAYER.md
├── All mandatory references loaded?
├── All triggers fired?
├── Budget enforced?
├── Truth hierarchy resolved?
└── Domain safety gates passed?
↓ (if all pass)
Retrieval + Context Assembly
↓
LLM Execution
↓
POST-EXECUTION GATE ← EXECUTION_ENFORCEMENT_LAYER.md
├── Forbidden patterns detected?
├── Constraints violated?
├── Failure modes considered?
├── Truth sources aligned?
├── Confidence classified?
└── Escalation needed?
↓ (if all pass)
Response Delivered to User

text

#### Implementation Requirement
This file MUST be implemented as:

A pre-execution hook in the agent orchestrator

A post-execution hook before response return

NOT as a prompt suggestion

NOT as an optional guideline

If the enforcement layer cannot run:

Execution must be blocked

The system must fail closed

No degraded mode permitted

Enforcement is not optional.
Enforcement is the difference between doctrine and philosophy.

text

---

### Why This Exists

Without enforcement:
- Agents can ignore retrieval protocols
- Forbidden patterns slip through
- Confidence is never classified
- The architecture is advisory, not binding

With enforcement:
- Every execution is validated
- Every response is checked
- Every failure is caught
- The architecture becomes law

This is not a "nice to have."
This is the difference between an agent framework and a governed system.
The Complete Governance Stack
text
webclaw/references/claw_coder/
├── OPERATING_RULES.md                    ← Constitutional law
├── REFERENCE_SELECTION_PROTOCOL.md        ← WHAT to retrieve (triggers)
├── RETRIEVAL_BUDGET_POLICY.md             ← HOW MUCH to retrieve (budget)
├── TRUTH_HIERARCHY.md                     ← WHO WINS on conflict (arbitration)
├── DECISION_FEEDBACK_LOOP.md              ← SELF-IMPROVEMENT (learning)
├── EXECUTION_ENFORCEMENT_LAYER.md         ← GATES + BLOCKS (enforcement)
├── REFERENCE_RANKING.md                   ← Priority weights
├── SYSTEM_OVERVIEW.md                     ← Architecture documentation
├── retrieval_priority.md                  ← Injection ordering
└── generate_references.py                 ← Reference generation