# Scaling Failures

## When Scaling Went Wrong
| Company | Mistake | Result |
|---------|---------|--------|
| Twitter (Fail Whale) | Ruby monolith couldn't handle growth | Years of emergency rewrites |
| Tumblr | MySQL couldn't handle dashboard complexity | 4-day outage during migration |
| Reddit | Single database for everything | Daily crashes, years to fix |
| Pinterest | Python/Django couldn't serve feeds | Moved to Java microservices |
| Etsy | Bare metal servers, manual deploys | Couldn't scale during peak shopping |

## Common Scaling Mistakes
1. Adding cache before fixing queries
2. Sharding too early (adds complexity)
3. Scaling the wrong layer
4. Not measuring before optimizing
5. Premature microservices
6. No load testing before launches
7. Assuming cloud means infinite scale

## Resources
| Resource | URL |
|----------|-----|
| K8s Failure Stories | https://k8s.af/ |
| High Scalability (Real Stories) | http://highscalability.com/ |
