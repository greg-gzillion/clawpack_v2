# TRUTH_HIERARCHY.md
## Conflict Resolution Protocol

### Core Principle
When information sources conflict, authority is not equal.
This hierarchy determines what wins—every time.

---

### Authority Hierarchy
PRODUCTION REALITY (truth_sources/)
↓ overrides

HARD CONSTRAINTS (constraints/)
↓ overrides

FAILURE PATTERNS (failure_modes/)
↓ overrides

DECISION FRAMEWORKS (engineering_decisions/)
↓ overrides

BEST PRACTICES (key_guidelines/)
↓ overrides

REFERENCE IMPLEMENTATIONS (golden_examples/)
↓ overrides

SYNTAX DOCUMENTATION (language references/)

text

---

### Conflict Resolution Rules

#### Rule 1: Production Reality Always Wins
IF golden_examples says "use pattern X"
AND truth_sources/postmortems shows "pattern X caused $10M outage"
THEN truth_sources wins. Do not use pattern X.

No exceptions.

text

#### Rule 2: Constraints Override Patterns
IF golden_examples shows "microservices pattern"
AND constraints/regulatory_constraints requires "monolith for compliance"
THEN constraints wins. Use monolith.

Regulatory compliance is not negotiable.

text

#### Rule 3: Failure Patterns Override Best Practices
IF key_guidelines recommends "optimize early"
AND failure_modes/premature_optimization documents "caused 6-month delay"
THEN failure_modes wins. Do not optimize early.

text

#### Rule 4: Production Incidents Override Decision Frameworks
IF engineering_decisions recommends "build over buy"
AND truth_sources/why_systems_died shows "build killed the company"
THEN truth_sources wins. Buy if available.

text

#### Rule 5: Multiple Conflicts → Escalate to Top
IF constraints says A
AND failure_modes says B
AND golden_examples says C
THEN:

Check truth_sources for reality validation

If truth_sources confirms A → use A

If truth_sources silent → constraints win (rank 2 > rank 6)

Document the conflict for future learning

text

---

### Auto-Escalation Triggers

| Situation | Action |
|-----------|--------|
| 3+ sources conflict | Flag for human review |
| Financial + security conflict | Both constraints injected, agent explains trade-off |
| truth_sources contradicts best practice | truth_sources wins, explanation required |
| No truth_sources available | Flag as "untested pattern," warning injected |

---

### Warning Injection Protocol

When a recommended pattern lacks truth_sources validation:
⚠️ UNTESTED PATTERN WARNING
This approach has not been validated against production incidents.
Proceed with caution. Consider adding findings to truth_sources/
after implementation.

text

---

### Why This Exists

Without explicit hierarchy:
- The LLM picks whatever sounds most confident
- Best practices that failed in production get repeated
- Junior-sounding answers win over senior judgment

With explicit hierarchy:
- Production reality is law
- Hard constraints are walls
- Everything else is subordinate

This is not opinion.
This is engineering discipline.