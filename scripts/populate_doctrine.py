import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

files["OPERATING_RULES.md"] = """# Operating Rules - Non-Negotiable Behaviors

These rules define how the coding agent must behave. They are not suggestions.

## Complexity Rules
1. Never recommend complexity before proving simplicity fails.
2. Never suggest microservices by default. Start with a monolith.
3. Every abstraction must justify its existence. If unclear, delete it.
4. The best code is the code you don't write.

## Optimization Rules
5. Never optimize before measuring. Ever.
6. Never assume scalability requirements without specific numbers.
7. Performance work must be driven by production data, not intuition.

## Debugging Rules
8. Never solve symptoms before finding root cause.
9. Never trust logs without verifying the assumptions behind them.
10. Reproduce before you fix. Always.

## Architecture Rules
11. Never recommend architecture without understanding constraints.
12. Design for the scale you have, not the scale you dream of.
13. The simplest solution that meets requirements is the correct one.

## Safety Rules
14. Never deploy without a rollback plan.
15. Never ship without tests that prove correctness.
16. Never add dependencies casually. Each dependency is a liability.
17. Never trust user input. Never trust external services. Never trust your own code without verification.

## Refactoring Rules
18. Never rewrite when refactoring is safer.
19. One logical change per commit. Always.
20. Behavior-preserving refactors must not change any observable behavior.

## Review Rules
21. Every review must find at least one thing to improve, or you are not reviewing carefully.
22. "LGTM" is not a review.

## The Prime Directive
When in doubt, choose the option that is:
1. Simplest to understand
2. Easiest to debug
3. Safest to change
4. Cheapest to operate

In that order.
"""

files["retrieval_priority.md"] = """# Retrieval Priority

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
"""

files["failure_modes/failure_modes.md"] = """# Failure Modes - What Goes Wrong

Senior engineers recognize failure patterns faster than they invent solutions.

## Common Failure Modes
| Mode | Symptom | Prevention |
|------|---------|------------|
| Premature Optimization | Complex code, no perf data | Measure first |
| Abstraction Leaks | Implementation details escape interface | Design interfaces by usage |
| Overengineering | Solution bigger than problem | Start simple |
| Hidden Coupling | Change in A breaks distant B | Explicit dependencies |
| Configuration Drift | Dev/staging/prod diverge | Infrastructure as code |
| Observability Blindness | Cannot debug because no logs | Log everything important |
| Testing Theater | Tests pass but bugs escape | Test behavior, not implementation |
| Dependency Hell | Upgrading one thing breaks everything | Lock and audit dependencies |
| Accidental Complexity | Complexity from chosen tools, not problem | Choose boring technology |
| Distributed Monolith | Services that must deploy together | Loose coupling, independent deploy |
| Resume-Driven Development | Chosen because trendy, not needed | Solve real problems |
| Cargo Cult Architecture | Copying without understanding why | Understand before adopting |

## Resources
| Resource | URL |
|----------|-----|
| How Complex Systems Fail | https://how.complexsystems.fail/ |
| Fallacies of Distributed Computing | https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing |
| The Twelve-Factor App | https://12factor.net/ |
"""

files["failure_modes/premature_optimization/premature_optimization.md"] = """# Premature Optimization

"The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places and at the wrong times; blind ignorance is a better starting point than premature optimization." - Donald Knuth

## Signs
- Optimizing code without profiling
- Making code less readable for imagined performance gains
- Choosing complex architectures for hypothetical scale
- Adding caching layers before measuring database performance

## Prevention
- Profile before optimizing. Always.
- Set performance budgets with real numbers
- Optimize the bottleneck, not what you think is slow
- Write clear code first, optimize only where measured
"""

files["failure_modes/overengineering/overengineering.md"] = """# Overengineering

## Signs
- Building a framework when you need a function
- Designing for "future requirements" that never arrive
- Adding abstraction layers "just in case"
- Using microservices for a 3-person team
- Kubernetes for a static website

## The YAGNI Principle
You Ain't Gonna Need It.
Build what you need NOW.
Design so you CAN change later.
Do not build what you MIGHT need later.

## Resources
| Resource | URL |
|----------|-----|
| You Are Not Google (Blog) | https://blog.bradfieldcs.com/you-are-not-google-84912cf44afb |
| Choose Boring Technology | https://boringtechnology.club/ |
"""

files["failure_modes/abstraction_leaks/abstraction_leaks.md"] = """# Abstraction Leaks

"The law of leaky abstractions means that whenever somebody invents a new, code-generating-tool-wielding, higher-level abstraction, it will inevitably leak." - Joel Spolsky

## Common Leaks
| Abstraction | Leak |
|-------------|------|
| ORM | N+1 queries, lazy loading surprises |
| Cloud | Zone failures, network partitions |
| Microservices | Network latency, distributed transactions |
| Virtual DOM | Performance cliffs with large trees |
| Garbage Collection | Stop-the-world pauses |
| TCP | Packet loss, retransmission |
| Docker | Filesystem performance, resource isolation |

## Prevention
- Understand one layer below your abstraction
- Test with realistic conditions
- Have escape hatches to the lower level
- Monitor the abstraction boundary
"""

files["failure_modes/distributed_system_traps/distributed_system_traps.md"] = """# Distributed System Traps

## The Eight Fallacies
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

## Common Traps
| Trap | Reality |
|------|---------|
| Distributed transactions are easy | They are impossible at scale (see: CAP) |
| Time is consistent across systems | Clocks drift, NTP fails |
| Exactly-once delivery | At-most-once or at-least-once is reality |
| Services are independent | Failures cascade |
| You can test distributed behavior locally | You cannot |
| Adding nodes fixes everything | Coordination overhead kills scaling |

## Resources
| Resource | URL |
|----------|-----|
| Jepsen Analyses | https://jepsen.io/analyses |
| Distributed Systems Reading List | https://dancres.github.io/Pages/ |
"""

files["architecture/kill_decisions/kill_decisions.md"] = """# Kill Decisions - When NOT To Use Technology

Most agents over-prescribe complexity. This fixes that.

## When NOT to Use Microservices
- Team is fewer than 20 engineers
- No independent deployment needs
- Data is tightly coupled
- You don't have DevOps maturity
- Transaction boundaries span services
- You cannot afford operational complexity

## When NOT to Use Kubernetes
- Single application or few services
- No container experience
- Startup with limited resources
- Predictable, steady load
- You cannot afford a platform team
- Static site or simple web app

## When NOT to Use Event Sourcing
- Simple CRUD application
- No audit trail requirements
- Team unfamiliar with the pattern
- Performance requirements are moderate
- Query patterns are simple

## When NOT to Use CQRS
- Read and write models are the same
- No performance separation needed
- Simple domain logic
- Small team, small codebase

## When NOT to Use GraphQL
- Simple REST API suffices
- No complex nested queries
- Caching requirements are simple
- Team unfamiliar with GraphQL
- Mobile bandwidth is not constrained

## When NOT to Use Redis
- Data fits in PostgreSQL/MySQL
- No sub-millisecond latency requirements
- Cache invalidation is complex
- You cannot afford to lose data
- Simple key-value needs (use memcached)

## When NOT to Use NoSQL
- Data is relational
- ACID transactions are required
- Ad-hoc querying is needed
- Data integrity is critical
- You need joins

## The Prime Rule
Default to the simplest technology.
Only upgrade when the current solution proves insufficient with real data.
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")
