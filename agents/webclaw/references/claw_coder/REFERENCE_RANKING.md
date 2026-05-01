# Reference Ranking System

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
