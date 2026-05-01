import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

# === SYSTEM OVERVIEW ===
files["SYSTEM_OVERVIEW.md"] = """# ClawCoder - Engineering Reasoning Engine

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
"""

# === ARCHITECTURE ===
files["architecture/system_design/system_design.md"] = """# System Design

## Core Resources
| Resource | URL |
|----------|-----|
| System Design Primer (GitHub) | https://github.com/donnemartin/system-design-primer |
| ByteByteGo System Design | https://bytebytego.com/ |
| Designing Data-Intensive Applications | https://dataintensive.net/ |
| System Design Interview | https://www.educative.io/courses/grokking-the-system-design-interview |
| High Scalability Blog | http://highscalability.com/ |

## Key Concepts
| Concept | URL |
|---------|-----|
| CAP Theorem Explained | https://www.infoq.com/articles/cap-twelve-years-later/ |
| Load Balancing Strategies | https://www.nginx.com/resources/glossary/load-balancing/ |
| Caching Patterns | https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/Strategies.html |
| Database Sharding | https://www.mongodb.com/docs/manual/sharding/ |
| Rate Limiting | https://stripe.com/blog/rate-limiters |
"""

files["architecture/design_patterns/design_patterns.md"] = """# Design Patterns

| Resource | URL |
|----------|-----|
| Refactoring Guru | https://refactoring.guru/design-patterns |
| Gang of Four Patterns | https://www.oodesign.com/ |
| Head First Design Patterns | https://www.oreilly.com/library/view/head-first-design/0596007124/ |
| Enterprise Integration Patterns | https://www.enterpriseintegrationpatterns.com/ |
| Cloud Design Patterns (Microsoft) | https://learn.microsoft.com/en-us/azure/architecture/patterns/ |
"""

files["architecture/distributed_systems/distributed_systems.md"] = """# Distributed Systems

| Resource | URL |
|----------|-----|
| MIT 6.824 Distributed Systems | https://pdos.csail.mit.edu/6.824/ |
| Distributed Systems Reading List | https://dancres.github.io/Pages/ |
| Jepsen (Distributed Systems Testing) | https://jepsen.io/ |
| Raft Consensus Algorithm | https://raft.github.io/ |
| Kafka: A Distributed Messaging System | https://kafka.apache.org/documentation/#design |
"""

files["architecture/api_design/api_design.md"] = """# API Design

| Resource | URL |
|----------|-----|
| REST API Design Guide | https://restfulapi.net/ |
| Microsoft REST API Guidelines | https://github.com/microsoft/api-guidelines |
| Google API Design Guide | https://cloud.google.com/apis/design |
| Stripe API Design | https://stripe.com/docs/api |
| JSON:API Specification | https://jsonapi.org/ |
| GraphQL Best Practices | https://graphql.org/learn/best-practices/ |
"""

# === DEBUGGING ===
files["debugging/root_cause_analysis/root_cause_analysis.md"] = """# Root Cause Analysis

## The Five Whys Method
1. Why did the system fail? (symptom)
2. Why did that happen? (direct cause)
3. Why was that possible? (process failure)
4. Why wasn't it caught? (detection gap)
5. Why did the system allow this? (architectural root)

## RCA Resources
| Resource | URL |
|----------|-----|
| Google SRE - Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ |
| Incident Analysis (J. Allspaw) | https://www.adaptivecapacitylabs.com/blog/ |
| How Complex Systems Fail | https://how.complexsystems.fail/ |
| The Infinite Hows | https://www.oreilly.com/radar/the-infinite-hows/ |
"""

files["debugging/debugging_frameworks/debugging_frameworks.md"] = """# Debugging Frameworks

| Resource | URL |
|----------|-----|
| How to Debug (John Regehr) | https://blog.regehr.org/archives/199 |
| Debugging: The 9 Indispensable Rules | https://www.goodreads.com/book/show/368235.Debugging |
| Rubber Duck Debugging | https://rubberduckdebugging.com/ |
| The Scientific Method of Debugging | https://www.cs.cornell.edu/courses/cs312/2006fa/lectures/lec26.html |
"""

files["debugging/performance_bottlenecks/performance_bottlenecks.md"] = """# Performance Bottlenecks

| Resource | URL |
|----------|-----|
| Brendan Gregg - Linux Performance | https://www.brendangregg.com/linuxperf.html |
| Systems Performance Book | https://www.brendangregg.com/systems-performance-2nd-edition-book.html |
| USE Method (Utilization Saturation Errors) | https://www.brendangregg.com/usemethod.html |
| Flame Graphs | https://www.brendangregg.com/flamegraphs.html |
"""

# === CODE REVIEW ===
files["code_review/anti_patterns/anti_patterns.md"] = """# Code Anti-Patterns

| Anti-Pattern | Description |
|--------------|-------------|
| God Object | Single class doing everything |
| Spaghetti Code | No structure, tangled logic |
| Golden Hammer | Using favorite tool for everything |
| Premature Optimization | Optimizing without measuring |
| Cargo Cult Programming | Copying without understanding |
| Magic Numbers | Unexplained constants |
| Boolean Blindness | Functions returning bool without context |
| Null Checks Everywhere | Instead of proper error handling |

| Resource | URL |
|----------|-----|
| Anti-Patterns Catalog | https://wiki.c2.com/?AntiPatternsCatalog |
| Refactoring Guru - Code Smells | https://refactoring.guru/refactoring/smells |
"""

files["code_review/senior_engineer_reviews/senior_engineer_reviews.md"] = """# Senior Engineer Review Standards

## Review Checklist
- Does this solve the right problem?
- Is the design the simplest possible?
- Will I understand this in 6 months?
- What is the failure mode?
- Is there a test that proves correctness?
- Could this be deleted or simplified?
- Does this introduce coupling?
- Is the naming clear and consistent?

## Resources
| Resource | URL |
|----------|-----|
| Google Code Review Guide | https://google.github.io/eng-practices/review/ |
| How to Do Code Reviews (Palantir) | https://blog.palantir.com/code-review-best-practices-19e02780015f |
| The Code Review Pyramid | https://www.morling.dev/blog/the-code-review-pyramid/ |
"""

# === ENGINEERING DECISIONS ===
files["engineering_decisions/decision_frameworks/decision_frameworks.md"] = """# Engineering Decision Frameworks

## The Decision Matrix
For any engineering decision:
1. What problem are we solving?
2. What are the constraints? (time, money, skill, scale)
3. What are the options?
4. What is the simplest option that works?
5. What is the cost of being wrong?
6. Can we reverse this decision easily?

## Resources
| Resource | URL |
|----------|-----|
| Technical Decision Making (Martin Fowler) | https://martinfowler.com/articles/technical-decision-making.html |
| Architecture Decision Records | https://adr.github.io/ |
| The Build vs Buy Decision | https://blog.pragmaticengineer.com/build-vs-buy/ |
"""

files["engineering_decisions/tradeoff_analysis/tradeoff_analysis.md"] = """# Tradeoff Analysis

## Common Tradeoffs
| Dimension | Option A | Option B |
|-----------|----------|----------|
| Consistency | Strong (CP) | Eventual (AP) |
| Performance | Throughput | Latency |
| Simplicity | Monolith | Microservices |
| Storage | Normalized | Denormalized |
| Communication | Sync (REST) | Async (Events) |
| Deployment | Big Bang | Incremental |
| Testing | Unit Heavy | Integration Heavy |

## Resources
| Resource | URL |
|----------|-----|
| CAP Theorem 20 Years Later | https://www.infoq.com/articles/cap-twelve-years-later/ |
| The Architecture of Open Source | https://aosabook.org/ |
"""

# === MENTAL MODELS ===
files["mental_models/problem_decomposition/problem_decomposition.md"] = """# Problem Decomposition

## The Decomposition Method
1. State the problem in one sentence
2. List all constraints
3. Break into independent sub-problems
4. Solve the hardest sub-problem first
5. Integrate solutions
6. Verify end-to-end

## Resources
| Resource | URL |
|----------|-----|
| How to Solve It (Polya) | https://math.berkeley.edu/~gmelvin/polya.pdf |
| First Principles Thinking | https://fs.blog/first-principles/ |
| The Engineering Method | https://www.goodreads.com/book/show/358641.The_Engineering_Method |
"""

files["mental_models/abstraction/abstraction.md"] = """# Abstraction in Engineering

## The Abstraction Hierarchy
| Level | Question |
|-------|----------|
| Problem | What does the user need? |
| Architecture | What components solve this? |
| Interface | How do components communicate? |
| Implementation | How does each component work? |
| Data | What state exists and where? |
| Infrastructure | What runs this? |

Good abstractions:
- Hide irrelevant detail
- Amplify essential complexity
- Are consistent at their level
- Have clear boundaries

## Resources
| Resource | URL |
|----------|-----|
| The Law of Leaky Abstractions | https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/ |
| Out of the Tar Pit | https://github.com/papers-we-love/papers-we-love/blob/main/design/out-of-the-tar-pit.pdf |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")
