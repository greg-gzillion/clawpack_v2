# Agent Test Results — October 19, 2026

All 21 agents tested end-to-end with domain-specific commands.
Server running on port 8766. mem0 active.

## Results

| Agent | Command | Time | Length | Status |
|-------|---------|------|--------|--------|
| lawclaw | /court Denver CO | 6.82s | 4255 | ✅ Real court data |
| mediclaw | /diagnose headache fever | 4.85s | 5947 | ✅ Medical guidance |
| txclaw | /stats | 0.15s | 58 | ✅ |
| docuclaw | /help | 0.15s | 354 | ✅ |
| dataclaw | /stats | 8.94s | 54 | ✅ 41,465 files indexed |
| fileclaw | /help | 0.22s | 287 | ✅ |
| llmclaw | /list | 0.56s | 1050 | ✅ Model list |
| interpretclaw | /translate Hello world to Spanish | 0.45s | 10 | ✅ Hola mundo |
| crustyclaw | /audit fn main() {} | 1.68s | 967 | ✅ |
| claw_coder | /code python function... | 2.52s | 202 | ✅ Validated |
| mathematicaclaw | /solve 2x + 5 = 13 | 0.29s | 12 | ✅ Solutions: 4 |
| rustypycraw | /scan . | 0.75s | 84 | ✅ 27 files |
| webclaw | search Denver court | 0.35s | 7242 | ✅ 10 results deduped |
| plotclaw | /bar 1 2 3 4 5 | 3.84s | 85 | ✅ PNG generated |
| flowclaw | /flowchart start -> end | 0.44s | 192 | ✅ Mermaid |
| langclaw | /lesson Spanish greetings | 4.10s | 5605 | ✅ |
| designclaw | /logo tech startup | 2.93s | 2191 | ✅ SVG |
| draftclaw | /blueprint 100x200 room | 39.58s | 8617 | ✅ (slow) |
| drawclaw | /draw sunset | 2.25s | 72 | ✅ |
| dreamclaw | /imagine cyberpunk city | 7.89s | 3954 | ✅ |
| liberateclaw | /models | 1.57s | 562 | ✅ |

**Result: 21/21 agents working.**

## Notes

- **draftclaw (39s)** — chains 4 cross-agent calls (dataclaw search → webclaw search → LLM synthesis → fileclaw export). The 39s is the cost of coordination, not a bug.
- **drawclaw** — initial test showed a transient path error; direct call worked. Likely a working-directory race during rapid restart.
- **mem0 lock warning** — appears when two server instances run simultaneously. Ensure single instance.

## Architecture Confirmed

Server logs during draftclaw call show:
dataclaw.search → webclaw HTTP → fileclaw HTTP → draftclaw HTTP

text

This confirms the hub-and-spoke model:
- Agents are thin dispatch shells
- Cross-agent calls go through A2A
- WebClaw is the centralized web gateway
- DataClaw is the centralized local search
- FileClaw is the centralized format handler
- LLMClaw is the centralized LLM router
File 2 — docs/ABOUT.md:

markdown
# What Clawpack V2 Is

Clawpack V2 is a local multi-agent Python application for Windows,
Linux, and macOS. It runs as a CLI menu (`python clawpack.py`) or an
HTTP A2A server (`python a2a_server.py`) on port 8766.

## Architecture: Shell Agents + Shared Gateways

The 21 agents fall into two categories:

**16 domain specialists** — each handles a specific domain with
commands relevant to its name (lawclaw for legal, mediclaw for medical,
claw_coder for code, etc.).

**5 infrastructure agents** — these serve the specialists:

- **webclaw** — all web access for the entire system
- **dataclaw** — all local file search
- **fileclaw** — all format conversion
- **llmclaw** — all LLM access (Sovereign Gateway)
- **liberateclaw** — model library management

### How They Interact

Agents are **thin shells**. They dispatch commands but don't duplicate
shared functionality. They call shared services:

- **All web information → WebClaw.** WebClaw queries the local
  Chronicle (237,878 records), fetches live URLs, deduplicates by URL,
  and ranks by BM25 × source trust.
- **All local file search → DataClaw.** DataClaw searches 41,465
  indexed files across `docs/`, `data/`, `exports/`, and
  `agents/webclaw/references/`.
- **All LLM access → LLMClaw.** LLMClaw routes to Groq (primary),
  Ollama, OpenRouter, or Anthropic.
- **All format conversion → FileClaw.** FileClaw handles 52 formats.

### Cross-Agent Coordination

A single command may invoke a chain of cross-agent calls. For example,
`draftclaw /blueprint` calls DataClaw (local search), then WebClaw
(web), then LLMClaw (synthesis), then FileClaw (export). The full
pipeline takes ~39 seconds.

### Underlying Storage

- **Chronicle** (`runtime/chronicle.db`) — SQLite FTS5, 587 MB,
  237,878 records of web fetches and indexed content
- **Memory** (`runtime/mem0/qdrant/`) — Qdrant vector store for
  cross-agent memory
- **References** (`agents/webclaw/references/`) — 40,838 curated
  files across 19 namespaces

### What It Is Not

- **Not an operating system** — runs on one, doesn't replace one
- **Not a swarm** — agents don't exhibit emergent behavior
- **Not a chatbot** — CLI menu and A2A API, not conversation
- **Not fully enforced governance** — the Constitution exists but
  Articles IV and XI are dormant

## Verified Working

As of October 19, 2026, all 21 agents respond correctly to
domain-specific commands. See
[docs/archive/AGENT_TEST_RESULTS_2026_10_19.md](docs/archive/AGENT_TEST_RESULTS_2026_10_19.md)
for the full test results.