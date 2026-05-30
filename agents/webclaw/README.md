# WebClaw — Web Search & Chronicle Index

## What It Does
WebClaw is the information backbone of Clawpack V2. It fetches web content,
indexes it to the 448MB Chronicle SQLite database, and serves search results
to all 21 agents. Every jurisdiction file, medical reference, and legal document
flows through WebClaw.

## Commands

| Command | Description |
|---------|-------------|
| `search <query>` | Search the web with Chronicle enrichment + AI analysis |
| `fetch <url>` | Fetch and cite a specific URL |
| `/stats` | Agent statistics |
| `/delegate <agent> <task>` | Send task to any agent |

## Quick Start

search qualified immunity doctrine
fetch https://www.law.cornell.edu/wex/qualified_immunity

text

## Architecture
- **Chronicle**: 448MB SQLite FTS5 with 35,000+ indexed entries
- **References**: 3,800+ city jurisdiction files in `references/lawclaw/jurisdictions/us/`
- **Caching**: DataClaw search cache for 24hr result persistence
- **Constitutional**: 23-system boundary, 36 shared systems, circuit breaker protected
