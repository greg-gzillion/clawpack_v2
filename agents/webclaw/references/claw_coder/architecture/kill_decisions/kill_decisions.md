# Kill Decisions - When NOT To Use Technology

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
