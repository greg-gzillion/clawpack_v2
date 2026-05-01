# Engineering Under Scale Constraints

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
