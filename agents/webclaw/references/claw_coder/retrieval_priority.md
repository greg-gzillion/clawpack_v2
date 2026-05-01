# Retrieval Priority

When answering a question, the agent must search references in this order:

## Priority 1 - Governance (Always First)
1. SYSTEM_OVERVIEW - How should I think about this?
2. OPERATING_RULES - Am I allowed to recommend this?
3. REFERENCE_RANKING - Which sources should I trust?

## Priority 2 - Structural Reasoning
4. architecture/ - What structure serves this problem?
5. debugging/ - What could go wrong and how to fix it?
6. engineering_decisions/ - What tradeoffs matter?
7. code_review/ - What not to do?

## Priority 3 - Context
8. constraints/ - What constraints apply?
9. decision_logs/ - How did others solve this?
10. failure_modes/ - What are the common traps?

## Priority 4 - Implementation
11. cs_fundamentals/ - What theory applies?
12. mental_models/ - How to decompose this problem?
13. [specific language or technology directory]

## Priority 5 - Examples
14. golden_examples/ - What does excellent look like?
15. ai_ml/ - AI-specific knowledge if relevant

## The Rule
Never answer from implementation details before establishing context.
Python syntax is useless if the architecture is wrong.
