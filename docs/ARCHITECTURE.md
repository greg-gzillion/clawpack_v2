# 🦞 CLAWPACK V2 - ARCHITECTURE REFERENCE
## What an AI Agent Needs to Know

**Generated:** '$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')'

---

## 🎯 SYSTEM OVERVIEW

Clawpack V2 is a modular AI agent ecosystem with:
- **21 specialized agents** communicating via A2A (port 8766)
- **17 LLM models** (local obliterated, standard, large CPU, cloud)
- **20,212 reference files** indexed in SQLite (280 MB, 1.5M terms)
- **Multi-provider LLM routing** (Groq → Ollama → OpenRouter)

**Location:** `C:\Users\greg\dev\clawpack_v2`

---

## 🏗️ KEY DIRECTORIES

| Directory | Purpose |
|-----------|---------|
| `agents/` | All 21 agents (each is self-contained) |
| `core/` | Core system modules (agent loader, LLM manager) |
| `shared/` | Shared utilities (base agent, A2A client, memory) |
| `models/` | LLM storage (obliterated + stock) |
| `docs/` | Documentation |
| `scripts/` | Utility scripts |
| `exports/` | Output files |

---

## 🤖 AGENTS (21 Total)

| Agent | Purpose | Handler | References |
|-------|---------|---------|------------|
| **llmclaw** | Model selection & multi-provider LLM | ✅ | - |
| **webclaw** | Knowledge base search | ✅ | 20,212 files |
| **lawclaw** | Legal research | ✅ | 16,827 files |
| **claw_coder** | Code generation (38 langs) | ✅ | 1,566 files |
| **mediclaw** | Medical references | ❌ | 1,421 files |
| **mathematicaclaw** | Math solver | ❌ | 17 files |
| **flowclaw** | Diagrams & flowcharts | ❌ | 20 files |
| **interpretclaw** | Translation | ❌ | 38 files |
| **langclaw** | Language teaching | ❌ | 259 files |
| **txclaw** | Blockchain | ❌ | 15 files |
| **docuclaw** | Document processing | ❌ | 21 files |
| **liberateclaw** | Model obliteration | ❌ | - |
| **dataclaw** | Data analysis | ❌ | - |
| **designclaw** | Graphic design | ❌ | - |
| **draftclaw** | Technical drawings | ❌ | - |
| **drawclaw** | Drawing/sketching | ❌ | - |
| **dreamclaw** | AI vision | ❌ | - |
| **plotclaw** | Charts/graphs | ❌ | - |
| **fileclaw** | File analysis | ❌ | - |
| **crustyclaw** | Rust assistant | ❌ | - |
| **rustypycraw** | Code crawler | ❌ | - |

**Agent Pattern:** Each agent has `agent_handler.py` for A2A, `commands/` for CLI, and inherits from `shared/base_agent.py`.

---

## 🧠 LLM MODELS (17 Working)

### Obliterated (No Refusals)
| Model | Size |
|-------|------|
| deepseek-coder-liberated | 3.8 GB |
| codellama-liberated | 3.8 GB |
| smollm2-liberated | 3.4 GB |
| tinyllama-liberated | 2.2 GB |
| gemma3-liberated | 815 MB |

### Standard Local
| Model | Size |
|-------|------|
| Qwen2.5-Coder GGUF | 4.7 GB |
| deepseek-coder:6.7b | 3.8 GB |
| codellama:7b | 3.8 GB |
| deepseek-r1:8b | 5.2 GB |
| gemma3:4b | 3.3 GB |
| gemma3:1b | 815 MB |
| tinyllama:1.1b | 637 MB |

### Large (CPU Offloaded)
| Model | Size |
|-------|------|
| gemma3:12b | 8.1 GB |
| gemma3:27b | 17 GB |
| qwen3-coder:30b | 18 GB |
| qwen3-vl:30b | 19 GB |

### Cloud
| Model | Provider |
|-------|----------|
| claude-3-haiku | Anthropic |

**Config:** `working_llms.json` | **Active:** `models/active_model.json`

---

## 📚 KNOWLEDGE BASE

**Index:** `agents/webclaw/cache/web_cache.db` (280 MB SQLite)

| Table | Rows |
|-------|------|
| web_cache | 20,211 |
| search_index | 1,484,984 |

**References by Category:**
| Category | Files |
|----------|-------|
| lawclaw | 16,827 |
| claw_coder | 1,566 |
| mediclaw | 1,421 |
| langclaw | 259 |
| interpretclaw | 38 |
| docuclaw | 21 |
| flowclaw | 20 |
| mathematicaclaw | 17 |
| txclaw | 15 |

---

## 🔗 A2A PROTOCOL

**Server:** `a2a_server.py` | **Port:** 8766 | **URL:** `http://127.0.0.1:8766`

### Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Server status |
| GET | `/v1/agents` | List all agents |
| GET | `/memory/stats` | Memory statistics |
| POST | `/v1/message/{agent}` | Send task to agent |

### Calling an Agent (Python)
```python
import requests
response = requests.post(
    "http://127.0.0.1:8766/v1/message/llmclaw",
    json={"task": "/llm Write hello world", "agent": "my_agent"},
    timeout=60
)
result = response.json()["result"]
Calling an Agent (PowerShell)
powershell
$body = @{task = "/llm Write hello world"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8766/v1/message/llmclaw" -Method POST -Body $body -ContentType "application/json"
🔧 KEY FILES
FilePurpose
a2a_server.pyMain A2A server
clawpack.pyCLI launcher
working_llms.jsonModel inventory
.envAPI keys (Groq, OpenRouter, Anthropic)
models/active_model.jsonCurrent LLM selection
agents/shared/base_agent.pyBase agent class
agents/shared/a2a_client.pyA2A client for agents
shared/llm/manager.pyMulti-provider LLM manager
🚀 QUICK START
Start A2A Server
bash
cd C:\Users\greg\dev\clawpack_v2
python a2a_server.py
Launch CLI
bash
python clawpack.py
Direct Agent Call
bash
cd agents/llmclaw
python llmclaw.py /llm "Write hello world in Python"
WebClaw Search
bash
curl -X POST http://127.0.0.1:8766/v1/message/webclaw -H "Content-Type: application/json" -d "{\"task\":\"search habeas corpus\"}"
📊 SYSTEM SUMMARY
ComponentCount
Agents21
LLM Models17
Reference Files20,212
Search Index Terms1,484,984
A2A Endpoints4
Total Storage~160 GB
This is everything an AI agent needs to know to work with Clawpack V2.
