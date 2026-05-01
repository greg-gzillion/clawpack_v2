# Famous Engineering Failures

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
