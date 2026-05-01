# Famous Engineering Failures

## Learning From Scars
Real engineering is learned from what broke, not what worked.

| Failure | Root Cause | Lesson |
|---------|-----------|--------|
| AWS us-east-1 Outage (2021) | Internal network congestion | No region is immune |
| Knight Capital (2012) | Deploy script left old code | Never deploy without testing |
| GitLab Database Incident (2017) | rm -rf on primary, no verified backup | Backups must be tested |
| Cloudbleed (2017) | Buffer overflow leaking memory | Memory safety matters |
| Boeing 737 MAX | Software override without training | Code can kill people |
| Therac-25 | Race condition in medical device | Formal verification for safety-critical |
| Mars Climate Orbiter | Unit conversion error (metric/imperial) | Type systems prevent disasters |
| Toyota Unintended Acceleration | Spaghetti code, no peer review | Code quality is safety-critical |
| Facebook 6-Hour Outage (2021) | BGP config change broke internal DNS | Kill switches need to work offline |

## Resources
| Resource | URL |
|----------|-----|
| The Morning Paper (Incident Reviews) | https://blog.acolyer.org/ |
| Dan Luu Incident Reviews | https://danluu.com/postmortem-lessons/ |
| K8s Failure Stories | https://k8s.af/ |
