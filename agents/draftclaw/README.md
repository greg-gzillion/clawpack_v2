# DraftClaw v5 — Constitutional Technical Drawing Agent

Jurisdiction-aware building permits, structural packages, and blueprints. 
Powered by Chronicle database (4,744 jurisdiction entries across 50 states + territories).

## Commands

| Command | Description |
|---------|-------------|
| /lookup <city> | Search jurisdiction database, auto-open AHJ website |
| /structural <project> <location> | Conceptual structural package with real design criteria |
| /permit <project> <location> | Permit compliance package with jurisdiction codes |
| /blueprint <specs> | Dynamic PIL blueprint image + auto-save PNG |
| /correct <city> <field> <value> | Community edit (3 confirmations = consensus) |
| /cad <specs> | CAD/schematic with measurements (ASCII) |
| /circuit <design> | Circuit/wiring diagram with component specs |
| /specs <project> | Technical specifications with dimensions |
| /help | Show commands |

## Quick Start

/lookup phoenix
/structural warehouse 100x200 with 30ft clear height miami florida
/permit office building chicago
/blueprint warehouse 100x200 with loading docks and office
/correct Phoenix Phone (602) 555-1234

text

## Features

- **Chronicle-powered**: All 4,744 jurisdiction entries indexed in SQLite with FTS
- **Community editable**: /correct writes to chronicle, 3 confirmations = consensus
- **Constitutional**: Truth resolver, memory guard, no silent exceptions
- **Real design criteria**: Frost depth, snow load, wind speed, seismic from source data
- **Conceptual only**: No fabricated engineering values — marked [DESIGN REQUIRED]
- **Auto-browser**: Opens AHJ website on /lookup, /structural, /permit, /blueprint

## Data Flow
User Query → DraftClaw → Chronicle (SQLite) → Truth Resolver → LLM (Sovereign Gateway) → Output
