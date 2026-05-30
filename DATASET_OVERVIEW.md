# Clawpack V2 — Jurisdictional Dataset Overview

## Coverage
- 50 states + District of Columbia
- 3,800+ cities with municipal data (courts, police, jails, hospitals, libraries, building permits)
- 13 tribal nations with court data
- 5 US territories
- 4,744 city-level building code entries
- Design resources for all 50 states (firms, schools, makers)

## Categories

| Category | Files |
|----------|-------|
| Building Codes | 4,744 |
| Courts | 15,000+ |
| Hospitals (with GPS) | 3,800+ |
| Police Departments | 3,800+ |
| Libraries | 3,800+ |
| Design Resources | 500+ |
| Tribal | 13 nations |

## Access Methods

### From any agent (via BaseAgent):
```python
hospitals = agent.lookup_jurisdiction("Denver CO", "hospital")
libraries = agent.lookup_jurisdiction("Miami FL", "library")
codes = agent.lookup_jurisdiction("Chicago IL", "building_codes")
From Chronicle FTS5:
python
results = agent.search_chronicle("Denver CO municipal court", limit=10)
Direct file access:
text
agents/webclaw/references/lawclaw/jurisdictions/us/{ST}/{County}/{City}/
Update Model
Community corrections via /correct command (3 confirmations = consensus)

Original data preserved with hash verification

Chronicle SQLite FTS5 index (448MB, 35,000+ interactions)

Searchable across county boundaries via full-text search

Version
Current: v3.1.0-data-license (May 29, 2026)
License: CC BY 4.0 (data) / MIT (code)
DOI: 10.5281/zenodo.19713157
