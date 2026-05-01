# RETRIEVAL_BUDGET_POLICY.md
## Token Budget Allocation for Reference Injection

### Core Principle
Better retrieval ≠ more retrieval.
Better retrieval = better selection under constraint.

---

### Budget Limits

| Task Classification | Max References | Buffer for Context | Total Token Cap |
|---------------------|---------------|---------------------|-----------------|
| Standard (single domain) | 5 | 1,500 tokens | ~8,000 |
| Complex (2-3 domains) | 7 | 2,000 tokens | ~12,000 |
| Architecture (system design) | 8 | 2,500 tokens | ~15,000 |
| Critical (financial/security) | 10 | 3,000 tokens | ~18,000 |

---

### Priority Injection Order (Highest → Lowest)

| Rank | Category | Drops Last | Rationale |
|------|----------|------------|-----------|
| 1 | constraints/ | ✅ | Hard boundaries prevent catastrophe |
| 2 | truth_sources/ | ✅ | Reality overrides all theory |
| 3 | failure_modes/ | ✅ | Prevention > cure |
| 4 | engineering_decisions/ | If budget tight | Judgment over syntax |
| 5 | debugging/ | If budget tight | Only when failure patterns active |
| 6 | key_guidelines/ | If budget tight | Standards over opinion |
| 7 | golden_examples/ | If budget tight | Patterns over raw docs |
| 8 | code_review/ | Drops first | Context-dependent |
| 9 | domain syntax | Always included | Baseline, minimal tokens |

---

### Dropping Rules

When budget exceeded, drop from bottom (rank 9) upward.

Never drop:
- Rank 1-3 (constraints, truth_sources, failure_modes)
- Mandatory always-retrieve files (OPERATING_RULES, REFERENCE_RANKING, SYSTEM_OVERVIEW)

If budget still exceeded after dropping all droppable:
→ Expand to next budget tier
→ If max tier exceeded, split into multi-turn retrieval

---

### Multi-Turn Retrieval Strategy

If task requires 15+ references:
1. First turn: Inject ranks 1-3 + context
2. Second turn: Inject ranks 4-6 based on first response
3. Third turn: Inject ranks 7-9 for refinement

This prevents prompt bloat while maintaining depth.