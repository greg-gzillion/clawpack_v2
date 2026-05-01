import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

# === REFERENCE RANKING ===
files["REFERENCE_RANKING.md"] = """# Reference Ranking System

## Why Ranking Matters
Not all references are equal. The agent should trust and prioritize sources based on authority, accuracy, and depth.

## Tier S - Definitive Sources (Trust First)
These are the sources you bet your production system on.

| Source | Domain | Why |
|--------|--------|-----|
| Google SRE Book | Reliability | Production-tested at planetary scale |
| MIT 6.824 | Distributed Systems | Academic foundation of modern infra |
| Designing Data-Intensive Applications | Data Systems | The modern backend bible |
| CPython Source | Python | Ground truth implementation |
| Linux Kernel Documentation | Systems | How computers actually work |
| PostgreSQL Documentation | Databases | The best database documentation |
| SQLite Source Code | Embedded DB | Perfect C codebase, 100% tested |
| Redis Source | Caching/Data | Clean architecture, single-threaded |
| Rust Standard Library | Systems | Zero-cost abstractions |
| Go Standard Library | Systems | Idiomatic, well-documented |
| Nginx Documentation | Web Servers | High-performance serving |
| OCaml Compiler Source | Compilers | Functional programming excellence |

## Tier A - High Authority (Trust Highly)
Production engineering from companies that operate at scale.

| Source | Domain |
|--------|--------|
| Stripe Engineering Blog | Payments, API design |
| Cloudflare Engineering Blog | Networking, security, scale |
| Netflix Tech Blog | Microservices, chaos engineering |
| Uber Engineering Blog | Mobile, ML, data |
| Meta Engineering Blog | Infrastructure, AI |
| Microsoft Architecture Docs | Enterprise architecture |
| Amazon Builders Library | Distributed systems |
| Martin Fowler's Blog | Software architecture |
| Refactoring Guru | Design patterns, refactoring |
| Brendan Gregg's Blog | Performance, Linux |
| Julia Evans Zines | Systems, debugging |
| The Morning Paper (blog) | CS research summaries |

## Tier B - Good Quality (Use Selectively)
Solid resources with generally accurate information.

| Source | Domain |
|--------|--------|
| FreeCodeCamp | Tutorials, fundamentals |
| Real Python | Python tutorials |
| DigitalOcean Community | DevOps, infrastructure |
| CSS-Tricks | Frontend |
| Smashing Magazine | Web development |
| ArXiv (peer-reviewed) | Research papers |
| Google Engineering Practices | Code review, testing |
| Mozilla Developer Network | Web standards |
| Exercism | Language practice |
| LeetCode Discussion | Algorithm patterns |

## Tier C - Use With Caution
May contain errors, oversimplifications, or outdated information.

| Source | Issues |
|--------|--------|
| Medium (general) | Mixed quality, SEO content |
| Dev.to | Variable accuracy |
| YouTube tutorials | Often skip edge cases |
| Stack Overflow (unverified) | Check dates, upvotes |
| ChatGPT/LLM output | Requires verification |
| Random blog posts | No quality control |

## Tier D - Avoid
These sources are actively harmful to learning.

| Source | Why Avoid |
|--------|-----------|
| SEO content farms | Generated garbage |
| W3Schools (outdated parts) | Historically inaccurate |
| TutorialsPoint (some) | Often incorrect |
| Copy-paste tutorial sites | Never explain WHY |
| Rote memorization sites | No understanding |

## Ranking Algorithm
When synthesizing an answer:
1. Prioritize Tier S sources for core claims
2. Support with Tier A for practical context
3. Use Tier B for supplementary examples
4. Avoid Tier C unless Tier S/A unavailable
5. Never cite Tier D

## Trust Indicators
A source is more trustworthy when it:
- Cites specific production experience
- Explains WHY, not just HOW
- Acknowledges limitations and tradeoffs
- Is maintained and up-to-date
- Has clear authorship from practitioners
- Links to primary sources
"""

# === DECISION LOGS ===
files["decision_logs/architecture_case_studies/architecture_case_studies.md"] = """# Architecture Case Studies

## Why Architecture Decisions Matter
The best way to learn architecture is to study real decisions with real consequences.

## Case Studies
| System | Key Decision | Why It Matters |
|--------|-------------|----------------|
| Redis - Single Thread | Chose single-threaded event loop | Simplicity > parallelism for data structures |
| SQLite - Serverless | Embedded database, no server | No network, perfect reliability |
| PostgreSQL - MVCC | Multi-version concurrency control | Snapshot isolation, no read locks |
| Kubernetes - Declarative | Desired state, not commands | Self-healing, idempotent |
| Git - Content-Addressable | Everything is a hash | Integrity, distributed by design |
| HTTP - Stateless | No server state between requests | Infinite horizontal scaling |
| Unix - Everything is a File | Uniform interface | Composability, pipes |
| React - Virtual DOM | Diff virtual tree, patch real DOM | Declarative UI at scale |

## Resources
| Resource | URL |
|----------|-----|
| The Architecture of Open Source Applications | https://aosabook.org/ |
| High Scalability Blog | http://highscalability.com/ |
| Martin Fowler Architecture | https://martinfowler.com/architecture/ |
| InfoQ Architecture | https://www.infoq.com/architecture-design/ |
"""

files["decision_logs/famous_engineering_failures/famous_engineering_failures.md"] = """# Famous Engineering Failures

## Learning From Scars
Real engineering is learned from what broke, not what worked.

| Failure | Root Cause | Lesson |
|---------|-----------|--------|
| AWS us-east-1 Outage (2021) | Internal network congestion | No region is immune |
| Knight Capital (2012) | Deploy script left old code | Never deploy without testing |
| GitLab Database Incident (2017) | rm -rf on primary, no verified backup | Backups must be tested |
| Cloudbleed (2017) | Buffer overflow leaking memory | Memory safety matters |
| Boeing 737 MAX | Software override without training | Code can kill people |
| Therac-25 | Race condition in medical device | Formal verification for safety-critical |
| Mars Climate Orbiter | Unit conversion error (metric/imperial) | Type systems prevent disasters |
| Toyota Unintended Acceleration | Spaghetti code, no peer review | Code quality is safety-critical |
| Facebook 6-Hour Outage (2021) | BGP config change broke internal DNS | Kill switches need to work offline |

## Resources
| Resource | URL |
|----------|-----|
| The Morning Paper (Incident Reviews) | https://blog.acolyer.org/ |
| Dan Luu Incident Reviews | https://danluu.com/postmortem-lessons/ |
| K8s Failure Stories | https://k8s.af/ |
"""

files["decision_logs/scaling_stories/scaling_stories.md"] = """# Scaling Stories

## How Real Systems Scale
| Company | Problem | Solution |
|---------|---------|----------|
| Twitter | Fail Whale era | Gradual rewrite from Ruby to JVM |
| Amazon | Monolith to services | Two-pizza teams, SOA mandate |
| Netflix | DVD to streaming | Cloud migration, Chaos Monkey |
| Monzo | Banking at scale | Microservices from day one |
| WhatsApp | 50 engineers, 2B users | Erlang/OTP, minimal dependencies |
| Stack Overflow | High traffic, small team | Monolith + SQL Server, scale up not out |
| GitHub | Ruby monolith | Eventually migrated to Rails services |
| Shopify | Black Friday scale | Read replicas, CDN, aggressive caching |

## Common Scaling Patterns
1. Start simple, optimize when measured
2. Cache everything that is read-heavy
3. Queue everything that can be async
4. Denormalize reads, normalize writes
5. Feature flags > big bang deployments

## Resources
| Resource | URL |
|----------|-----|
| High Scalability | http://highscalability.com/ |
| InfoQ Case Studies | https://www.infoq.com/articles/ |
"""

# === CONSTRAINTS ===
files["constraints/high_scale/high_scale.md"] = """# Engineering Under Scale Constraints

## The Scale Constraint
When your system must serve millions of users:

| Principle | Why |
|-----------|-----|
| Stateless servers | Horizontal scaling |
| Async processing | Decouple request from work |
| Caching at every layer | Reduce database load |
| Denormalized reads | Fast queries |
| Partitioning/Sharding | Distribute data |
| Rate limiting | Protect downstream |
| Graceful degradation | Partial service > no service |

## Resources
| Resource | URL |
|----------|-----|
| Amazon Builders Library | https://aws.amazon.com/builders-library/ |
| Google SRE Book | https://sre.google/sre-book/table-of-contents/ |
"""

files["constraints/low_memory/low_memory.md"] = """# Engineering Under Memory Constraints

| Principle | Why |
|-----------|-----|
| Stream processing | Never load entire dataset |
| Lazy evaluation | Compute only when needed |
| Pool and reuse | Allocate once |
| Compact data structures | Enums, bitfields, packed |
| Memory-mapped files | OS handles paging |
| Reference counting | Deterministic cleanup |
| Avoid GC pressure | Pre-allocate, object pools |
"""

files["constraints/low_budget/low_budget.md"] = """# Engineering Under Budget Constraints

| Principle | Why |
|-----------|-----|
| Start with monolith | Cheaper to build and deploy |
| Use managed services | Reduce ops burden |
| Serverless for spiky workloads | Pay per use |
| Open source over commercial | No licensing costs |
| SQLite for small data | Zero ops cost |
| Single server until proven otherwise | Scale is expensive |
| Static site where possible | Free CDN hosting |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")
