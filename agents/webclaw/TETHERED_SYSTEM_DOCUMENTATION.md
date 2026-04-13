# 🦞 CLAWpack Tether System - Complete Documentation

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [How Agents Communicate](#how-agents-communicate)
5. [Installation & Setup](#installation--setup)
6. [Using the System](#using-the-system)
7. [Agent Reference](#agent-reference)
8. [Shared Memory Database](#shared-memory-database)
9. [Cross-Agent Learning](#cross-agent-learning)
10. [Extending the System](#extending-the-system)
11. [Troubleshooting](#troubleshooting)
12. [API Reference](#api-reference)

---

## System Overview

CLAWpack is a **tethered multi-agent system** where specialized AI agents share knowledge through a common SQLite database. Each agent focuses on a specific domain (legal, medical, math, translation) but can learn from and query other agents' knowledge.

### Key Features
- **19 agents** with specialized capabilities
- **Shared memory** via SQLite database
- **Cross-agent search** - query any agent from any agent
- **Persistent knowledge** - agents remember across sessions
- **Zero external dependencies** - pure Python, no APIs required
- **Offline capable** - works completely offline

### Current Active Agents (7 with data)

| Agent | Domain | Knowledge Entries | Status |
|-------|--------|------------------|--------|
| AgentForLaw | Legal/Court | 36 | ✅ Active |
| MedicLaw | Medical/Health | 10 | ✅ Active |
| MathematicaClaw | Math/Calculations | 6 | ✅ Active |
| PolyClaw | Translations | 59 | ✅ Active |
| Unified | Cross-Agent Routing | 4 | ✅ Active |
| Memory | General Knowledge | 28 | ✅ Active |
| DocuClaw | Documents | 1 | ✅ Active |

**Total: 144 shared knowledge entries**

---

## Architecture

### System Diagram
┌─────────────────────────────────────────────────────────────────┐
│ CLAWpack System │
├─────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ AgentForLaw │ │ MedicLaw │ │ PolyClaw │ │
│ │ (Legal) │ │ (Medical) │ │(Translation) │ │
│ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ SHARED MEMORY (SQLite) │ │
│ │ ~/.claw_memory/shared_memory.db │ │
│ │ │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ Tables: │ │ │
│ │ │ • agentforlaw_knowledge (36 entries) │ │ │
│ │ │ • medical_knowledge (10 entries) │ │ │
│ │ │ • math_knowledge (6 entries) │ │ │
│ │ │ • translations (59 entries) │ │ │
│ │ │ • unified_knowledge (4 entries) │ │ │
│ │ │ • memories (28 entries) │ │ │
│ │ │ • documents (1 entry) │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ▲ ▲ ▲ │
│ │ │ │ │
│ ┌──────┴───────┐ ┌──────┴───────┐ ┌──────┴───────┐ │
│ │ Mathematica │ │ Unified │ │ DocuClaw │ │
│ │ Claw │ │ (Brain) │ │ (Documents) │ │
│ │ (Math) │ │ │ │ │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘

text

### Data Flow

1. **Write Flow**: Agent learns → Saves to shared memory → Other agents can read
2. **Read Flow**: User queries → Agent searches shared memory → Returns results
3. **Cross-Agent Flow**: Agent A queries → Searches ALL tables → Returns results from Agents B, C, D

---

## Core Components

### 1. Shared Memory Database

**Location**: `~/.claw_memory/shared_memory.db`

**Initialization** (in each agent):
```python
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
SHARED_DB.parent.mkdir(exist_ok=True)

def init_shared_memory():
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                 (id INTEGER PRIMARY KEY, 
                  query TEXT UNIQUE, 
                  response TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()
2. Agent Base Structure
Every agent follows this pattern:

python
class AgentName:
    def __init__(self):
        init_shared_memory()  # Ensure DB exists
        register_agent()      # Optional: register in agent_registry
    
    def save_knowledge(self, query, response):
        """Save to shared memory"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO agent_table VALUES (?, ?, ?)',
                  (query, response, datetime.now()))
        conn.commit()
    
    def search_knowledge(self, query):
        """Search shared memory"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('SELECT response FROM agent_table WHERE query LIKE ?', 
                  (f'%{query}%',))
        return c.fetchone()
    
    def cross_search(self, query):
        """Search ALL agent tables"""
        # See cross-agent search implementation below
        pass
3. Cross-Agent Search Implementation
The key to tethering - searching across all agents:

python
def cross_agent_search(query):
    """Search ALL agent tables in shared memory"""
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    results = []
    
    # Define search strategies for each agent
    searches = [
        ('agentforlaw_knowledge', 'query', 'response', '⚖️', 'Legal'),
        ('medical_knowledge', 'query', 'response', '🏥', 'Medical'),
        ('math_knowledge', 'query', 'response', '📐', 'Math'),
        ('translations', 'source_text', 'translated_text', '🌐', 'Translation'),
        ('unified_knowledge', 'query', 'response', '🧠', 'Unified'),
        ('memories', 'memory_text', 'memory_text', '💾', 'Memory'),
        ('documents', 'title', 'content', '📄', 'Documents')
    ]
    
    for table, q_col, r_col, icon, name in searches:
        try:
            c.execute(f"SELECT {q_col}, {r_col} FROM {table} 
                       WHERE LOWER({q_col}) LIKE ?", (f'%{query.lower()}%',))
            for row in c.fetchall():
                results.append({
                    'icon': icon,
                    'agent': name,
                    'query': row[0][:100],
                    'response': row[1][:400]
                })
        except:
            pass
    
    conn.close()
    return results
How Agents Communicate
Method 1: Direct Database Read/Write
All agents read and write to the same SQLite database:

python
# Agent A writes
save_to_shared_memory("Texas courts", "Texas has 254 counties...")

# Agent B reads (can be different agent, different time)
result = query_shared_memory("Texas courts")
Method 2: Cross-Agent Search Command
From any agent, search ALL agents:

text
/cross "flu symptoms"   # Finds MedicLaw data
/cross "hello"          # Finds PolyClaw translations
/cross "calculate"      # Finds MathematicaClaw math
Method 3: Agent Registry (for real-time communication)
python
# Register agent
c.execute('INSERT INTO agent_registry (agent_name, status, last_seen) 
           VALUES (?, "active", ?)', (agent_name, datetime.now()))

# Check which agents are running
c.execute('SELECT agent_name FROM agent_registry WHERE status = "active"')
Method 4: Message Bus (async communication)
python
# Send message
c.execute('INSERT INTO agent_messages (from_agent, to_agent, message) 
           VALUES (?, ?, ?)', (from_agent, to_agent, message))

# Read messages
c.execute('SELECT message FROM agent_messages WHERE to_agent = ? AND read = 0', 
          (agent_name,))
Installation & Setup
Prerequisites
Python 3.8+

No external dependencies (uses only standard library)

Quick Start
bash
# 1. Clone the repository
git clone https://github.com/greg-gzillion/clawpack.git
cd clawpack

# 2. Run an agent
python agents/agentforlaw/agentforlaw.py

# 3. In another terminal, run another agent
python agents/mediclaw/mediclaw.py

# 4. Use cross-search from any agent
# In AgentForLaw: /cross "symptoms"
Directory Structure
text
clawpack/
├── agents/
│   ├── agentforlaw/          # Legal/court agent
│   │   ├── agentforlaw.py    # Main agent file
│   │   └── library/          # Local knowledge cache
│   ├── mediclaw/             # Medical agent
│   ├── polyclaw/             # Translation agent
│   ├── mathematicaclaw/      # Math agent
│   ├── unified/              # Orchestration agent
│   └── webclaw/              # Web reference agent
│       └── references/       # Static knowledge base
│           └── agentforlaw/
│               └── jurisdictions/  # Court data
│                   ├── TX/         # Texas courts
│                   ├── CA/         # California courts
│                   └── federal/    # Federal courts
├── check_memory.py           # Shared memory inspection tool
├── search_memory.py          # Cross-agent search utility
├── demo_cross_agent.py       # Demonstration script
└── master_launcher.py        # Launch multiple agents
Using the System
Basic Commands (AgentForLaw)
text
# Court Information
/court TX                    # Texas state courts overview
/court TX/Dallas            # Dallas County courts
/court TX/Harris            # Harris County courts
/court CA                    # California courts
/court NY                    # New York courts

# Federal Courts
/federal 5th                 # 5th Circuit Court of Appeals
/federal 9th                 # 9th Circuit

# Cross-Agent Search
/cross "flu symptoms"        # Search MedicLaw
/cross "hello"               # Search PolyClaw translations
/cross "calculate 5+3"       # Search MathematicaClaw
/cross "Texas court"         # Search AgentForLaw

# Statistics
/cross-stats                 # Show all agent statistics
/stats                       # Show local agent stats
Example Session
text
⚖️ AgentForLaw> /cross-stats

📊 CROSS-AGENT SHARED MEMORY STATISTICS
============================================================
  ⚖️ AgentForLaw: 36 entries
  🏥 MedicLaw: 10 entries
  📐 MathematicaClaw: 6 entries
  🌐 PolyClaw: 59 entries
  🧠 Unified: 4 entries
  💾 Memory: 28 entries
  📄 DocuClaw: 1 entries

📚 TOTAL: 144 knowledge entries shared across agents

⚖️ AgentForLaw> /cross symptoms

🔍 CROSS-AGENT SEARCH: 'symptoms'
============================================================

✅ Found 7 results across agents:

🏥 MedicLaw
   Q: what are the symptoms of flu
   A: ### Symptoms of the Flu (Influenza)
   The flu is a contagious respiratory illness...

🏥 MedicLaw
   Q: What are the symptoms of the common cold?
   A: ### Symptoms of the Common Cold...

🌐 PolyClaw
   Q: hello → hola

⚖️ AgentForLaw> /court TX/Dallas

🏛️ TX/Dallas
--------------------------------------------------
# Dallas County, TX

## County Court
- Phone: (214) 653-6000
- Address: 600 Commerce Street, Dallas, TX 75202

## District Court
- Jurisdiction: Felonies, Civil cases over $200,000
...
Utility Scripts
bash
# Check shared memory contents
python check_memory.py

# Search across all agents from command line
python search_memory.py "flu symptoms"
python search_memory.py "hello"

# Run demonstration
python demo_cross_agent.py

# Launch multiple agents (Windows)
launch_all_agents.bat

# Launch master controller
python master_launcher.py --start-all
Agent Reference
AgentForLaw (⚖️)
Purpose: Legal research, court information, case law

Capabilities:

50 state court systems

254 Texas counties with complete court data

Federal circuit courts

County-level court information (District, County, Family, Juvenile, Probate)

Commands:

CommandDescriptionExample
/court [state]State court overview/court TX
/court [state]/[county]Specific county courts/court TX/Dallas
/federal [circuit]Federal circuit info/federal 5th
/cross [query]Search all agents/cross "symptoms"
/cross-statsShow statistics/cross-stats
Data Source: agents/webclaw/references/agentforlaw/jurisdictions/

MedicLaw (🏥)
Purpose: Medical information, symptoms, treatments

Knowledge Examples:

Flu symptoms and treatment

Common cold symptoms

Headache causes

Dehydration signs

Burn treatment

Sprained ankle care

PolyClaw (🌐)
Purpose: Language translation

Supported Languages:

Spanish, French, German, Italian

Japanese, Chinese, Korean

Russian

Examples:

hello → hola, salut, hallo, ciao

goodbye → arrivederci, adiós, au revoir

MathematicaClaw (📐)
Purpose: Mathematical calculations

Capabilities: Basic arithmetic, equations

Unified (🧠)
Purpose: Cross-agent routing, orchestration

Function: Routes queries to appropriate specialized agents

Shared Memory Database
Schema Details
sql
-- AgentForLaw knowledge
CREATE TABLE agentforlaw_knowledge (
    id INTEGER PRIMARY KEY,
    query TEXT UNIQUE,
    response TEXT,
    category TEXT,
    jurisdiction TEXT,
    timestamp TEXT,
    source_agent TEXT,
    usage_count INTEGER DEFAULT 1
);

-- Medical knowledge
CREATE TABLE medical_knowledge (
    id INTEGER PRIMARY KEY,
    query TEXT UNIQUE,
    response TEXT,
    category TEXT,
    timestamp TEXT,
    source_agent TEXT
);

-- Translations
CREATE TABLE translations (
    id INTEGER PRIMARY KEY,
    source_text TEXT,
    translated_text TEXT,
    source_lang TEXT,
    target_lang TEXT,
    timestamp TEXT
);

-- Math knowledge
CREATE TABLE math_knowledge (
    id INTEGER PRIMARY KEY,
    query TEXT UNIQUE,
    response TEXT,
    timestamp TEXT
);

-- Agent registry (for active agents)
CREATE TABLE agent_registry (
    agent_name TEXT PRIMARY KEY,
    status TEXT,
    last_seen TEXT,
    capabilities TEXT,
    pid INTEGER
);

-- Message bus (inter-agent communication)
CREATE TABLE agent_messages (
    id INTEGER PRIMARY KEY,
    from_agent TEXT,
    to_agent TEXT,
    message TEXT,
    timestamp TEXT,
    read INTEGER DEFAULT 0
);
Querying the Database Directly
python
import sqlite3
from pathlib import Path

db = Path.home() / ".claw_memory" / "shared_memory.db"
conn = sqlite3.connect(str(db))
c = conn.cursor()

# Get all medical knowledge
c.execute("SELECT query, response FROM medical_knowledge")
for row in c.fetchall():
    print(f"Q: {row[0]}")
    print(f"A: {row[1][:200]}...")

# Get translation count
c.execute("SELECT COUNT(*) FROM translations")
print(f"Translations: {c.fetchone()[0]}")
Cross-Agent Learning
How Learning Works
Agent learns something new

python
save_to_shared_memory("What is a motion?", "A motion is a procedural request...")
Knowledge saved to agent's table

sql
INSERT INTO agentforlaw_knowledge VALUES (...)
Other agent queries for it

python
result = search_all_agents("motion")
Result returned regardless of source agent

text
⚖️ AgentForLaw: What is a motion? → A motion is a procedural request...
Learning Across Domains
If you query...Agent that knows...
"flu symptoms"MedicLaw
"hello in Spanish"PolyClaw
"calculate 5*7"MathematicaClaw
"Texas courts"AgentForLaw
Adding New Knowledge
python
# From any agent, you can add to shared memory
conn = sqlite3.connect(str(SHARED_DB))
c = conn.cursor()
c.execute('INSERT OR REPLACE INTO medical_knowledge (query, response, timestamp)
           VALUES (?, ?, ?)',
          ("What is telemedicine?", "Telemedicine is remote healthcare...", 
           datetime.now().isoformat()))
conn.commit()
Extending the System
Adding a New Agent
Create agent directory:

bash
mkdir agents/mynewagent
cd agents/mynewagent
Create agent file (mynewagent.py):

python
#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from datetime import datetime

SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

class MyNewAgent:
    def __init__(self):
        self.init_shared_memory()
        self.name = "mynewagent"
    
    def init_shared_memory(self):
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS myagent_knowledge
                     (id INTEGER PRIMARY KEY,
                      query TEXT UNIQUE,
                      response TEXT,
                      timestamp TEXT)''')
        conn.commit()
        conn.close()
    
    def save_knowledge(self, query, response):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO myagent_knowledge (query, response, timestamp)
                   VALUES (?, ?, ?)',
                  (query, response, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def cross_search(self, query):
        # Search ALL agents including this one
        results = []
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        # Search this agent's table
        c.execute("SELECT query, response FROM myagent_knowledge 
                   WHERE query LIKE ?", (f'%{query}%',))
        for row in c.fetchall():
            results.append(('🤖', 'MyNewAgent', row[0], row[1]))
        
        # Search other agents' tables
        # (add other tables as needed)
        
        conn.close()
        return results
    
    def run(self):
        print(f"🤖 {self.name} running...")
        while True:
            cmd = input(f"\n{self.name}> ").strip()
            if cmd == "/quit":
                break
            elif cmd.startswith("/cross "):
                results = self.cross_search(cmd[7:])
                for r in results:
                    print(f"{r[0]} {r[1]}: {r[2]} → {r[3][:200]}")
            # Add more commands as needed

if __name__ == "__main__":
    agent = MyNewAgent()
    agent.run()
Add to cross-search (in other agents):

python
# Add to tables_to_search in cross_agent_search()
('myagent_knowledge', 'query', 'response', '🤖', 'MyNewAgent')
Adding New Data
Adding a new state's court data:

bash
# Create state directory
mkdir agents/webclaw/references/agentforlaw/jurisdictions/CA/state

# Create court files
echo "# California Supreme Court" > CA/state/supreme_court.md
echo "# California Court of Appeals" > CA/state/court_of_appeals.md

# Create county directories
mkdir CA/Los_Angeles
mkdir CA/San_Francisco
Adding medical knowledge:

python
# In MedicLaw
save_to_medical_knowledge("What is diabetes?", 
    "Diabetes is a chronic condition affecting blood sugar...")
Troubleshooting
Common Issues and Solutions
IssueLikely CauseSolution
/cross returns no resultsWrong table/column namesCheck actual table schema with check_memory.py
Agents not sharing memoryDifferent database pathsEnsure all agents use same SHARED_DB path
Database lockedMultiple writes simultaneouslySQLite handles this; retry on failure
Court data not foundPath issueVerify WEBCLAW_REFS path is correct
Diagnostic Commands
bash
# Check shared memory exists and has data
python check_memory.py

# Test cross-agent search from command line
python search_memory.py "test query"

# View database directly
sqlite3 ~/.claw_memory/shared_memory.db
.tables
SELECT COUNT(*) FROM medical_knowledge;
Resetting Shared Memory
bash
# Backup existing database
cp ~/.claw_memory/shared_memory.db ~/.claw_memory/shared_memory.db.backup

# Remove and recreate (agents will recreate on next run)
rm ~/.claw_memory/shared_memory.db
API Reference
Shared Memory Functions
python
def save_to_shared_memory(table, query, response, **metadata):
    """Save knowledge to shared memory"""
    
def query_shared_memory(table, query):
    """Query specific agent's knowledge"""
    
def cross_agent_search(query, limit=10):
    """Search all agent tables"""
    
def get_agent_stats():
    """Get statistics for all agents"""
    
def register_active_agent(agent_name, capabilities):
    """Register agent in agent_registry table"""
Agent Template
python
class BaseAgent:
    def __init__(self, name, table_name, icon):
        self.name = name
        self.table = table_name
        self.icon = icon
        self.init_db()
    
    def init_db(self):
        """Initialize shared memory tables"""
        
    def save(self, query, response):
        """Save to this agent's table"""
        
    def search_local(self, query):
        """Search only this agent's table"""
        
    def search_cross(self, query):
        """Search all agents' tables"""
        
    def run_interactive(self):
        """Main command loop"""
Summary
CLAWpack is a tethered multi-agent system where:

Each agent specializes in a domain (legal, medical, math, translation)

All agents share a common SQLite database at ~/.claw_memory/shared_memory.db

Cross-agent search (/cross) queries all agents' knowledge

Knowledge persists across sessions and agents

No internet required - works completely offline

Key Files for Understanding
FilePurpose
agents/agentforlaw/agentforlaw.pyMain legal agent with cross-search
check_memory.pyInspect shared database contents
search_memory.pyCommand-line cross-agent search
demo_cross_agent.pyDemonstration of cross-agent learning
Quick Commands Reference
text
/cross "query"     - Search all agents
/cross-stats       - Show all agent statistics
/court TX/County   - Get Texas county court info
/court CA          - Get California courts
License & Contributing
This system is open source. To contribute:

Fork the repository

Create a feature branch

Add your agent or knowledge

Submit a pull request

Documentation generated: April 2026
*CLAWpack Version: 1.0 - Tethered Multi-Agent System*
