# Distributed System Traps

## The Eight Fallacies
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

## Common Traps
| Trap | Reality |
|------|---------|
| Distributed transactions are easy | They are impossible at scale (see: CAP) |
| Time is consistent across systems | Clocks drift, NTP fails |
| Exactly-once delivery | At-most-once or at-least-once is reality |
| Services are independent | Failures cascade |
| You can test distributed behavior locally | You cannot |
| Adding nodes fixes everything | Coordination overhead kills scaling |

## Resources
| Resource | URL |
|----------|-----|
| Jepsen Analyses | https://jepsen.io/analyses |
| Distributed Systems Reading List | https://dancres.github.io/Pages/ |
