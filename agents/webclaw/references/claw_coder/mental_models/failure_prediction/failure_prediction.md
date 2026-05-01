# Failure Prediction - Thinking Like an SRE

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
