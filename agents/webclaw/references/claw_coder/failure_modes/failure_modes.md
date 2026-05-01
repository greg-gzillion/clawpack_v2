# Failure Modes - What Goes Wrong

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
