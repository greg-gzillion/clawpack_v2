# Postmortems - Learning From Production

## Why Postmortems Matter
Postmortems are the highest-value engineering documents.
They tell you what actually happened, not what should have happened.

## Essential Postmortems
| Incident | Company | Key Lesson |
|----------|---------|------------|
| GitLab Database Outage (2017) | GitLab | Test your backups |
| AWS us-east-1 (2021) | Amazon | No region is safe |
| Cloudflare DNS Outage (2020) | Cloudflare | Configuration is code |
| Facebook Global Outage (2021) | Meta | Kill switches must work offline |
| Roblox 73-Hour Outage (2021) | Roblox | Single points of failure |
| Fastly CDN Outage (2021) | Fastly | One customer broke the internet |
| Google Cloud Outage (2022) | Google | Automation can amplify failure |
| Slack Outage (2022) | Slack | Dependency chains fail hard |
| Okta Breach (2022) | Okta | Supply chain is your attack surface |
| CrowdStrike Global Outage (2024) | CrowdStrike | Kernel-level updates need staged rollout |

## Postmortem Template
1. What happened? (timeline)
2. What was the impact? (users, revenue, data)
3. How did we detect it? (or why didn't we?)
4. What was the root cause?
5. How did we fix it?
6. How do we prevent this class of failure?
7. What systems failed that should have caught this?

## Resources
| Resource | URL |
|----------|-----|
| Google SRE Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ |
| PagerDuty Postmortem Guide | https://postmortems.pagerduty.com/ |
| Incident Review (Dan Luu) | https://danluu.com/postmortem-lessons/ |
