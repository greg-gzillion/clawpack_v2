# Architecture Case Studies

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
