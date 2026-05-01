import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

files["debugging/production_incidents/production_incidents.md"] = """# Production Incidents

## The Real Work of Engineering
Most engineering is fixing things that should not be broken.

## Incident Response Framework
1. DETECT - How did you find out?
2. TRIAGE - Is this a SEV? What is blast radius?
3. MITIGATE - Stop the bleeding first, find root cause later
4. RESOLVE - Fix the root cause
5. POSTMORTEM - What process allowed this?
6. PREVENT - System change, not just code fix

## Blameless Postmortems
- Focus on systems, not people
- Ask "how was this possible?" not "who did this?"
- Every incident is a learning opportunity
- The same class of incident should never happen twice

## Resources
| Resource | URL |
|----------|-----|
| Google SRE Book | https://sre.google/sre-book/table-of-contents/ |
| Incident Response Guide | https://response.pagerduty.com/ |
| Atlassian Incident Management | https://www.atlassian.com/incident-management |
| The PagerDuty Incident Response | https://response.pagerduty.com/training/course |
"""

files["code_review/before_after_refactors/before_after_refactors.md"] = """# Before/After Refactors

## What Makes a Great Refactor
- Smaller than the original
- More readable
- More testable
- Less coupled
- No behavior change
- One logical change per commit

## Refactor Patterns
| Smell | Before | After |
|-------|--------|-------|
| Long Method | 200-line function | 5 x 20-line functions |
| God Class | 1000-line class | 5 focused classes |
| Switch Statement | if/else chain | Polymorphism |
| Primitive Obsession | String phone number | PhoneNumber class |
| Feature Envy | Class A using Class B's data | Move method to B |

## Resources
| Resource | URL |
|----------|-----|
| Refactoring.com (Martin Fowler) | https://refactoring.com/ |
| Source Making Refactoring | https://sourcemaking.com/refactoring |
| Work Effectively with Legacy Code | https://www.goodreads.com/book/show/44919.Working_Effectively_with_Legacy_Code |
"""

files["engineering_decisions/build_vs_buy/build_vs_buy.md"] = """# Build vs Buy Decision Framework

## The Framework
| Question | Build | Buy |
|----------|-------|-----|
| Is this core to your business? | Yes | No |
| Do you have expertise? | Build | Buy |
| Is time to market critical? | Buy | Build |
| Is there an excellent OSS option? | Buy | Build |
| Will you need deep customization? | Build | Buy |
| Is maintenance cost high? | Maybe | Maybe |

## The Real Cost
Building: Development + maintenance + onboarding + documentation + debugging
Buying: License + integration + vendor lock-in + customization limits

## Resources
| Resource | URL |
|----------|-----|
| Build vs Buy Decision Guide | https://blog.pragmaticengineer.com/build-vs-buy/ |
| Make vs Buy in Software | https://martinfowler.com/articles/build-vs-buy.html |
"""

files["mental_models/failure_prediction/failure_prediction.md"] = """# Failure Prediction - Thinking Like an SRE

## Pre-Mortem Questions
Before deploying:
1. What is the worst thing that could happen?
2. What would cause that?
3. How would we detect it?
4. How would we recover?
5. What would the blast radius be?

## Common Failure Modes
| Pattern | Example | Prevention |
|---------|---------|------------|
| Cascading Failure | One service takes down others | Circuit breakers |
| Thundering Herd | All clients retry simultaneously | Jitter, exponential backoff |
| Slow Query | One slow request blocks pool | Timeouts, connection limits |
| Configuration Error | Wrong config value | Validation, gradual rollout |
| Dependency Hell | Upstream service fails | Graceful degradation |
| Resource Exhaustion | Memory leak, disk full | Monitoring, alerts, limits |
| Race Condition | Concurrent access | Proper locking, immutability |

## Resources
| Resource | URL |
|----------|-----|
| How Complex Systems Fail | https://how.complexsystems.fail/ |
| The Checklist Manifesto | https://www.goodreads.com/book/show/6667514-the-checklist-manifesto |
| Resilience Engineering | https://resiliencepapers.club/ |
"""

files["golden_examples/elite_open_source/elite_open_source.md"] = """# Elite Open Source Examples

## Code Worth Studying
| Project | Why |
|---------|-----|
| SQLite | Perfect C codebase, 100% branch coverage |
| Redis | Clean C, single-threaded clarity |
| CPython | Language implementation reference |
| Go Standard Library | Idiomatic, well-documented |
| Rust Standard Library | Zero-cost abstractions |
| Kubernetes | Distributed systems at scale |
| React | Component architecture |
| Linux Kernel | Systems programming |
| Nginx | High-performance networking |
| VSCode | Large TypeScript application |

## Study Method
1. Pick one file. Read it completely.
2. Understand the design decisions.
3. Note patterns you can use.
4. Apply one pattern to your own code.
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")
