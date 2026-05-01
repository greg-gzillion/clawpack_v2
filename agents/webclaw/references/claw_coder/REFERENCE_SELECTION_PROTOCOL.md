# REFERENCE_SELECTION_PROTOCOL.md
## Deterministic Retrieval Routing

### Core Principle
Every task → explicit retrieval triggers → deterministic reference injection.
No heuristic guesswork. No "maybe retrieve this."

---

### Trigger → Retrieval Map

#### SCALE TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| scale, millions, throughput, concurrent | constraints/high_scale/ | failure_modes/distributed_system_traps/ |
| users, traffic, load | constraints/high_scale/ | truth_sources/scaling_failures/ |
| data volume, big data | constraints/high_scale/ | golden_examples/elite_open_source/ |

#### FINANCIAL TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| money, payment, financial, transaction | constraints/regulatory_constraints/ | truth_sources/postmortems/ |
| banking, trading, settlement | constraints/regulatory_constraints/ | engineering_decisions/tradeoff_analysis/ |
| audit, compliance | constraints/regulatory_constraints/ | truth_sources/why_systems_died/ |

#### DISTRIBUTED SYSTEMS TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| distributed, cluster, partition | architecture/distributed_systems/ | failure_modes/distributed_system_traps/ |
| consensus, replication, leader | architecture/distributed_systems/ | truth_sources/famous_failures/ |
| microservices, service mesh | architecture/design_patterns/ | failure_modes/overengineering/ |

#### PERFORMANCE TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| performance, latency, slow, bottleneck | debugging/performance_bottlenecks/ | golden_examples/excellent_backend/ |
| optimize, profiling, memory | debugging/performance_bottlenecks/ | failure_modes/premature_optimization/ |
| caching, indexing | performance/ | golden_examples/elite_open_source/ |

#### SECURITY TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| security, auth, authentication, authorization | cybersecurity/ | truth_sources/security_breaches/ |
| breach, vulnerability, exploit | cybersecurity/ | truth_sources/incident_reports/ |
| encryption, hashing, token | cybersecurity/ | key_guidelines/security_best_practices/ |

#### DATA TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| database, sql, query | databases/ | constraints/high_scale/ |
| migration, schema, alter | engineering_decisions/tradeoff_analysis/ | truth_sources/why_systems_died/ |
| backup, recovery, disaster | constraints/ | truth_sources/postmortems/ |

#### REFACTOR TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| refactor, rewrite, restructure | engineering_decisions/build_vs_buy/ | failure_modes/overengineering/ |
| migration, upgrade, legacy | engineering_decisions/maintainability/ | golden_examples/excellent_refactors/ |
| deprecate, remove, sunset | engineering_decisions/kill_decisions/ | truth_sources/famous_failures/ |

#### DECISION TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| decide, choose, pick, select | engineering_decisions/decision_frameworks/ | engineering_decisions/tradeoff_analysis/ |
| trade-off, pros/cons, versus | engineering_decisions/tradeoff_analysis/ | mental_models/constraints_reasoning/ |
| architecture, design, system design | architecture/system_design/ | decision_logs/architecture_case_studies/ |

#### DEBUGGING TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| debug, bug, error, crash, throw | debugging/ | failure_modes/ |
| log, trace, monitor, observe | debugging/log_analysis/ | truth_sources/production_incidents/ |
| root cause, why, investigate | debugging/root_cause_analysis/ | truth_sources/why_systems_died/ |

#### CODE QUALITY TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| clean, maintainable, readable | key_guidelines/clean_code/ | golden_examples/elite_open_source/ |
| pattern, anti-pattern, smell | code_review/anti_patterns/ | code_review/before_after_refactors/ |
| review, feedback, critique | code_review/senior_engineer_reviews/ | golden_examples/excellent_refactors/ |

#### TESTING TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| test, unit test, integration test | testing/ | key_guidelines/testing_guidelines/ |
| mock, stub, spy, fake | testing/ | golden_examples/elite_open_source/ |
| CI, continuous integration, pipeline | devops/ | key_guidelines/ |

#### API TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| API, endpoint, REST, GraphQL | architecture/api_design/ | key_guidelines/api_design/ |
| version, deprecate, breaking change | engineering_decisions/tradeoff_analysis/ | golden_examples/excellent_api_design/ |
| rate limit, throttle, quota | constraints/high_scale/ | engineering_decisions/ |

#### DEPLOYMENT TRIGGERS
| Trigger | Primary Retrieval | Secondary Retrieval |
|---------|-------------------|---------------------|
| deploy, release, ship, rollout | devops/ | truth_sources/incident_reports/ |
| rollback, revert, hotfix | engineering_decisions/kill_decisions/ | debugging/production_incidents/ |
| cloud, AWS, Azure, GCP | architecture/cloud/ | constraints/high_scale/ |

---

### Priority Rules

1. **Safety First**: If both `constraints/regulatory_constraints/` and any other reference are triggered, regulatory constraints are injected FIRST.
2. **Failure Before Success**: If `failure_modes/` is triggered, it is always injected before `golden_examples/`.
3. **Complexity Gating**: If triggers span 3+ domains, also retrieve `mental_models/problem_decomposition/`.
4. **Financial Gating**: Any financial trigger automatically adds `truth_sources/why_systems_died/` as mandatory retrieval.
5. **Novelty Gating**: If the task involves a technology not in the agent's training cutoff, `golden_examples/` for that technology is mandatory.

---

### Mandatory Always-Retrieve

These are injected into EVERY prompt regardless of triggers:

- `OPERATING_RULES.md`
- `REFERENCE_RANKING.md`
- `SYSTEM_OVERVIEW.md`

---

### Retrieval Weighting

| Category | Weight | Rationale |
|----------|--------|-----------|
| truth_sources/ | 5 (Critical) | Reality overrides theory |
| constraints/ | 5 (Critical) | Hard boundaries prevent catastrophic failure |
| failure_modes/ | 4 (High) | Prevention > cure |
| engineering_decisions/ | 4 (High) | Judgment over syntax |
| golden_examples/ | 3 (Medium) | Patterns over raw syntax |
| key_guidelines/ | 3 (Medium) | Standards over opinion |
| code_review/ | 2 (Low) | Context-dependent relevance |
| debugging/ | 2 (Low) | Only if failure patterns detected |
| language syntax | 1 (Baseline) | Always available, lowest priority |