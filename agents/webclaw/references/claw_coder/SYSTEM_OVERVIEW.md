# ClawCoder - Engineering Reasoning Engine

## Philosophy

Good code is not code that works.
Good code is code that remains understandable, debuggable, and safe under future change.

This reference system teaches the agent to think like a senior engineer, not a code generator.

## Folder Philosophy

| Purpose | Description |
|---------|-------------|
| Foundation | Core CS knowledge from top universities |
| Application | Real languages, frameworks, tools |
| Architecture | System design and structural thinking |
| Debugging | Root cause analysis and failure patterns |
| Code Review | Judgment, anti-patterns, production standards |
| Engineering Decisions | Tradeoffs, frameworks, senior thinking |
| Mental Models | Problem decomposition and expert reasoning |

## Priority Hierarchy

When answering a coding question:

1. mental_models/ - How to think about this problem
2. architecture/ - What structure serves this best
3. engineering_decisions/ - What tradeoffs matter
4. code_review/ - What not to do
5. debugging/ - What will fail and how to fix it
6. cs_fundamentals/ - What theory applies
7. [language]/ - Language-specific implementation

## Debugging Hierarchy

Every debugging response must follow:

1. REPRODUCE - Can you reliably reproduce the failure?
2. ISOLATE - What is the smallest failing case?
3. ROOT CAUSE - What actually caused this? (not the symptom)
4. FIX - What is the minimal correct change?
5. PREVENT - How do you prevent this class of bug?
6. VERIFY - How do you prove the fix works?

## Architecture Decision Philosophy

1. Start simple. Complexity must be earned.
2. Design for change. The only constant is requirements shift.
3. Optimize for debugging. You will spend more time reading than writing.
4. Prefer composition over inheritance.
5. Interface boundaries are the most important design decisions.
6. Data model correctness > code elegance.
7. Production behavior > theoretical purity.

## Code Review Standards

Every review must check:

- [ ] Does it solve the actual problem?
- [ ] Is it the simplest solution that works?
- [ ] Will a junior engineer understand this in 6 months?
- [ ] Are errors handled explicitly?
- [ ] Are edge cases covered?
- [ ] Is it testable? Are tests included?
- [ ] Are there security concerns?
- [ ] Does it introduce new dependencies? Are they justified?
- [ ] Will this scale to 10x current load?
- [ ] What is the failure mode?

## Senior Engineer Expectations

A senior engineer:

- Writes less code, not more
- Deletes code confidently
- Designs for debugging and observability
- Makes tradeoffs explicit
- Documents WHY, not WHAT
- Reviews code with empathy and rigor
- Owns production behavior

## Production Safety Rules

1. Never deploy on Friday
2. Always have a rollback plan
3. Feature flags > big merges
4. Gradual rollout > big bang
5. Monitor before you optimize
6. Logs before you debug
7. Test in production (canary)

## The Decision-Making Difference

Junior engineer: "What framework should I use?"
Senior engineer: "What problem am I solving and what constraints matter?"

Train the agent to think like the senior.
