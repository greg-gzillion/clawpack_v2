# CLAWPACK V2 — Chronicle Index Guide

## What is the Chronicle?

The Chronicle is the shared knowledge database for all 21 agents. It's a SQLite database with FTS5 full-text search, located at `data/chronicle.db` (448MB, ~76,463 entries).

## How Data Gets Into the Chronicle

### 1. Reference File Indexing
```powershell
python scripts/index_all_references.py
This scans ALL markdown files in agents/webclaw/references/ and indexes:

Full file content (no truncation)

File paths as URLs (reference://agent/category/...)

Metadata (agent name, file type, coordinates, URLs found in content)

2. Automatic Recording
Every time WebClaw fetches a URL, the content is recorded in Chronicle via chronicle.record_fetch().

3. Agent Learning
When agents call self.learn(), facts are stored in unified memory and indexed.

How Agents Search the Chronicle
Direct Search (from any agent)
python
# In any agent's handle() method:
results = self.search_chronicle("Denver CO hospital", limit=10)
FTS5 Full-Text Search
The Chronicle uses SQLite FTS5 for fast text search:

Supports boolean operators: word1 OR word2

Automatic keyword extraction on natural language queries

Falls back to LIKE search if FTS5 returns empty

Source Filtering
No filtering by default — all agents see all data (Constitution Article VI).

How to Rebuild the Index
powershell
# Purge and reindex all references
python scripts/index_all_references.py

# Check index status
python scripts/check_index.py
Database Structure
TablePurpose
chronicleMain entries: url, context, source, timestamp, metadata
chronicle_ftsFTS5 virtual table for full-text search
Key Files
FilePurpose
data/chronicle.dbThe SQLite database
agents/webclaw/core/chronicle_ledger.pyChronicle class — record_fetch, recover_by_context
shared/base_agent.pysearch_chronicle() — how agents query
scripts/index_all_references.pyRebuilds the index
scripts/check_index.pyShows index statistics
Data Flow
text
webclaw/references/*.md
        ↓
index_all_references.py
        ↓
chronicle.db (FTS5 indexed)
        ↓
BaseAgent.search_chronicle()
        ↓
Any of 21 agents
        ↓
LLM synthesis with citations
What's Indexed (76,463 entries)
lawclaw: 70+ legal categories + 50-state jurisdiction data (courts, police, jails, hospitals, libraries, building permits)

mediclaw: 91 medical specialties (diseases, medications, guidelines)

txclaw: 60+ tx.org blockchain documentation categories

claw_coder: 39 programming language references

designclaw, drawclaw, docuclaw, draftclaw: Design resources

All other agent references: Language, math, blockchain, etc.
