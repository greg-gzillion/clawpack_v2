# Scaling Stories

## How Real Systems Scale
| Company | Problem | Solution |
|---------|---------|----------|
| Twitter | Fail Whale era | Gradual rewrite from Ruby to JVM |
| Amazon | Monolith to services | Two-pizza teams, SOA mandate |
| Netflix | DVD to streaming | Cloud migration, Chaos Monkey |
| Monzo | Banking at scale | Microservices from day one |
| WhatsApp | 50 engineers, 2B users | Erlang/OTP, minimal dependencies |
| Stack Overflow | High traffic, small team | Monolith + SQL Server, scale up not out |
| GitHub | Ruby monolith | Eventually migrated to Rails services |
| Shopify | Black Friday scale | Read replicas, CDN, aggressive caching |

## Common Scaling Patterns
1. Start simple, optimize when measured
2. Cache everything that is read-heavy
3. Queue everything that can be async
4. Denormalize reads, normalize writes
5. Feature flags > big bang deployments

## Resources
| Resource | URL |
|----------|-----|
| High Scalability | http://highscalability.com/ |
| InfoQ Case Studies | https://www.infoq.com/articles/ |
