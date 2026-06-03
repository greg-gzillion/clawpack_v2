# CLAWPACK V2 — Quick Start Guide

## Starting the System

### Terminal 1: A2A Server
```powershell
cd C:\Users\greg\dev\clawpack_v2
python a2a_server.py
Keep this running. Look for: 🌐 http://127.0.0.1:8766 and 📡 21 Agents Registered

Terminal 2: Clawpack Menu
powershell
cd C:\Users\greg\dev\clawpack_v2
python clawpack.py
Select agents by number (1-21), m to switch models, q to quit.

Testing Each Agent
1. LawClaw — Legal Research
text
/court Denver CO          → Courts, police, jails, hospitals, library, building permits
/ask legal question       → LLM-powered research with Chronicle context
/help                     → All commands
2. MedicLaw — Medical Analysis
text
/diagnose chest pain      → Differential diagnosis with red flags
/treatment hypertension   → Evidence-based guidelines
/medications metformin    → Pharmacology, dosing, interactions
/research hospitals in Denver CO  → Finds hospitals from jurisdiction data
/sources                  → Lists 91 medical specialties
3. MathematicaClaw — Math Engine
text
/derivative x^3 + 2*x^2 - 5*x + 7     → Step-by-step calculus
/integral sin(x) from 0 to pi          → Definite integrals
/limit (x^2-4)/(x-2) as x->2           → Limits with explanation
/solve x^2 + 3*x + 2 = 0               → Equation solving
4. LangClaw — Language Teacher
text
/lesson spanish           → Full language lesson with exercises
/vocab french             → Vocabulary practice
5. DocuClaw — Document Creation
text
/create letter Test content    → Creates formatted documents
/templates                     → Lists templates (business, education, personal, technical)
6. TXClaw — Blockchain
text
/networks                 → TX.org network endpoints
/search Coreum            → Blockchain reference search
7. WebClaw — Web Search
text
search Denver CO court    → Searches Chronicle + web with citations
fetch https://example.com → Fetches URL with verified citation
Switching Models
From the menu: press m
From llmclaw: /use MODEL_NAME
From any agent: exit to menu, select agent 21 (llmclaw)

Available: claude-haiku-4-5-20251001, gemma3:12b, qwen3-coder:30b, deepseek-r1:8b, + 13 more

Key Files
a2a_server.py — Central server (port 8766)

clawpack.py — Interactive menu

shared/CONSTITUTION_v1.md — Supreme law

data/chronicle.db — 76K indexed entries

.env — API keys

QUICKSTART.md — This file

SESSION_HANDOFF.md — What we built, current state

CHRONICLE_GUIDE.md — Data layer guide
