# Why Systems Died

## Startups That Failed From Engineering Mistakes
| Company | What Happened | Lesson |
|---------|---------------|--------|
| Friendster | Couldn't scale, pages took 30 seconds | Performance kills social networks |
| Pets.com | Built infrastructure for scale that never came | Don't scale before demand |
| Juicero | Overengineered hardware, simple problem | Solve the actual problem |
| Quibi | Built for mobile-only, ignored user behavior | Technology doesn't force behavior |

## Rewrites That Failed
| Company | What Happened | Lesson |
|---------|---------------|--------|
| Netscape | 3-year rewrite while Microsoft shipped | Never stop shipping |
| Healthcare.gov | Big bang launch, no incremental testing | Launch gradually |
| Knight Capital | Deploy script left old code on 1 of 8 servers | Automate everything or nothing |

## Migrations That Failed
| Company | Migration | Lesson |
|---------|-----------|--------|
| Hershey ERP | ERP migration during Halloween season | Never migrate during peak demand |
| TSB Bank | 1.9M customers locked out for weeks | Test migration at scale before cutover |
| UK Post Office (Horizon) | Blamed sub-postmasters for software bugs | Trust your error logs, not assumptions |

## Common Death Patterns
1. Scaling before product-market fit
2. Rewriting instead of refactoring
3. Big bang migrations with no rollback
4. Building for imaginary users
5. Blaming humans for systematic failures
6. Optimizing the wrong thing
