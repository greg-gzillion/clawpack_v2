# Clawpack V2 - Decisions Log

## 2026-04-10: Webclaw as Single Source
**Decision:** All references go in `webclaw/references/`
**Why:** Prevents duplication across agents
**Alternative considered:** Each agent having its own references

## 2026-04-09: Routes Folder
**Decision:** Created `routes/` with one file per agent
**Why:** Makes clawpack.py clean and modular

## 2026-04-08: Fork Agents
**Decision:** Implemented fork agents for parallel execution
**Why:** Cache sharing = 90% cost savings
