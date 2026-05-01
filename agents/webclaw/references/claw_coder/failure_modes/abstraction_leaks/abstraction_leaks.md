# Abstraction Leaks

"The law of leaky abstractions means that whenever somebody invents a new, code-generating-tool-wielding, higher-level abstraction, it will inevitably leak." - Joel Spolsky

## Common Leaks
| Abstraction | Leak |
|-------------|------|
| ORM | N+1 queries, lazy loading surprises |
| Cloud | Zone failures, network partitions |
| Microservices | Network latency, distributed transactions |
| Virtual DOM | Performance cliffs with large trees |
| Garbage Collection | Stop-the-world pauses |
| TCP | Packet loss, retransmission |
| Docker | Filesystem performance, resource isolation |

## Prevention
- Understand one layer below your abstraction
- Test with realistic conditions
- Have escape hatches to the lower level
- Monitor the abstraction boundary
