# CLAWPACK_V2 - COMPLETE SYSTEM DOCUMENTATION
## Every File, Every Function, Every Agent - NOTHING LEFT OUT

================================================================================
TABLE OF CONTENTS
================================================================================
1.  SYSTEM ARCHITECTURE OVERVIEW
2.  ROOT DIRECTORY - Every File Explained
3.  A2A SERVER - Complete Endpoint Documentation
4.  CORE MODULES - Every File & Function
5.  SHARED MODULES - Complete Breakdown
6.  MODELS - Stock vs Obliterated
7.  AGENTS - All 21 Agents, Every Command, Every File
    7.1  webclaw (Search & Index Engine)
    7.2  lawclaw (Legal Research)
    7.3  llmclaw (Model Manager)
    7.4  dataclaw (Data Management)
    7.5  flowclaw (Diagrams & Flowcharts)
    7.6  docuclaw (Document Generation)
    7.7  mathematicaclaw (Math & Visualization)
    7.8  claw_coder (38 Language Code Generation)
    7.9  liberateclaw (Model Liberation/Obliteration)
    7.10 mediclaw (Medical References)
    7.11 interpretclaw (Translation & Speech)
    7.12 langclaw (Language Learning)
    7.13 txclaw (Blockchain)
    7.14 dreamclaw (AI Vision)
    7.15 designclaw (Graphic Design)
    7.16 draftclaw (Technical Drawings)
    7.17 drawclaw (Drawing)
    7.18 fileclaw (File Analysis)
    7.19 plotclaw (Charts & Graphs)
    7.20 rustypycraw (Code Crawler)
    7.21 crustyclaw (Rust AI Assistant)
8.  CHRONICLE SYSTEM - Dataclaw & Webclaw Indexing
9.  MEMORY SYSTEM - Three-Tier Architecture
10. LLM INTEGRATION - API, Ollama, Obliterated
11. ROUTES - All API Endpoints
12. SCRIPTS & UTILITIES
13. TESTS
14. GIT STRUCTURE
15. TROUBLESHOOTING GUIDE
16. STARTUP SEQUENCE (EXACT ORDER)

================================================================================
1. SYSTEM ARCHITECTURE OVERVIEW
================================================================================

ClawPack V2 Architecture:
┌─────────────────────────────────────────────────────────────────────────────┐
│                           🦞 CLAWPACK_V2                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ENTRY POINTS:                                                              │
│  • a2a_server.py (Port 8766) - Agent-to-Agent communication hub             │
│  • clawpack.py - Interactive agent launcher with model selection            │
│  • claw.py - Legacy entry point                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYERS:                                                                    │
│  1. A2A Server (FastAPI-style HTTP server)                                  │
│  2. Agent Layer (21 specialized agents, each with commands/)                │
│  3. Shared Layer (LLM, Memory, Search, Hooks, Skills)                       │
│  4. Core Layer (State, Permissions, Validation, Error handling)             │
│  5. Models Layer (Stock symlinks + Obliterated full models)                 │
│  6. Data Layer (url_index.json, web_cache.db, data_index.db)                │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flow:
User → clawpack.py → Select Model (llmclaw) → Select Agent → 
Agent Command → A2A Server (8766) → WebClaw Search → LLM Generation → Response

================================================================================
2. ROOT DIRECTORY - EVERY FILE EXPLAINED
================================================================================

📄 .env (309 B)
   PURPOSE: Environment variables for API keys
   CONTENTS: OPENROUTER_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY
   USED BY: shared/llm/client.py, shared/llm/openrouter.py, shared/llm/anthropic.py

📄 .gitignore (583 B)
   PURPOSE: Git ignore patterns
   EXCLUDES: __pycache__, .venv, *.safetensors, models/obliterated/*

📄 a2a_server.py (8856 B)
   PURPOSE: Main A2A protocol server - THE HEART OF THE SYSTEM
   FUNCTIONS:
     • main() - Starts HTTP server on port 8766
     • handle_request() - Routes to /health, /v1/agents, /v1/message/{agent}
     • agent_discovery() - Scans agents/ folder, registers all agents
     • process_agent_task() - Routes task to specific agent's agent_handler.py
   ENDPOINTS:
     • GET  /health        - Server health + memory stats
     • GET  /v1/agents     - List all registered agents (21 total)
     • GET  /memory/stats  - Three-tier memory statistics
     • POST /v1/message/{agent} - Send task to specific agent
   MUST BE RUNNING BEFORE ANY AGENT IS USED

📄 a2a_server_backup.py (8442 B)
   PURPOSE: Backup of a2a_server.py before modifications
   STATUS: Redundant - can be deleted

📄 activate_features.py (2094 B)
   PURPOSE: Feature flag activation script
   FUNCTIONS: activate_feature(), list_features()

📄 claw.py (5545 B)
   PURPOSE: Legacy main entry point
   FUNCTIONS: main() - Original agent launcher (pre-llmclaw integration)
   STATUS: Partially deprecated - use clawpack.py instead

📄 clawpack.py (7807 B) - CURRENT MAIN ENTRY
   PURPOSE: Main interactive menu with model selection
   FUNCTIONS:
     • main() - Main loop
     • banner() - Display ClawPack ASCII art
     • show_agents() - Display 21 agents with descriptions
     • get_active_model_display() - Show current LLM model
     • launch_agent() - Execute agent's main .py file
     • launch_model_selector() - Open llmclaw interface
   FLOW: Model Select (m) → Agent Select (1-21) → Launch Agent

📄 clawpack_backup.py (16745 B)
   PURPOSE: Backup before llmclaw integration
   STATUS: Keep for reference

📄 LICENSE (1073 B)
   PURPOSE: MIT License

📄 README.md (14388 B)
   PURPOSE: Project documentation
   CONTENTS: Overview, installation, agent list, usage

📄 requirements.txt (492 B)
   PURPOSE: Python dependencies
   CONTENTS: requests, aiohttp, transformers, torch, ollama, etc.

📄 SECURITY.md (1310 B)
   PURPOSE: Security policy and reporting

📄 working_llms.json (1994 B)
   PURPOSE: Active LLM configuration registry
   FORMAT: [{"model": "name", "source": "ollama|openrouter|anthropic", "priority": 1}]
   MANAGED BY: agents/llmclaw/providers/stock.py and obliterated.py
   READ BY: shared/llm/manager.py

================================================================================
3. A2A SERVER - COMPLETE ENDPOINT DOCUMENTATION
================================================================================

File: a2a_server.py
Port: 8766
Protocol: HTTP/1.1 JSON

ENDPOINTS:

GET /health
  RESPONSE: {
    "status": "healthy",
    "agents_registered": 21,
    "memory": {
      "working_tokens": 0,
      "semantic_facts": 0,
      "messages_processed": 0
    }
  }

GET /v1/agents
  RESPONSE: {
    "agents": [
      "lawclaw", "webclaw", "flowclaw", "docuclaw", "mathematicaclaw",
      "liberateclaw", "txclaw", "interpretclaw", "langclaw", "claw_coder",
      "dataclaw", "fileclaw", "plotclaw", "mediclaw", "dreamclaw",
      "designclaw", "draftclaw", "drawclaw", "crustyclaw", "rustypycraw",
      "llmclaw"
    ]
  }

GET /memory/stats
  RESPONSE: {
    "working_memory": {"tokens": 0, "max": 8000},
    "semantic_memory": {"facts": 0},
    "episodic_memory": {"episodes": 0},
    "procedural_memory": {"procedures": 0}
  }

POST /v1/message/{agent}
  REQUEST: {"task": "/search denver", "agent": "lawclaw"}
  ROUTING: agent_handler.py → process_task() → returns result
  RESPONSE: {"status": "success", "agent": "webclaw", "result": "..."}

AGENT REGISTRATION:
  - Scans agents/ folder for directories containing agent_handler.py
  - Validates each agent has name/run pattern
  - Registers 21 agents at startup

================================================================================
4. CORE MODULES - EVERY FILE & FUNCTION
================================================================================

📁 core/
├── 📄 state.py (1490 B)
│   PURPOSE: Global state management
│   CLASSES: State - Singleton state container
│   PROPERTIES: model, provider, memory, config
│
├── 📄 config.py (8220 B) [in shared/]
│   PURPOSE: Configuration management
│   FUNCTIONS: load_config(), get_config(), save_config()
│
├── 📄 permissions.py (1956 B)
│   PURPOSE: Agent permission system
│   FUNCTIONS: check_permission(), grant_permission(), revoke_permission()
│
├── 📄 validation.py (6147 B)
│   PURPOSE: Input validation for all agents
│   FUNCTIONS: validate_command(), sanitize_input(), validate_path()
│
├── 📄 error_handler.py (9923 B)
│   PURPOSE: Centralized error handling
│   CLASSES: ClawpackError, AgentError, LLMError
│   FUNCTIONS: handle_error(), format_traceback()
│
├── 📄 logging.py (3790 B)
│   PURPOSE: Structured logging
│   FUNCTIONS: setup_logging(), log_agent_call(), log_llm_request()
│
├── 📄 metrics.py (7796 B)
│   PURPOSE: Performance metrics collection
│   FUNCTIONS: record_latency(), get_stats(), reset_metrics()
│
├── 📄 observability.py (4781 B)
│   PURPOSE: OpenTelemetry integration
│   FUNCTIONS: trace_agent(), trace_llm(), get_trace_context()
│
├── 📄 rate_limiter.py (4698 B)
│   PURPOSE: API rate limiting
│   CLASSES: RateLimiter
│   FUNCTIONS: check_limit(), wait_if_needed()
│
├── 📄 shutdown.py (6257 B)
│   PURPOSE: Graceful shutdown handling
│   FUNCTIONS: register_shutdown_handler(), cleanup()
│
├── 📄 security.py (4522 B)
│   PURPOSE: Security utilities
│   FUNCTIONS: hash_content(), verify_signature(), sanitize_path()
│
├── 📄 input_handler.py (3864 B)
│   PURPOSE: User input processing
│   FUNCTIONS: parse_command(), handle_interrupt()
│
├── 📄 output_handler.py (3505 B)
│   PURPOSE: Formatted output
│   FUNCTIONS: print_banner(), format_table(), colorize()
│
├── 📄 agent_router.py (2656 B)
│   PURPOSE: Route tasks to appropriate agent
│   FUNCTIONS: route_task(), get_agent_handler()
│
├── 📄 base_agent.py (5048 B)
│   PURPOSE: Base class for all agents
│   CLASSES: BaseAgent
│   METHODS: __init__(), register_command(), run_command(), get_help()
│
├── 📄 command_router.py (3377 B)
│   PURPOSE: Command parsing and routing
│   FUNCTIONS: parse(), route(), get_command_list()
│
├── 📄 query_loop.py (1442 B)
│   PURPOSE: Interactive query loop for agents
│   FUNCTIONS: start_loop(), process_input()
│
├── 📄 tool.py (2507 B)
│   PURPOSE: Tool registration system
│   CLASSES: Tool
│   FUNCTIONS: register_tool(), call_tool()
│
├── 📄 batcher.py (1993 B)
│   PURPOSE: Batch processing for LLM requests
│   FUNCTIONS: batch_requests(), process_batch()
│
├── 📄 compactor.py (4500 B)
│   PURPOSE: Memory compaction for long conversations
│   FUNCTIONS: compact_memory(), summarize_context()
│
├── 📄 latches.py (1565 B)
│   PURPOSE: Concurrency control latches
│   CLASSES: Latch, ReadWriteLatch
│
├── 📄 edit_tools.py (4969 B)
│   PURPOSE: File editing utilities
│   FUNCTIONS: edit_file(), apply_diff(), create_backup()
│
├── 📄 chronicle_helper.py (1826 B)
│   PURPOSE: Chronicle ledger integration
│   FUNCTIONS: record_event(), get_timeline()
│
├── 📄 math_engine.py (4995 B)
│   PURPOSE: Mathematical computation engine
│   FUNCTIONS: evaluate(), solve_equation(), plot_function()
│
├── 📄 agent_loader.py (2694 B)
│   PURPOSE: Dynamic agent loading
│   FUNCTIONS: load_agent(), discover_agents()
│
└── 📄 core (10 B)
    PURPOSE: Symlink to shared/core for compatibility

📁 core/llm/ - OBLITERATED MODEL STORAGE
├── 📁 obliterated/
│   ├── 📁 codellama_7b/ (12.55 GB) - Full obliterated CodeLlama
│   ├── 📁 deepseek_coder_6.7b/ (12.56 GB) - Obliterated DeepSeek
│   ├── 📁 phi2/ (5.18 GB) - Obliterated Phi-2
│   ├── 📁 qwen_coder_7b/ (14.19 GB) - Obliterated Qwen Coder
│   ├── 📁 smollm2_1.7b/ (3.19 GB) - Obliterated SmolLM2
│   └── 📁 tinyllama/ (2.05 GB) - Obliterated TinyLlama
├── 📄 batch_obliterate.ps1 (2212 B) - PowerShell batch obliteration script
├── 📄 monitor_progress.ps1 (3419 B) - Monitor obliteration progress
├── 📄 cache.py (1013 B) - Model cache management
├── 📄 config.py (1144 B) - Obliteration configuration
└── 📄 manager.py (2013 B) - Obliterated model manager

================================================================================
5. SHARED MODULES - COMPLETE BREAKDOWN
================================================================================

📁 shared/
├── 📁 llm/ - LLM INTEGRATION ENGINE
│   ├── 📄 __init__.py (329 B) - Exports LLMProvider, OllamaProvider, etc.
│   ├── 📄 client.py (9139 B)
│   │   CLASSES: LLMClient, LLMResponse
│   │   FUNCTIONS: get_llm(), call(), stream()
│   │   PROVIDERS: OpenRouter, Anthropic, OpenAI, Ollama (auto-detected)
│   │   FALLBACK: Tries providers in order until one succeeds
│   ├── 📄 manager.py (3155 B)
│   │   CLASSES: LLMManager
│   │   FUNCTIONS: load_working_llms(), get_best_for_task(), list_providers()
│   │   PRIORITY: Liberated models first, then standard, then API
│   ├── 📄 provider.py (413 B)
│   │   CLASSES: LLMProvider (abstract base class)
│   │   METHODS: call() - async method to be implemented
│   ├── 📄 ollama.py (970 B)
│   │   CLASSES: OllamaProvider
│   │   FUNCTIONS: is_available(), call()
│   │   ENDPOINT: http://localhost:11434/api/generate
│   ├── 📄 openrouter.py (1290 B)
│   │   CLASSES: OpenRouterProvider
│   │   FUNCTIONS: _load_key(), call()
│   │   ENDPOINT: https://openrouter.ai/api/v1/chat/completions
│   ├── 📄 anthropic.py (1323 B)
│   │   CLASSES: AnthropicProvider
│   │   FUNCTIONS: _load_key(), call()
│   │   ENDPOINT: https://api.anthropic.com/v1/messages
│   ├── 📄 webclaw.py (971 B)
│   │   CLASSES: WebclawProvider
│   │   FUNCTIONS: search() - searches references folder
│   ├── 📄 streaming.py (6895 B)
│   │   CLASSES: StreamingLLMClient, LLMCache
│   │   FUNCTIONS: stream(), _stream_openrouter(), _stream_anthropic()
│   │   CACHING: LRU cache with TTL
│   └── 📄 slot_reservation.py (1921 B)
│       CLASSES: SlotReservation
│       FUNCTIONS: on_truncation(), get_stats()
│       PATTERN: Claude Code Pattern #9 - 8K default, escalate to 64K
│
├── 📁 memory/ - THREE-TIER MEMORY SYSTEM
│   ├── 📄 __init__.py (299 B)
│   ├── 📄 three_tier.py (5406 B)
│   │   CLASSES: ThreeTierMemory
│   │   LAYERS:
│   │     • Working Memory (8K tokens) - Current conversation
│   │     • Semantic Memory - Facts and knowledge
│   │     • Episodic Memory - Past interactions
│   │   FUNCTIONS: add(), recall(), compact(), get_stats()
│   ├── 📄 procedural_memory.py (5359 B)
│   │   CLASSES: ProceduralMemory
│   │   FUNCTIONS: learn_procedure(), execute_procedure(), get_procedures()
│   └── 📄 trauma_guard.py (1873 B) [in agents/shared/safety/]
│       PURPOSE: Safety filter for LLM outputs
│       FUNCTIONS: check_safety(), filter_response()
│
├── 📁 search/ - BITMAP SEARCH ENGINE
│   └── 📄 __init__.py (3936 B)
│       CLASSES: BitmapIndex, FuzzyScorer, SearchResult
│       FUNCTIONS:
│         • BitmapIndex.__init__(index_name)
│         • BitmapIndex.add_batch(items) - Add multiple items
│         • BitmapIndex.build() - Build search index
│         • BitmapIndex.search(query, max_results) - Search and score
│         • BitmapIndex.get_stats() - Index statistics
│         • FuzzyScorer.score(a, b) - Fuzzy matching score
│         • FuzzyScorer.highlight_matches(text) - Highlight query matches
│       USED BY: agents/webclaw/providers/webclaw_provider.py
│
├── 📁 hooks/ - LIFECYCLE HOOK SYSTEM
│   ├── 📄 __init__.py (458 B)
│   ├── 📄 hook_manager.py (6213 B)
│   │   CLASSES: HookManager
│   │   FUNCTIONS: register(), trigger(), get_hooks()
│   ├── 📄 hook_matcher.py (1631 B)
│   │   FUNCTIONS: match_hook(), filter_hooks()
│   ├── 📄 hook_types.py (4468 B)
│   │   TYPES: PRE_COMMAND, POST_COMMAND, PRE_LLM, POST_LLM, ON_ERROR
│   └── 📁 runners/
│       ├── 📄 agent_runner.py (655 B) - Run agent hooks
│       ├── 📄 command_runner.py (3962 B) - Run command hooks
│       ├── 📄 http_runner.py (1904 B) - Run HTTP hooks
│       └── 📄 prompt_runner.py (1479 B) - Run prompt hooks
│
├── 📁 skills/ - AGENT SKILLS
│   └── 📄 __init__.py (5544 B)
│       CLASSES: Skill, SkillRegistry
│       FUNCTIONS: register_skill(), get_skill(), execute_skill()
│
├── 📄 router.py (870 B)
│   PURPOSE: Shared routing utilities
│   FUNCTIONS: route(), match_pattern()
│
├── 📄 agent_router.py (2656 B) [duplicate of core/agent_router.py?]
│
├── 📄 base_agent.py (5048 B) [duplicate of core/base_agent.py?]
│
├── 📄 config.py (8220 B)
│   PURPOSE: Shared configuration
│
├── 📄 permissions.py (8617 B)
│   PURPOSE: Extended permissions system
│
├── 📄 rate_limiter.py (4698 B)
│   PURPOSE: Shared rate limiting
│
├── 📄 security.py (4522 B)
│   PURPOSE: Shared security utilities
│
├── 📄 shutdown.py (6257 B)
│   PURPOSE: Shared shutdown handling
│
├── 📄 validation.py (6147 B)
│   PURPOSE: Shared validation
│
├── 📄 chronicle_helper.py (1826 B)
│   PURPOSE: Chronicle ledger helpers
│
├── 📄 commands.py (440 B)
│   PURPOSE: Shared command utilities
│
├── 📄 edit_tools.py (4969 B)
│   PURPOSE: Shared editing tools
│
├── 📄 batcher.py (1993 B)
│   PURPOSE: Shared batch processing
│
├── 📄 compactor.py (4500 B)
│   PURPOSE: Shared memory compaction
│
├── 📄 latches.py (1565 B)
│   PURPOSE: Shared concurrency latches
│
├── 📄 logging.py (3790 B)
│   PURPOSE: Shared logging
│
├── 📄 metrics.py (7796 B)
│   PURPOSE: Shared metrics
│
├── 📄 observability.py (4781 B)
│   PURPOSE: Shared observability
│
├── 📄 input_handler.py (3864 B)
│   PURPOSE: Shared input handling
│
├── 📄 output_handler.py (3505 B)
│   PURPOSE: Shared output handling
│
└── 📄 error_handler.py (9923 B)
    PURPOSE: Shared error handling

================================================================================
6. MODELS - STOCK VS OBLITERATED
================================================================================

📁 models/
├── 📄 active_model.json (47 B)
│   PURPOSE: Currently selected model
│   FORMAT: {"model": "gemma3:12b", "source": "stock"}
│   UPDATED BY: agents/llmclaw/providers/*.py
│   READ BY: All LLM queries
│
├── 📁 stock/ - NORMAL MODELS (Ollama symlinks)
│   ├── 📄 ollama_provider.py (1719 B) - Stock model provider
│   ├── 📄 ollama_registry.json (1311 B) - Cached Ollama model list
│   └── 📄 __init__.py (121 B)
│   NOTE: Symlinks to ~/.ollama/models should be here but are currently missing
│
└── 📁 obliterated/ - FULL OBLITERATED MODELS (local, uncensored)
    ├── 📁 codellama_7b/ (12.55 GB)
    │   ├── model-00001-of-00007.safetensors (1.89 GB)
    │   ├── model-00002-of-00007.safetensors (1.90 GB)
    │   ├── model-00003-of-00007.safetensors (1.90 GB)
    │   ├── model-00004-of-00007.safetensors (1.90 GB)
    │   ├── model-00005-of-00007.safetensors (1.84 GB)
    │   ├── model-00006-of-00007.safetensors (1.84 GB)
    │   ├── model-00007-of-00007.safetensors (1.58 GB)
    │   ├── model.safetensors.index.json
    │   ├── config.json
    │   ├── tokenizer.json (3.5 MB)
    │   ├── tokenizer_config.json
    │   ├── generation_config.json
    │   ├── chat_template.jinja
    │   └── abliteration_metadata.json
    ├── 📁 deepseek_coder_6.7b/ (12.56 GB) - Similar structure
    ├── 📁 phi2/ (5.18 GB) - Similar structure
    ├── 📁 qwen_coder_7b/ (14.19 GB) - Similar structure
    ├── 📁 smollm2_1.7b/ (3.19 GB) - Similar structure
    └── 📁 tinyllama/ (2.05 GB) - Similar structure

================================================================================
7. AGENTS - ALL 21 AGENTS, EVERY COMMAND, EVERY FILE
================================================================================

📁 agents/
├── 📁 shared/ - SHARED AGENT UTILITIES
│   ├── 📁 collaboration/
│   ├── 📁 importers/
│   │   └── 📄 unified_importer.py (10119 B) - Import from various formats
│   ├── 📁 memory/
│   │   ├── 📄 procedural_memory.py (5359 B)
│   │   └── 📄 three_tier.py (5406 B)
│   ├── 📁 safety/
│   │   └── 📄 trauma_guard.py (1873 B)
│   ├── 📄 a2a_client.py (2333 B) - A2A client for agents
│   ├── 📄 acp_client.py (2204 B) - Agent Control Protocol client
│   ├── 📄 agent_loader.py (1681 B)
│   ├── 📄 base_agent.py (1403 B)
│   ├── 📄 budget_controller.py (2843 B) - Token budget management
│   ├── 📄 decomposer.py (3351 B) - Task decomposition
│   ├── 📄 mcp_registry.py (4084 B) - Model Context Protocol registry
│   ├── 📄 router.py (3553 B)
│   └── 📄 sandbox.py (2381 B) - Code execution sandbox

================================================================================
7.1 WEBCLAW - SEARCH & INDEX ENGINE
================================================================================
📁 agents/webclaw/
├── 📄 webclaw.py (2731 B) - Main entry point
├── 📄 webclaw_agent.py (2563 B) - Agent class
├── 📄 agent_handler.py (5747 B) - A2A message handler (UNIVERSAL ROUTER)
│   FUNCTIONS:
│     • process_task(task, agent) - Main router for all agent commands
│     • route_to_agent_command(agent, task) - Route to specific agent
│   SUPPORTS: All 21 agents' commands
├── 📄 a2a_server.py (1181 B) - WebClaw's own A2A server (rarely used)
├── 📄 api_server.py (1102 B) - REST API for WebClaw
├── 📄 timeline_viewer.py (1450 B) - Chronicle timeline viewer
│
├── 📁 a2a/
│   ├── 📄 integrated_server.py (7409 B) - Integrated A2A handler
│   └── 📄 search_handler.py (0 B) - EMPTY (deprecated)
│
├── 📁 cache/ - INDEX STORAGE
│   ├── 📄 url_index.json (613 KB) - THE REAL SEARCH INDEX
│   │   FORMAT: {"url": {"content": "...", "title": "...", "category": "..."}}
│   │   SIZE: 33,116+ entries
│   └── 📄 web_cache.db (458 KB) - SQLite cache of fetched content
│
├── 📁 cli/
│   ├── 📄 parser.py (251 B) - Command parser
│   └── 📄 __init__.py (97 B)
│
├── 📁 commands/ - WEBCLAW'S OWN COMMANDS
│   ├── 📄 __init__.py (953 B) - Command registry
│   ├── 📄 browse.py (955 B) - /browse - Browse web categories
│   ├── 📄 cache_stats.py (915 B) - /cache - Cache statistics
│   ├── 📄 chronicle.py (1572 B) - /chronicle - Chronicle ledger queries
│   ├── 📄 fetch.py (6903 B) - /fetch - Fetch and cache URL
│   ├── 📄 help.py (1372 B) - /help - Show commands
│   ├── 📄 list.py (657 B) - /list - List available categories
│   ├── 📄 llm.py (1578 B) - /llm - LLM query with context
│   ├── 📄 quit.py (210 B) - /quit - Exit
│   ├── 📄 recall.py (848 B) - /recall - Recall from memory
│   ├── 📄 share.py (1993 B) - /share - Query all agents' knowledge
│   ├── 📄 stats.py (713 B) - /stats - Index statistics
│   └── 📄 system.py (392 B) - /system - System info
│
├── 📁 core/
│   ├── 📄 agent.py (2161 B) - WebClaw agent class
│   ├── 📄 api.py (3420 B) - OpenRouter + Ollama API
│   ├── 📄 cache.py (4360 B) - Caching system with SQLite
│   │   FUNCTIONS: get(), set(), _clean_old_entries(), stats()
│   ├── 📄 chronicle_ledger.py (6613 B) - Immutable URL tracking
│   │   FUNCTIONS: record_fetch(), recover_by_context(), get_timeline()
│   ├── 📄 config.py (899 B) - WebClaw configuration
│   ├── 📄 data.py (263 B) - Data path utilities
│   ├── 📄 pacer.py (3312 B) - PACER court records integration
│   ├── 📄 rate_limiter.py (4493 B) - Rate limiting & robots.txt
│   └── 📄 shared_memory.py (3722 B) - Cross-agent memory
│
├── 📁 docs/
│   ├── 📄 webclaw_documentation.md (24056 B)
│   ├── 📄 TETHERED_SYSTEM_DOCUMENTATION.md (22977 B)
│   └── 📄 CHRONICLE_ATTRIBUTION.md (1285 B)
│
├── 📁 providers/
│   └── 📄 webclaw_provider.py (3538 B) - Fast bitmap search
│       CLASSES: WebclawProvider
│       FUNCTIONS: build_index(), search(), search_with_highlight(), get_stats()
│       USES: shared/search/__init__.py (BitmapIndex)
│
├── 📁 references/ - 33,116+ MARKDOWN FILES
│   ├── 📄 MASTER_ATTRIBUTION_INDEX.md (5322 B)
│   ├── 📁 ai_ml/ - AI/ML references
│   ├── 📁 apis/ - API documentation
│   ├── 📁 backend/ - Backend development
│   ├── 📁 citations/ - Legal citations
│   ├── 📁 claw_coder/ - Code generation references
│   ├── 📁 cloud/ - Cloud computing
│   ├── 📁 cybersecurity/ - Security references
│   ├── 📁 databases/ - Database references
│   ├── 📁 data_science/ - Data science
│   ├── 📁 devops/ - DevOps
│   ├── 📁 docuclaw/ - Document generation refs
│   ├── 📁 flowclaw/ - Diagram references
│   ├── 📁 frontend/ - Frontend development
│   ├── 📁 game_dev/ - Game development
│   ├── 📁 interpretclaw/ - Translation refs
│   ├── 📁 langclaw/ - Language learning refs
│   ├── 📁 languages/ - Programming languages
│   ├── 📁 lawclaw/ - LEGAL REFERENCES (31,686+ files)
│   │   ├── 📁 courts/ - Court information
│   │   ├── 📁 statutes/ - Legal statutes
│   │   ├── 📁 cases/ - Case law
│   │   └── 📁 jurisdictions/ - Jurisdiction info
│   ├── 📁 liberateclaw/ - Model liberation refs
│   ├── 📁 mathematicaclaw/ - Math references
│   ├── 📁 mediclaw/ - Medical references
│   ├── 📁 mobile_dev/ - Mobile development
│   ├── 📁 monitoring/ - System monitoring
│   ├── 📁 networks/ - Networking
│   ├── 📁 programming_languages/ - Language references
│   ├── 📁 security/ - Security references
│   ├── 📁 testing/ - Testing references
│   ├── 📁 txclaw/ - Blockchain references
│   ├── 📁 web_development/ - Web dev references
│   ├── 📄 ai_ml_references.md (3006 B)
│   ├── 📄 cybersecurity_references.md (3444 B)
│   ├── 📄 javascript_reference.md (3626 B)
│   └── 📄 python_reference.md (3732 B)
│
├── 📁 resources/ - Additional resources
├── 📁 utils/
│   ├── 📄 content_parser.py (1073 B) - Extract content from various formats
│   ├── 📄 display.py (1062 B) - Display utilities
│   └── 📄 helpers.py (257 B) - Helper functions
│
└── 📄 TETHERED_SYSTEM_DOCUMENTATION.md (22977 B) - Complete system docs

================================================================================
7.2 LAWCLAW - LEGAL RESEARCH
================================================================================
📁 agents/lawclaw/
├── 📄 lawclaw.py (3009 B) - Main entry point
├── 📄 lawclaw_backup.py (8320 B) - Backup
├── 📄 lawclaw_original.py (22143 B) - Original version
│
├── 📁 cli/
│   └── 📄 parser.py (329 B)
│
├── 📁 commands/ - 19 LEGAL COMMANDS
│   ├── 📄 __init__.py (4251 B) - Command registry with categories
│   ├── 📄 analyze.py (401 B) - /analyze - Analyze legal text
│   ├── 📄 ask.py (560 B) - /ask - AI legal Q&A via WebClaw
│   ├── 📄 brief.py (366 B) - /brief - Find legal briefs
│   ├── 📄 browse.py (209 B) - /browse - Browse state courts
│   ├── 📄 cite.py (473 B) - /cite - Parse legal citations
│   ├── 📄 court.py (3600 B) - /court - County court info WITH LLM
│   │   FLOW: WebClaw search → LLM generation → Response
│   ├── 📄 docket.py (358 B) - /docket - Search court dockets
│   ├── 📄 federal.py (461 B) - /federal - Federal courts
│   ├── 📄 judge.py (427 B) - /judge - Judge information
│   ├── 📄 jurisdiction.py (651 B) - /jurisdiction - Jurisdiction info
│   ├── 📄 law.py (190 B) - /law - Legal research
│   ├── 📄 list.py (167 B) - /list - List resources
│   ├── 📄 oral.py (418 B) - /oral - Oral arguments
│   ├── 📄 precedent.py (460 B) - /precedent - Find precedents
│   ├── 📄 search.py (678 B) - /search - Search via WebClaw A2A
│   ├── 📄 state.py (743 B) - /state - State courts
│   ├── 📄 stats.py (292 B) - /stats - Statistics
│   ├── 📄 statute.py (410 B) - /statute - Look up statutes
│   └── 📄 summarize.py (397 B) - /summarize - Summarize cases
│
├── 📁 core/
│   ├── 📄 agent.py (385 B)
│   ├── 📄 api.py (1815 B)
│   ├── 📄 app.py (4509 B)
│   ├── 📄 config.py (610 B)
│   ├── 📄 data.py (1970 B)
│   └── 📄 display.py (1136 B)
│
├── 📁 display/
├── 📁 law_search/
│   ├── 📁 file/
│   ├── 📁 index/
│   └── 📁 web/
│
├── 📁 queries/
│   ├── 📄 case_searcher.py (3594 B)
│   ├── 📄 llm_searcher.py (2119 B)
│   ├── 📄 webclaw_queries.py (1196 B)
│   └── 📄 court_orchestrator.py (5129 B)
│
├── 📁 resources/
├── 📁 synthesis/
│   └── 📄 llm_synthesis.py (3833 B)
│
└── 📁 utils/
    ├── 📄 display.py (2026 B)
    └── 📄 helpers.py (257 B)

================================================================================
7.3 LLMCLAW - MODEL MANAGER
================================================================================
📁 agents/llmclaw/
├── 📄 llmclaw.py (274 B) - Main entry (launches interface.py)
│
├── 📁 cli/
│   └── 📄 interface.py (2809 B) - MAIN MODEL SELECTION MENU
│       FUNCTIONS: main_menu(), banner(), clear()
│       MENU OPTIONS:
│         [1] Stock Models (Ollama)
│         [2] Obliterated Models
│         [3] API Providers
│         [4] Proceed to Agent Selection
│         [5] Exit
│
├── 📁 commands/ - LLMCLAW COMMANDS
│   ├── 📄 __init__.py (692 B) - Command registry
│   ├── 📄 list.py (1488 B) - /list - List ALL models (stock + obliterated)
│   ├── 📄 normal.py (580 B) - /normal - Show stock models only
│   ├── 📄 obliterated.py (773 B) - /obliterated - Show obliterated models only
│   └── 📄 use.py (1159 B) - /use <model> - Switch active model
│
├── 📁 core/
│   ├── 📄 state.py (1093 B) - Active model state management
│   │   FUNCTIONS: get_active_model(), set_active_model()
│   └── 📄 sync.py (2387 B) - Sync to global state
│
├── 📁 providers/
│   ├── 📄 stock.py (3086 B) - STOCK MODEL SELECTOR
│   │   FUNCTIONS:
│   │     • get_stock_models() - Query Ollama for installed models
│   │     • select_stock_model() - Interactive selection menu
│   │     • sync_to_global_state() - Update working_llms.json
│   └── 📄 obliterated.py (3755 B) - OBLITERATED MODEL SELECTOR
│       FUNCTIONS:
│         • get_obliterated_models() - Scan models/obliterated/
│         • select_obliterated_model() - Interactive selection menu
│         • sync_to_global_state() - Update active_model.json
│
└── 📁 utils/

================================================================================
7.4 DATACLAW - DATA MANAGEMENT
================================================================================
📁 agents/dataclaw/
├── 📄 dataclaw.py (1081 B) - Main entry
│
├── 📁 cli/
│   ├── 📄 parser.py (162 B)
│   └── 📄 __init__.py (65 B)
│
├── 📁 commands/
│   ├── 📄 data.py (449 B) - /data - Data operations
│   └── 📄 system.py (355 B) - /system - System info
│
├── 📁 core/
│   ├── 📄 data.py (181 B)
│   └── 📄 __init__.py (63 B)
│
├── 📁 modules/
│   └── 📁 indexer/
│       └── 📄 local_indexer.py - index_file(), index_directory(), search_local()
│
├── 📁 references/
│   ├── 📄 data_index.db (16 KB) - Local data index
│   ├── 📁 algorithms/
│   ├── 📁 big_data/
│   ├── 📁 data_structures/
│   ├── 📁 data_visualization/
│   ├── 📁 data_warehousing/
│   ├── 📁 etl/
│   ├── 📁 machine_learning/
│   ├── 📁 nosql/
│   └── 📁 sql/
│
└── 📁 utils/
    └── 📄 helpers.py (255 B)

================================================================================
7.5 FLOWCLAW - DIAGRAMS & FLOWCHARTS
================================================================================
📁 agents/flowclaw/
├── 📄 flowclaw.py (11702 B) - Main entry
├── 📄 flowclaw_*.py (Multiple versions - 12 files)
│
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 flowchart.py (1953 B) - /flowchart - Generate flowcharts
│   └── 📄 mindmap.py (837 B) - /mindmap - Generate mindmaps
│
├── 📁 core/
│   ├── 📄 agent.py (1561 B)
│   └── 📄 __init__.py (31 B)
│
├── 📁 engine/
│   ├── 📄 diagram_engine.py (2237 B)
│   ├── 📄 diagram_processor.py (1311 B)
│   ├── 📄 diagram_types.py (2052 B)
│   ├── 📄 high_res_renderer.py (11718 B)
│   ├── 📄 mermaid_validator.py (1569 B)
│   ├── 📄 syntax_cleaner.py (1191 B)
│   └── 📄 syntax_validator.py (2475 B)
│
├── 📁 exporters/
│   ├── 📄 advanced_exporters.py (1147 B)
│   └── 📄 base_exporter.py (2535 B)
│
├── 📁 exports/ - Generated diagrams (many .mmd, .html files)
├── 📁 modules/
├── 📁 output/
├── 📁 providers/
├── 📁 templates/
├── 📁 viewer/
│   ├── 📄 advanced_viewer.py (1604 B)
│   ├── 📄 diagram_viewer.py (8069 B)
│   ├── 📄 popup_viewer.py (3390 B)
│   └── 📄 save_handler.py (1292 B)
│
└── 📄 schemaclaw.py (3032 B) - Schema generation

================================================================================
7.6 DOCUCLAW - DOCUMENT GENERATION
================================================================================
📁 agents/docuclaw/
├── 📄 docuclaw.py (547 B)
├── 📄 docuclaw_clean.py (10259 B)
├── 📄 media_importer.py (7583 B)
├── 📄 session_manager.py (2447 B)
│
├── 📁 cli/
├── 📁 code_processors/
├── 📁 commands/ - 30+ COMMANDS
│   ├── 📄 analyze.py, batchprint.py, codesearch.py, codestats.py
│   ├── 📄 create.py, csvtable.py, diagram.py, diff.py, doc.py
│   ├── 📄 draft.py, export.py, exportapp.py, flowchart.py
│   ├── 📄 footer.py, footnote.py, formatcode.py, header.py
│   ├── 📄 help.py, highlight.py, import.py, layout.py
│   ├── 📄 pagenum.py, print.py, printfile.py, quit.py
│   ├── 📄 review.py, table.py, templates.py, toc.py
│   ├── 📄 topdf.py, translate.py
│   └── 📄 __init__.py
│
├── 📁 core/
├── 📁 exporters/ - csv, docx, html, json, markdown, odt, pdf, rtf, text, xml
├── 📁 formatters/
├── 📁 importers/
├── 📁 imports/
├── 📁 modules/
│   └── 📁 ai/ - AI-powered document generation
├── 📁 output/ - Generated documents (many .html, .md files)
├── 📁 printers/
├── 📁 processors/
├── 📁 session/
├── 📁 templates/
│   ├── 📁 business/
│   ├── 📁 education/
│   ├── 📁 personal/
│   └── 📁 technical/
└── 📁 utils/

================================================================================
7.7 MATHEMATICACLAW - MATH & VISUALIZATION
================================================================================
📁 agents/mathematicaclaw/
├── 📄 mathematicaclaw.py (1848 B)
├── 📄 mathematicaclaw_complete.py (6330 B)
├── 📄 agent.py (4339 B)
├── 📄 ai_assistant.py (12715 B)
├── 📄 ai_visualizer.py (2415 B)
│
├── 📁 cli/
│   ├── 📄 interface.py (7942 B)
│   └── 📄 main.py (5960 B)
│
├── 📁 commands/
│   ├── 📄 add.py, algebra.py, arithmetic.py, calculus.py
│   ├── 📄 math.py, plot.py, solve.py, system.py
│   └── 📄 __init__.py
│
├── 📁 core/
│   ├── 📄 agent.py (2300 B)
│   ├── 📄 engine.py (7761 B)
│   ├── 📄 math_engine.py (4354 B)
│   └── 📄 session_manager.py (795 B)
│
├── 📁 handlers/
│   ├── 📄 algebra_commands.py (2631 B)
│   ├── 📄 arithmetic_commands.py (3203 B)
│   ├── 📄 calculus_commands.py (1907 B)
│   ├── 📄 command_handler.py (2018 B)
│   ├── 📄 expression_handler.py (470 B)
│   ├── 📄 math_handler.py (1034 B)
│   ├── 📄 plot_commands.py (1574 B)
│   └── 📄 system_commands.py (685 B)
│
├── 📁 visualization/
│   ├── 📄 graph_builder.py (3705 B)
│   └── 📄 plotter.py (5883 B)
│
└── 📁 providers/

================================================================================
7.8 CLAW_CODER - CODE GENERATION (38 LANGUAGES)
================================================================================
📁 agents/claw_coder/
├── 📄 claw_coder.py (2187 B)
├── 📄 hooks.py (1287 B)
├── 📄 test_ai.py, test_discovery.py, test_import.py
│
├── 📁 agents/
│   ├── 📄 dataclaw_client.py (959 B)
│   └── 📄 webclaw_client.py (917 B)
│
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 code.py (716 B) - /code - Generate code
│   └── 📄 system.py (355 B)
│
├── 📁 engine/
│   ├── 📄 base_language.py (903 B)
│   ├── 📄 llm_wrapper.py (823 B)
│   ├── 📄 memory.py (1997 B)
│   ├── 📄 orchestrator.py (3899 B)
│   └── 📄 programming_engine.py (3568 B)
│
├── 📁 languages/ - 38 LANGUAGE IMPLEMENTATIONS
│   ├── 📄 assembly.py, bash.py, batch.py, c.py, clojure.py, cobol.py
│   ├── 📄 cpp.py, csharp.py, dart.py, elixir.py, erlang.py, fortran.py
│   ├── 📄 go.py, groovy.py, haskell.py, html.py, java.py, javascript.py
│   ├── 📄 julia.py, kotlin.py, lua.py, makefile.py, matlab.py, nim.py
│   ├── 📄 objectivec.py, perl.py, php.py, powershell.py, python.py
│   ├── 📄 r.py, ruby.py, rust.py, scala.py, sql.py, swift.py
│   ├── 📄 typescript.py, vhdl.py, yaml.py, zig.py
│   └── 📄 __init__.py
│
├── 📁 integrations/
├── 📁 src/ - RUST INTEGRATION
│   ├── 📄 chronicle_bridge.rs (3631 B)
│   ├── 📄 a2a.rs (2243 B)
│   ├── 📄 chronicle_commands.rs (3243 B)
│   ├── 📄 lib.rs (553 B)
│   ├── 📄 main.rs (5574 B)
│   ├── 📄 memory.rs (3765 B)
│   └── 📄 security.rs (1952 B)
│
└── 📄 Cargo.toml (1332 B) - Rust dependencies

================================================================================
7.9 LIBERATECLAW - MODEL LIBERATION/OBLITERATION
================================================================================
📁 agents/liberateclaw/
├── 📄 liberateclaw.py (4299 B)
│
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 liberate.py (1567 B) - /liberate - Download model
│   ├── 📄 liberated.py (1025 B) - /liberated - List liberated models
│   ├── 📄 models.py (760 B) - /models - List available models
│   ├── 📄 obliterate.py (1996 B) - /obliterate - Obliterate model
│   ├── 📄 remote.py (3877 B) - /remote - Remote model operations
│   └── 📄 use.py (1562 B) - /use - Use liberated model
│
├── 📁 config/
├── 📁 core/
├── 📁 data/
│   └── 📄 shared_memory.json (109 B)
├── 📁 exports/ - Modelfiles
│   ├── 📄 codellama-liberated.Modelfile (373 B)
│   ├── 📄 deepseek-coder-liberated.Modelfile (380 B)
│   ├── 📄 deepseek-r1-liberated.Modelfile (375 B)
│   ├── 📄 gemma3-liberated.Modelfile (370 B)
│   ├── 📄 llama3.2-liberated.Modelfile (372 B)
│   ├── 📄 qwen3-coder-liberated.Modelfile (376 B)
│   └── 📄 qwen3-vl-liberated.Modelfile (373 B)
│
├── 📁 fetchers/
├── 📁 providers/
└── 📁 utils/

================================================================================
7.10 MEDICLAW - MEDICAL REFERENCES
================================================================================
📁 agents/mediclaw/
├── 📄 mediclaw.py (1301 B)
│
├── 📁 cli/
│   ├── 📄 interface.py (8019 B)
│   └── 📄 __init__.py (1803 B)
│
├── 📁 commands/
│   ├── 📄 clinical_commands.py (1033 B)
│   ├── 📄 commands.py (7829 B)
│   ├── 📄 core_commands.py (1452 B)
│   ├── 📄 diagnose.py (321 B)
│   ├── 📄 lifestyle_commands.py (1324 B)
│   ├── 📄 med.py (966 B)
│   ├── 📄 pharma_commands.py (984 B)
│   ├── 📄 research.py (629 B)
│   ├── 📄 sources.py (518 B)
│   ├── 📄 specialty_commands.py (1241 B)
│   ├── 📄 stats.py (441 B)
│   └── 📄 treatment.py (327 B)
│
├── 📁 config/
├── 📁 core/
│   ├── 📄 agent.py (387 B)
│   └── 📄 engine.py (1281 B)
│
├── 📁 docs/
│   └── 📄 Mediclaw.md (11693 B)
│
├── 📁 fetchers/
│   └── 📄 url_fetcher.py (1991 B)
│
├── 📁 providers/
│   ├── 📄 anthropic.py (1038 B)
│   ├── 📄 api_provider.py (1281 B)
│   ├── 📄 ollama.py (970 B)
│   ├── 📄 ollama_provider.py (836 B)
│   ├── 📄 openrouter.py (835 B)
│   ├── 📄 openrouter_provider.py (917 B)
│   ├── 📄 providers.py (2492 B)
│   └── 📄 webclaw_provider.py (853 B)
│
└── 📁 utils/

================================================================================
7.11 INTERPRETCLAW - TRANSLATION & SPEECH
================================================================================
📁 agents/interpretclaw/
├── 📄 interpretclaw.py (2489 B)
│
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 detect.py (921 B) - /detect - Detect language
│   ├── 📄 help.py (747 B)
│   ├── 📄 languages.py (526 B) - /languages - List supported languages
│   ├── 📄 lesson.py (1069 B) - /lesson - Language lessons
│   ├── 📄 listen.py (1189 B) - /listen - Speech to text
│   ├── 📄 speak.py (679 B) - /speak - Text to speech
│   ├── 📄 translate.py (1186 B) - /translate - Translate text
│   ├── 📄 translatedoc.py (1460 B) - /translatedoc - Translate documents
│   └── 📄 vocab.py (924 B) - /vocab - Vocabulary practice
│
├── 📁 core/
│   ├── 📄 config.py (1335 B)
│   └── 📄 data.py (183 B)
│
├── 📁 languages/
│   ├── 📁 asian_languages/
│   ├── 📁 cultural_notes/
│   ├── 📁 european_languages/
│   ├── 📁 grammar/
│   ├── 📁 localization/
│   ├── 📁 middle_eastern/
│   ├── 📁 phrase_dictionaries/
│   └── 📁 translation_apis/
│
├── 📁 stt/ - Speech to Text
├── 📁 translator/
│   ├── 📁 engines/
│   ├── 📁 formats/
│   ├── 📄 core.py (2952 B)
│   └── 📄 llm_translator.py (634 B)
│
├── 📁 tts/ - Text to Speech
└── 📁 utils/

================================================================================
7.12 LANGCLAW - LANGUAGE LEARNING
================================================================================
📁 agents/langclaw/
├── 📄 langclaw.py (2862 B)
│
├── 📁 audio/
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 commands.py (478 B)
│   ├── 📄 conversation.py (823 B)
│   ├── 📄 lesson.py (779 B)
│   ├── 📄 practice.py (662 B)
│   ├── 📄 speak.py (321 B)
│   ├── 📄 teach.py (753 B)
│   └── 📄 vocab.py (829 B)
│
├── 📁 config/
│   └── 📄 settings.py (1105 B)
│
├── 📁 core/
│   ├── 📄 agent.py (1355 B)
│   ├── 📄 lesson_engine.py (1845 B)
│   ├── 📄 llm_wrapper.py (1207 B)
│   ├── 📄 session_manager.py (980 B)
│   ├── 📄 stt_engine.py (2251 B)
│   ├── 📄 translator.py (1507 B)
│   └── 📄 tts_engine.py (2208 B)
│
├── 📁 fetchers/
│   ├── 📄 translation_fetcher.py (1226 B)
│   └── 📄 url_fetcher.py (995 B)
│
├── 📁 providers/
│   ├── 📄 api_provider.py (2006 B)
│   └── 📄 webclaw_provider.py (3007 B)
│
├── 📁 references/
│   ├── 📁 asian_languages/
│   ├── 📁 cultural_notes/
│   ├── 📁 european_languages/
│   ├── 📁 grammar/
│   ├── 📁 localization/
│   ├── 📁 middle_eastern/
│   └── 📄 languages.md (1245 B)
│
├── 📁 stt/
│   └── 📄 stt_engine.py (5348 B)
│
├── 📁 teacher/
│   ├── 📁 exercises/
│   ├── 📁 lessons/
│   └── 📄 core.py (2398 B)
│
├── 📁 translator/
├── 📁 tts/
│   ├── 📁 engines/
│   ├── 📁 formats/
│   ├── 📄 engine.py (1240 B)
│   ├── 📄 player.py (3725 B)
│   └── 📄 tts_engine.py (4920 B)
│
├── 📁 tts_cache/ - Cached audio files
│   ├── 📄 google_es_-6837574656301321503.mp3 (6 KB)
│   ├── 📄 google_es_-7505699946232858754.mp3 (6 KB)
│   ├── 📄 google_es_682302535184967994.mp3 (6 KB)
│   └── 📄 google_es_7298730963098077579.mp3 (6 KB)
│
└── 📁 utils/
    └── 📄 helpers.py (731 B)

================================================================================
7.13 TXCLAW - BLOCKCHAIN
================================================================================
📁 agents/TXclaw/
├── 📄 txclaw.py (1168 B)
├── 📄 README.md (1195 B)
│
├── 📁 .txclaw/
├── 📁 cli/
│   ├── 📄 commands_list.py (2683 B)
│   ├── 📄 interface.py (3954 B)
│   └── 📄 settings.py (997 B)
│
├── 📁 commands/
├── 📁 config/
│   └── 📄 networks.json (547 B)
│
├── 📁 contracts/
│   ├── 📁 auction_contract/
│   └── 📁 my_auction_contract/
│
├── 📁 core/
│   ├── 📄 agent.py (568 B)
│   └── 📄 commands.py (3660 B)
│
├── 📁 fetchers/
│   └── 📄 url_fetcher.py (2464 B)
│
├── 📁 modules/
│   ├── 📁 ai/
│   ├── 📁 contracts/
│   ├── 📁 deploy/
│   ├── 📁 network/
│   ├── 📁 references/
│   └── 📁 tests/
│
├── 📁 providers/
│   └── 📄 api_provider.py (1619 B)
│
├── 📁 references/
│   └── 📄 tx_references.py (1693 B)
│
└── 📁 utils/
    └── 📄 helpers.py (1550 B)

================================================================================
7.14 DREAMCLAW - AI VISION & GENERATION
================================================================================
📁 agents/dreamclaw/
├── 📄 dreamclaw.py (1750 B)
│
├── 📁 cli/
├── 📁 commands/
├── 📁 core/
│   ├── 📄 agent.py (6755 B)
│   └── 📄 dream.py (1586 B)
│
├── 📁 exports/
│   ├── 📄 dream_1826.png (6 KB)
│   ├── 📄 dream_4711.png (6 KB)
│   ├── 📄 dream_7163.png (7 KB)
│   └── 📄 dream_8407.png (15 KB)
│
├── 📁 providers/
└── 📁 utils/

================================================================================
7.15 DESIGNCLAW - GRAPHIC DESIGN
================================================================================
📁 agents/designclaw/
├── 📄 designclaw.py (1176 B)
├── 📄 README.md (5748 B)
│
├── 📁 cli/
├── 📁 commands/
│   └── 📄 logo.py (1747 B)
│
├── 📁 core/
│   └── 📄 agent.py (5496 B)
│
├── 📁 data/
│   └── 📄 shared_memory.json (107 B)
│
├── 📁 exports/
├── 📁 providers/
├── 📁 utils/
│   ├── 📄 input_handler.py (3888 B)
│   └── 📄 preview.py (7076 B)
│
└── 📄 .env (0 B)

================================================================================
7.16 DRAFTCLAW - TECHNICAL DRAWINGS
================================================================================
📁 agents/draftclaw/
├── 📄 draftclaw.py (1750 B)
│
├── 📁 cli/
├── 📁 commands/
│   └── 📄 blueprint.py (1988 B)
│
├── 📁 core/
│   └── 📄 agent.py (2518 B)
│
├── 📁 exports/
├── 📁 providers/
└── 📁 utils/

================================================================================
7.17 DRAWCLAW - DRAWING
================================================================================
📁 agents/drawclaw/
├── 📄 drawclaw.py (1923 B)
│
├── 📁 cli/
├── 📁 commands/
├── 📁 core/
│   └── 📄 agent.py (1875 B)
│
├── 📁 exports/
├── 📁 providers/
└── 📁 utils/

================================================================================
7.18 FILECLAW - FILE ANALYSIS
================================================================================
📁 agents/fileclaw/
├── 📄 fileclaw.py (16098 B)
│
├── 📁 commands/
├── 📁 core/
├── 📁 handlers/
├── 📁 modules/
└── 📁 utils/

================================================================================
7.19 PLOTCLAW - CHARTS & GRAPHS
================================================================================
📁 agents/plotclaw/
├── 📄 plotclaw.py (1743 B)
├── 📄 utils.py (301 B)
│
├── 📁 cli/
├── 📁 commands/
│   ├── 📄 bar.py (1648 B)
│   ├── 📄 pie.py (1419 B)
│   └── 📄 plot.py (1935 B)
│
├── 📁 core/
│   └── 📄 agent.py (1557 B)
│
├── 📁 exports/
│   ├── 📄 bar_2646.png (23 KB)
│   ├── 📄 pie_1317.png (34 KB)
│   ├── 📄 plot_153.png (66 KB)
│   └── 📄 plot_4417.png (55 KB)
│
├── 📁 providers/
└── 📁 utils/

================================================================================
7.20 RUSTYPYCRAW - CODE CRAWLER
================================================================================
📁 agents/rustypycraw/
├── 📄 rustypycraw.py (1059 B)
│
├── 📁 a2a/
│   └── 📄 client.py (1705 B)
│
├── 📁 integrations/
│   └── 📄 chronicle_bridge.py (5678 B)
│
├── 📁 modules/
│   ├── 📁 analyzer/
│   ├── 📁 crawler/
│   ├── 📁 indexer/
│   ├── 📁 llm/
│   └── 📁 scanner/
│
└── 📄 __init__.py (27 B)

================================================================================
7.21 CRUSTYCLAW - RUST AI ASSISTANT
================================================================================
📁 agents/crustyclaw/
└── (Empty/minimal - no main .py file)

================================================================================
7.22 FORK - AGENT FORKING
================================================================================
📁 agents/fork/
├── 📄 fork.py (932 B)
├── 📄 fork_agent.py (2356 B)
└── (Minimal implementation)

================================================================================
8. CHRONICLE SYSTEM - DATACLAW & WEBCLAW INDEXING
================================================================================

CHRONICLE LEDGER (WebClaw):
  File: agents/webclaw/core/chronicle_ledger.py
  Purpose: Immutable URL tracking with context recovery
  Functions:
    • record_fetch(url, content_hash, context) - Record a fetch
    • recover_by_context(query) - Find URLs by context
    • get_timeline() - Chronological history
    • to_dict() / _load_ledger() / _save_ledger()
  Storage: ~/.clawpack/chronicle_ledger.json (empty currently)

DATA INDEX (DataClaw):
  File: agents/dataclaw/references/data_index.db (16 KB)
  Purpose: Local data file index
  Managed by: agents/dataclaw/modules/indexer/local_indexer.py
  Functions: index_file(), index_directory(), search_local()

WEB INDEX (WebClaw):
  File: agents/webclaw/cache/url_index.json (613 KB)
  Purpose: Fast URL-to-content mapping for 33,116+ files
  Format: JSON dictionary with content, title, category
  File: agents/webclaw/cache/web_cache.db (458 KB)
  Purpose: SQLite cache of fetched web content
  Managed by: agents/webclaw/core/cache.py

================================================================================
9. MEMORY SYSTEM - THREE-TIER ARCHITECTURE
================================================================================

File: shared/memory/three_tier.py (5406 B)

ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│ WORKING MEMORY (8K tokens default, escalates to 64K)        │
│ • Current conversation context                              │
│ • Most recent interactions                                  │
│ • Token budget management                                   │
├─────────────────────────────────────────────────────────────┤
│ SEMANTIC MEMORY                                             │
│ • Facts and knowledge extracted from conversations          │
│ • Long-term factual storage                                 │
│ • Queryable by similarity                                   │
├─────────────────────────────────────────────────────────────┤
│ EPISODIC MEMORY                                             │
│ • Past interaction history                                  │
│ • Conversation summaries                                    │
│ • Contextual recall                                         │
├─────────────────────────────────────────────────────────────┤
│ PROCEDURAL MEMORY (procedural_memory.py)                    │
│ • Learned procedures and workflows                          │
│ • Executable action sequences                               │
└─────────────────────────────────────────────────────────────┘

SLOT RESERVATION (Claude Code Pattern #9):
  File: shared/llm/slot_reservation.py
  • Default: 8,000 tokens
  • On truncation: Double up to 64,000 tokens
  • Tracks savings and truncation rate

================================================================================
10. LLM INTEGRATION - API, OLLAMA, OBLITERATED
================================================================================

PROVIDER PRIORITY (shared/llm/manager.py):
  1. Obliterated models (if prefer_liberated=True)
  2. OpenRouter (if API key exists)
  3. Anthropic (if API key exists)
  4. OpenAI (if API key exists)
  5. Ollama (local fallback)

ACTIVE MODEL DETERMINATION:
  1. models/active_model.json - User selected model
  2. working_llms.json - Priority-ordered provider list
  3. .env - API keys

OLLAMA MODELS (13 installed):
  • gemma3:12b (8.1 GB) - DEFAULT ACTIVE
  • tinyllama:1.1b (637 MB)
  • gemma3-liberated:latest (815 MB)
  • codellama-liberated:latest (3.8 GB)
  • deepseek-coder-liberated:latest (3.8 GB)
  • codellama:7b (3.8 GB)
  • qwen3-vl:30b (19 GB)
  • qwen3-coder:30b (18 GB)
  • deepseek-r1:8b (5.2 GB)
  • gemma3:4b (3.3 GB)
  • gemma3:27b (17 GB)
  • deepseek-coder:6.7b (3.8 GB)
  • gemma3:1b (815 MB)

OBLITERATED MODELS (6 full models, 49.7 GB total):
  • codellama_7b (12.55 GB)
  • deepseek_coder_6.7b (12.56 GB)
  • phi2 (5.18 GB)
  • qwen_coder_7b (14.19 GB)
  • smollm2_1.7b (3.19 GB)
  • tinyllama (2.05 GB)

================================================================================
11. ROUTES - ALL API ENDPOINTS
================================================================================

📁 routes/
├── 📄 __init__.py (859 B)
├── 📄 registry.py (1783 B) - Route registry
├── 📄 blockchain_routes.py (353 B)
├── 📄 code_routes.py (352 B)
├── 📄 data_routes.py (343 B)
├── 📄 document_routes.py (353 B)
├── 📄 fork_routes.py (296 B)
├── 📄 language_routes.py (363 B)
├── 📄 lawclaw_routes.py (361 B)
├── 📄 liberateclaw_routes.py (374 B)
├── 📄 math_routes.py (518 B)
├── 📄 medical_routes.py (374 B)
├── 📄 search_routes.py (363 B)
├── 📄 translation_routes.py (523 B)
├── 📄 voice_routes.py (309 B)
└── 📄 web_routes.py (421 B)

================================================================================
12. SCRIPTS & UTILITIES
================================================================================

📁 scripts/
├── 📄 index_all_courts.py (2904 B) - Index all court data
├── 📄 index_claw_coder_refs.py (2053 B) - Index code references
└── 📄 index_references.py (1560 B) - General reference indexer

================================================================================
13. TESTS
================================================================================

📁 tests/
├── 📄 test_agents.py (2215 B)
├── 📄 test_apis.py (2611 B)
├── 📄 test_base.py (950 B)
├── 📄 test_law.py (190 B)
├── 📄 test_providers.py (443 B)
├── 📄 test_sync.py (559 B)
├── 📄 test_unified_llm.py (1081 B)
├── 📄 debug_llmclaw.py (1048 B)
├── 📄 add.py (713 B)
└── 📄 plot.py (1125 B)

================================================================================
14. GIT STRUCTURE
================================================================================

Branch: main
Status: Ahead of origin/main by 1 commit
Working tree: Clean (all changes committed)

Recent commits:
  • Fixed WebClaw search index, removed dumb scanner, added three-tier memory

================================================================================
15. TROUBLESHOOTING GUIDE
================================================================================

PROBLEM: "ModuleNotFoundError: No module named 'shared.search'"
  SOLUTION: shared/search/__init__.py was missing - FIXED

PROBLEM: "/court returns nothing"
  SOLUTION: Active model was obliterated, needed Ollama - FIXED (switched to gemma3:12b)

PROBLEM: "BitmapIndex has no attribute 'add_batch'"
  SOLUTION: Implemented complete BitmapIndex class - FIXED

PROBLEM: A2A server not responding
  SOLUTION: Start a2a_server.py FIRST, keep running in separate terminal

PROBLEM: LLM not responding
  CHECK: Ollama running? (ollama list)
  CHECK: active_model.json has valid stock model
  CHECK: .env has API keys for cloud providers

================================================================================
16. STARTUP SEQUENCE (EXACT ORDER)
================================================================================

TERMINAL 1 (SERVER - LEAVE RUNNING FOREVER):
  cd C:\Users\greg\dev\clawpack_v2
  python a2a_server.py
  (Should show: ✅ 21 Agents Registered, port 8766)

TERMINAL 2 (MAIN APPLICATION):
  cd C:\Users\greg\dev\clawpack_v2
  python clawpack.py
  
  THEN:
  1. Press 'm' for model selection (optional - defaults to gemma3:12b)
  2. Select [1] Stock or [2] Obliterated
  3. Choose specific model
  4. Press '4' to proceed to agent selection
  5. Select agent 1-21
  6. Use agent commands

TO SWITCH MODELS:
  • From agent menu: press 'm'
  • From within agent: /quit, then 'm'

TO EXIT:
  • From agent: /quit
  • From main menu: 'q'
  • Server: Ctrl+C (only when completely done)

================================================================================
END OF DOCUMENTATION
================================================================================
