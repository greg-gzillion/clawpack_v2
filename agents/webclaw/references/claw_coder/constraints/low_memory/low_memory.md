# Engineering Under Memory Constraints

| Principle | Why |
|-----------|-----|
| Stream processing | Never load entire dataset |
| Lazy evaluation | Compute only when needed |
| Pool and reuse | Allocate once |
| Compact data structures | Enums, bitfields, packed |
| Memory-mapped files | OS handles paging |
| Reference counting | Deterministic cleanup |
| Avoid GC pressure | Pre-allocate, object pools |
