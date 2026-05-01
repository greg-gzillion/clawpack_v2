import os
base = r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\claw_coder"
files = {}

files["truth_sources/postmortems/postmortems.md"] = """# Postmortems - Learning From Production

## Why Postmortems Matter
Postmortems are the highest-value engineering documents.
They tell you what actually happened, not what should have happened.

## Essential Postmortems
| Incident | Company | Key Lesson |
|----------|---------|------------|
| GitLab Database Outage (2017) | GitLab | Test your backups |
| AWS us-east-1 (2021) | Amazon | No region is safe |
| Cloudflare DNS Outage (2020) | Cloudflare | Configuration is code |
| Facebook Global Outage (2021) | Meta | Kill switches must work offline |
| Roblox 73-Hour Outage (2021) | Roblox | Single points of failure |
| Fastly CDN Outage (2021) | Fastly | One customer broke the internet |
| Google Cloud Outage (2022) | Google | Automation can amplify failure |
| Slack Outage (2022) | Slack | Dependency chains fail hard |
| Okta Breach (2022) | Okta | Supply chain is your attack surface |
| CrowdStrike Global Outage (2024) | CrowdStrike | Kernel-level updates need staged rollout |

## Postmortem Template
1. What happened? (timeline)
2. What was the impact? (users, revenue, data)
3. How did we detect it? (or why didn't we?)
4. What was the root cause?
5. How did we fix it?
6. How do we prevent this class of failure?
7. What systems failed that should have caught this?

## Resources
| Resource | URL |
|----------|-----|
| Google SRE Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ |
| PagerDuty Postmortem Guide | https://postmortems.pagerduty.com/ |
| Incident Review (Dan Luu) | https://danluu.com/postmortem-lessons/ |
"""

files["truth_sources/why_systems_died/why_systems_died.md"] = """# Why Systems Died

## Startups That Failed From Engineering Mistakes
| Company | What Happened | Lesson |
|---------|---------------|--------|
| Friendster | Couldn't scale, pages took 30 seconds | Performance kills social networks |
| Pets.com | Built infrastructure for scale that never came | Don't scale before demand |
| Juicero | Overengineered hardware, simple problem | Solve the actual problem |
| Quibi | Built for mobile-only, ignored user behavior | Technology doesn't force behavior |

## Rewrites That Failed
| Company | What Happened | Lesson |
|---------|---------------|--------|
| Netscape | 3-year rewrite while Microsoft shipped | Never stop shipping |
| Healthcare.gov | Big bang launch, no incremental testing | Launch gradually |
| Knight Capital | Deploy script left old code on 1 of 8 servers | Automate everything or nothing |

## Migrations That Failed
| Company | Migration | Lesson |
|---------|-----------|--------|
| Hershey ERP | ERP migration during Halloween season | Never migrate during peak demand |
| TSB Bank | 1.9M customers locked out for weeks | Test migration at scale before cutover |
| UK Post Office (Horizon) | Blamed sub-postmasters for software bugs | Trust your error logs, not assumptions |

## Common Death Patterns
1. Scaling before product-market fit
2. Rewriting instead of refactoring
3. Big bang migrations with no rollback
4. Building for imaginary users
5. Blaming humans for systematic failures
6. Optimizing the wrong thing
"""

files["truth_sources/famous_failures/famous_failures.md"] = """# Famous Engineering Failures

## Software Killed People
| System | What Happened | Root Cause |
|--------|---------------|------------|
| Therac-25 | Radiation machine killed patients | Race condition, no hardware interlocks |
| Boeing 737 MAX | 346 people died | Software override pilots couldn't disable |
| Toyota UA | Unintended acceleration deaths | Spaghetti code, no peer review |
| Patriot Missile | Failed to intercept Scud, 28 soldiers killed | Floating point precision error over time |

## Financial Disasters
| System | Loss | Root Cause |
|--------|------|------------|
| Knight Capital | $440M in 45 minutes | Deploy script error, no kill switch |
| Flash Crash 2010 | $1T temporary loss | Algorithmic trading feedback loop |
| Mt. Gox | 850K Bitcoin lost | No version control, no testing |
| Societe Generale | $7.2B loss | Single trader, no position limits enforced |

## Infrastructure Collapses
| System | Impact | Root Cause |
|--------|--------|------------|
| AWS S3 Outage (2017) | Half the internet down | Typo in maintenance command |
| Cloudflare Leak (2017) | Memory leak exposed customer data | Buffer overflow in HTML parser |
| Dyn DNS Attack (2016) | Twitter, Reddit, Netflix down | Mirai botnet DDoS on single provider |

## The Lesson
These were not "bug" failures.
These were systematic engineering failures.
Every single one was preventable with:
- Better design
- Better testing
- Better review
- Better assumptions
"""

files["truth_sources/scaling_failures/scaling_failures.md"] = """# Scaling Failures

## When Scaling Went Wrong
| Company | Mistake | Result |
|---------|---------|--------|
| Twitter (Fail Whale) | Ruby monolith couldn't handle growth | Years of emergency rewrites |
| Tumblr | MySQL couldn't handle dashboard complexity | 4-day outage during migration |
| Reddit | Single database for everything | Daily crashes, years to fix |
| Pinterest | Python/Django couldn't serve feeds | Moved to Java microservices |
| Etsy | Bare metal servers, manual deploys | Couldn't scale during peak shopping |

## Common Scaling Mistakes
1. Adding cache before fixing queries
2. Sharding too early (adds complexity)
3. Scaling the wrong layer
4. Not measuring before optimizing
5. Premature microservices
6. No load testing before launches
7. Assuming cloud means infinite scale

## Resources
| Resource | URL |
|----------|-----|
| K8s Failure Stories | https://k8s.af/ |
| High Scalability (Real Stories) | http://highscalability.com/ |
"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print(f"\nDone! Created {len(files)} files.")
