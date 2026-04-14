# CLAWPACK_V2 - COMPLETE AGENT DOCUMENTATION
# Every Agent, Every File, Every Function

AGENT COUNT: 22 TOTAL AGENTS


================================================================================
🤖 AGENT: claw_coder
================================================================================
Location: agents/claw_coder/

📄 claw_coder.py - MAIN ENTRY (2187 bytes)
   Purpose: claw_coder - Modular AI Programming Assistant
   Functions: process_command, fib, main

📁 commands/ - 2 commands
   📄 code.py - /code
      Functions: run
   📄 system.py - /system
      Functions: test_command, help_command, quit_command

📁 cli/ - 1 files
   📄 parser.py

📁 utils/ - 2 files (343 bytes)

📁 engine/ - 7 files (11 KB)


================================================================================
🤖 AGENT: crustyclaw
================================================================================
Location: agents/crustyclaw/

❌ crustyclaw.py - MISSING


================================================================================
🤖 AGENT: dataclaw
================================================================================
Location: agents/dataclaw/

📄 dataclaw.py - MAIN ENTRY (1081 bytes)
   Purpose: DataClaw - Simple working version
   Functions: __init__, handle, add_reference, search, main
   Classes: DataClaw

📁 commands/ - 2 commands
   📄 data.py - /data
      Data references from chronicle
      Functions: run
   📄 system.py - /system
      Functions: test_command, help_command, quit_command

📁 core/ - 1 modules
   📄 data.py (181 bytes)
      Functions: get_data_path

📁 cli/ - 1 files
   📄 parser.py

📁 references/ - 12 files (19 KB)

📁 utils/ - 2 files (343 bytes)

📁 modules/ - 9 files (7 KB)


================================================================================
🤖 AGENT: designclaw
================================================================================
Location: agents/designclaw/

📄 designclaw.py - MAIN ENTRY (1176 bytes)
   Purpose: designclaw - Creative Design Agent
   Functions: __init__, handle, main, _search_chronicle
   Classes: designclawAgent

📁 commands/ - 1 commands
   📄 logo.py - logo
      Logo command - Generate logos
      Functions: run

📁 core/ - 1 modules
   📄 agent.py (5496 bytes)
      Designclaw Core - AI-Powered Design Assistant
      Functions: __init__, process, _ai_brand_identity, _ai_color_palette, _ai_mood, _ai_typography, _ai_copywriting, _ai_general, _fallback_brand, _interactive_mode, _help
      Classes: designclawCore

📁 utils/ - 3 files (11 KB)

📁 data/ - 1 files (107 bytes)


================================================================================
🤖 AGENT: docuclaw
================================================================================
Location: agents/docuclaw/

📄 docuclaw.py - MAIN ENTRY (547 bytes)
   Purpose: DocuClaw - Document Processor

📁 commands/ - 31 commands
   📄 analyze.py - /analyze
      Analyze document command
      Functions: run
   📄 batchprint.py - /batchprint
      Batch print multiple files
      Functions: run
   📄 codesearch.py - /codesearch
      Search code across files
      Functions: run
   📄 codestats.py - /codestats
      Analyze code statistics
      Functions: run
   📄 create.py - /create
      Create document from template
      Functions: run
   📄 csvtable.py - /csvtable
      Import CSV as markdown table
      Functions: run
   📄 diagram.py - /diagram
      Functions: run
   📄 diff.py - /diff
      Compare two code files
      Functions: run
   📄 doc.py - /doc
      Document references from chronicle
      Functions: run
   📄 draft.py - /draft
      Draft a document using templates
      Functions: run
   📄 export.py - /export
      Export document command
      Functions: run
   📄 exportapp.py - /exportapp
      Export to other applications
      Functions: run
   📄 flowchart.py - /flowchart
      Functions: run
   📄 footer.py - /footer
      Add footer to document
      Functions: run
   📄 footnote.py - /footnote
      Add footnote to document
      Functions: run
   📄 formatcode.py - /formatcode
      Auto-format code files
      Functions: run
   📄 header.py - /header
      Add header to document
      Functions: run
   📄 help.py - /help
      Help command
      Functions: run
   📄 highlight.py - /highlight
      Syntax highlighting for code files
      Functions: run
   📄 import.py - /import
      Import document command
      Functions: run
   📄 layout.py - /layout
      Set page layout
      Functions: run
   📄 pagenum.py - /pagenum
      Add page numbers
      Functions: run
   📄 print.py - /print
      Print to printer command (Windows)
      Functions: run
   📄 printfile.py - /printfile
      Print to file command
      Functions: run
   📄 quit.py - /quit
      Quit command
      Functions: run
   📄 review.py - review
      Review and edit documents
      Functions: run
   📄 table.py - /table
      Create a table
      Functions: run
   📄 templates.py - /templates
      List templates command
      Functions: run
   📄 toc.py - /toc
      Generate table of contents
      Functions: run
   📄 topdf.py - /topdf
      Convert to PDF command
      Functions: run
   📄 translate.py - translate
      Translate documents using Interpretclaw's real translation engine
      Functions: run

📁 core/ - 2 modules
   📄 base.py (255 bytes)
      Base processor class
      Functions: process, analyze
      Classes: BaseProcessor
   📄 config.py (211 bytes)
      DocuClaw config

📁 cli/ - 1 files
   📄 parser.py

📁 utils/ - 2 files (343 bytes)

📁 modules/ - 11 files (1006 bytes)

📁 output/ - 34 files (33 KB)


================================================================================
🤖 AGENT: draftclaw
================================================================================
Location: agents/draftclaw/

📄 draftclaw.py - MAIN ENTRY (1750 bytes)
   Purpose: draftclaw - Modular Agent
   Functions: __init__, handle, main, _search_chronicle
   Classes: draftclawAgent

📁 commands/ - 1 commands
   📄 blueprint.py - blueprint
      Blueprint command - Create technical blueprints
      Functions: run

📁 core/ - 1 modules
   📄 agent.py (2518 bytes)
      draftclaw Core Logic
      Functions: process, process_command, main, _help
      Classes: draftclawCore

📁 utils/ - 1 files (33 bytes)


================================================================================
🤖 AGENT: drawclaw
================================================================================
Location: agents/drawclaw/

📄 drawclaw.py - MAIN ENTRY (1923 bytes)
   Purpose: drawclaw - Casual Drawing Agent
   Functions: __init__, handle, main
   Classes: drawclawAgent

📁 commands/ - 0 commands

📁 core/ - 1 modules
   📄 agent.py (1875 bytes)
      Drawclaw Core Logic - Casual drawing
      Functions: process, _sketch, _doodle, _paint, _illustrate, _cartoon, _meme, _help
      Classes: drawclawCore


================================================================================
🤖 AGENT: dreamclaw
================================================================================
Location: agents/dreamclaw/

📄 dreamclaw.py - MAIN ENTRY (1750 bytes)
   Purpose: dreamclaw - Modular Agent
   Functions: __init__, handle, main, _search_chronicle
   Classes: dreamclawAgent

📁 commands/ - 1 commands
   📄 dream.py - dream
      Dream command - Generate AI images with pop-up
      Functions: run

📁 core/ - 1 modules
   📄 agent.py (6755 bytes)
      dreamclaw Core Logic
      Functions: process, __init__, _load_key, analyze_image, generate_prompt, create_visualization, dream, run, _help
      Classes: dreamclawCore, Dreamclaw

📁 utils/ - 1 files (33 bytes)


================================================================================
🤖 AGENT: fileclaw
================================================================================
Location: agents/fileclaw/

📄 fileclaw.py - MAIN ENTRY (16098 bytes)
   Purpose: FileClaw - Intelligent File Management Agent
   Functions: __init__, _init_llm, analyze_file, convert_file, batch_process, find_files, _detect_type, _calculate_hash, __init__, handle, _analyze, _convert, _batch, _find, _info, collaborate, _help, main
   Classes: FileClawCore, FileClawAgent

📁 commands/ - 0 commands

📁 core/ - 0 modules

📁 utils/ - 1 files (0 bytes)

📁 modules/ - 1 files (0 bytes)

📁 handlers/ - 1 files (0 bytes)


================================================================================
🤖 AGENT: flowclaw
================================================================================
Location: agents/flowclaw/

📄 flowclaw.py - MAIN ENTRY (11702 bytes)
   Purpose: FlowClaw - Reliable Diagram Generator
   Functions: __init__, _init_llm, _init_chronicle, search_references, generate_diagram, show, __init__, view, ai, search, status, templates, test_all, process, help, main, smart_view
   Classes: LLMInterface, Renderer, FlowClaw

📁 commands/ - 2 commands
   📄 flowchart.py - flowchart
      Flowchart command - Creates diagrams with pop-up
      Functions: run
   📄 mindmap.py - mindmap
      Mindmap command - Creates mind maps
      Functions: run

📁 core/ - 1 modules
   📄 agent.py (1561 bytes)
      flowclaw Core Logic
      Functions: process, process_command, main, _help
      Classes: flowclawCore

📁 utils/ - 1 files (32 bytes)

📁 modules/ - 7 files (4 KB)

📁 engine/ - 8 files (22 KB)

📁 output/ - 55 files (25 KB)


================================================================================
🤖 AGENT: interpretclaw
================================================================================
Location: agents/interpretclaw/

📄 interpretclaw.py - MAIN ENTRY (2489 bytes)
   Purpose: Interpretclaw - Translation, Language Learning with Chronicle
   Functions: process_command, main, process_command

📁 commands/ - 10 commands
   📄 detect.py - /detect
      Detect language of text
      Functions: run
   📄 help.py - /help
      Help command
      Functions: run
   📄 languages.py - /languages
      List all supported languages
      Functions: run
   📄 lesson.py - /lesson
      Get language lesson from chronicle references
      Functions: run
   📄 listen.py - /listen
      Speech-to-text using microphone
      Functions: run
   📄 quit.py - /quit
      Quit command
      Functions: run
   📄 speak.py - /speak
      Text-to-speech using espeak
      Functions: run
   📄 translate.py - /translate
      Translate text using LLM (same as lawclaw)
      Functions: run
   📄 translatedoc.py - /translatedoc
      Translate an entire document using modular translator
      Functions: run
   📄 vocab.py - /vocab
      Look up vocabulary using chronicle references
      Functions: run

📁 core/ - 2 modules
   📄 config.py (1335 bytes)
      InterpretClaw configuration - Human Language Hub
      Functions: get_config
   📄 data.py (183 bytes)
      Functions: get_data_path

📁 cli/ - 1 files
   📄 parser.py

📁 references/ - 8 files (2 KB)

📁 utils/ - 2 files (343 bytes)


================================================================================
🤖 AGENT: langclaw
================================================================================
Location: agents/langclaw/

📄 langclaw.py - MAIN ENTRY (2862 bytes)
   Purpose: Langclaw - AI Language Teaching Agent with Chronicle Integration
   Functions: process_command, main

📁 commands/ - 7 commands
   📄 commands.py - /commands
      Command handlers for Langclaw
      Functions: __init__, translate, get_languages, get_stats
   📄 conversation.py - /conversation
      Functions: run
   📄 lesson.py - /lesson
      Functions: run
   📄 practice.py - /practice
      Functions: run
   📄 speak.py - /speak
      Functions: run
   📄 teach.py - /teach
      You are an interactive language teacher for {language}. 
      Functions: run
   📄 vocab.py - /vocab
      Functions: run

📁 core/ - 7 modules
   📄 agent.py (1355 bytes)
      Langclaw Agent - Standalone
      Functions: __init__, get_available_languages, get_language_name, translate, speak, get_stats
      Classes: LangclawAgent
   📄 lesson_engine.py (1845 bytes)
      Language Lesson Engine
      Functions: __init__, get_lesson, get_conversation, get_practice, get_vocab
      Classes: LessonEngine
   📄 llm_wrapper.py (1207 bytes)
      LLM Wrapper - re-export from project root
   📄 session_manager.py (980 bytes)
      Session Manager - Tracks translation history and statistics
      Functions: __init__, add_query, get_stats, get_recent
      Classes: SessionManager
   📄 stt_engine.py (2251 bytes)
      Speech-to-Text Engine for Langclaw
      Functions: __init__, listen, _listen_windows, _listen_mac, _listen_linux
      Classes: STTEngine
   📄 translator.py (1507 bytes)
      Core Translator - Main translation logic
      Functions: __init__, get_language_name, translate
      Classes: Translator
   📄 tts_engine.py (2208 bytes)
      Text-to-Speech Engine for Langclaw
      Functions: __init__, speak, _speak_windows, _speak_mac, _speak_linux, save_audio
      Classes: TTSEngine

📁 providers/ - 2 providers
   📄 api_provider.py
      API Provider for Langclaw - Using Shared API
   📄 webclaw_provider.py
      Webclaw Provider - Fetches live translation content from web references

📁 cli/ - 1 files
   📄 interface.py

📁 references/ - 10 files (4 KB)

📁 utils/ - 2 files (763 bytes)


================================================================================
🤖 AGENT: langclaw_backup
================================================================================
Location: agents/langclaw_backup/

❌ langclaw_backup.py - MISSING

📁 commands/ - 1 commands
   📄 system.py - /system
      Functions: test_command, help_command, quit_command

📁 core/ - 1 modules
   📄 data.py (181 bytes)
      Functions: get_data_path

📁 cli/ - 1 files
   📄 parser.py

📁 utils/ - 2 files (343 bytes)


================================================================================
🤖 AGENT: lawclaw
================================================================================
Location: agents/lawclaw/

📄 lawclaw.py - MAIN ENTRY (3009 bytes)
   Purpose: LawClaw - Pure Logic Legal Agent with Dynamic Command Loading
   Functions: parse_command, banner, __init__, print_welcome, run, show_stats
   Classes: Display, LawClaw

📁 commands/ - 19 commands
   📄 analyze.py - /analyze
      analyze command - Analyze legal text
      Functions: run
   📄 ask.py - /ask
      ask command - AI legal Q&A via WebClaw
      Functions: run
   📄 brief.py - /brief
      brief command - Find briefs
      Functions: run
   📄 browse.py - /browse
      browse command - Browse state courts
      Functions: run
   📄 cite.py - /cite
      cite command - Parse legal citations
      Functions: run
   📄 court.py - /court
      court command - County court info with LLM (supports stock + obliterated)
      Functions: run
   📄 docket.py - /docket
      docket command - Search dockets
      Functions: run
   📄 federal.py - /federal
      federal command - Federal courts
      Functions: run
   📄 judge.py - /judge
      judge command - Judge information
      Functions: run
   📄 jurisdiction.py - /jurisdiction
      jurisdiction command - Jurisdiction info
      Functions: run
   📄 law.py - /law
      law command - Legal research
      Functions: run
   📄 list.py - /list
      list command - List available resources
      Functions: run
   📄 oral.py - /oral
      oral command - Oral arguments
      Functions: run
   📄 precedent.py - /precedent
      precedent command - Find precedents
      Functions: run
   📄 search.py - /search
      search command - Search legal references via WebClaw
      Functions: run
   📄 state.py - /state
      state command - State courts
      Functions: run
   📄 stats.py - /stats
      stats command - Show statistics
      Functions: run
   📄 statute.py - /statute
      statute command - Look up statutes
      Functions: run
   📄 summarize.py - /summarize
      summarize command - Summarize cases
      Functions: run
   📄 __init__.py - Dynamic command registry

📁 core/ - 6 modules
   📄 agent.py (385 bytes)
      Lawclaw Agent - Standalone
      Functions: __init__, search, get_stats
      Classes: LawclawAgent
   📄 api.py (1815 bytes)
      API - AI and web requests
      Functions: ask_ai, _ask_openrouter, _ask_ollama, fetch_url
   📄 app.py (4509 bytes)
      Main application - routes commands to modules
      Functions: __init__, run, _help, _stats, _list, _search, _browse, _court, _ask, _fetch
      Classes: LawClaw
   📄 config.py (610 bytes)
      Configuration - paths and API keys
      Functions: get_api_key
   📄 data.py (1970 bytes)
      Data access - search, states, counties
      Functions: search_local, get_states, get_state_info, get_county_info
   📄 display.py (1136 bytes)
      Display utilities
      Functions: banner, categories, commands
      Classes: Display

📁 cli/ - 1 files
   📄 parser.py

📁 utils/ - 5 files (7 KB)


================================================================================
🤖 AGENT: liberateclaw
================================================================================
Location: agents/liberateclaw/

📄 liberateclaw.py - MAIN ENTRY (4299 bytes)
   Purpose: Liberateclaw - Model Liberation Agent (Modular)
   Functions: process_command, get_help, main

📁 commands/ - 6 commands
   📄 liberate.py - /liberate
      Liberate command - Local model liberation via Ollama
      Functions: run_liberate
   📄 liberated.py - /liberated
      List liberated models
      Functions: list_liberated
   📄 models.py - /models
      Models command - List available models
      Functions: list_models
   📄 obliterate.py - /obliterate
      Obliterate command - Advanced model liberation using OBLITERATUS
      Functions: run_obliterate
   📄 remote.py - /remote
      Remote command - Liberate models on remote GPU servers
      Functions: show_remote_help, remote_liberate
   📄 use.py - /use
      Use command - Run inference with liberated models
      Functions: run_use

📁 core/ - 0 modules

📁 exports/ - 7 files (3 KB)

📁 utils/ - 1 files (0 bytes)

📁 data/ - 1 files (109 bytes)


================================================================================
🤖 AGENT: llmclaw
================================================================================
Location: agents/llmclaw/

📄 llmclaw.py - MAIN ENTRY (274 bytes)
   Purpose: LLMClaw - Model Management Agent for Clawpack

📁 commands/ - 4 commands
   📄 list.py - /list
      list - List available models
      Functions: run
   📄 normal.py - /normal
      normal - Show normal models menu
      Functions: run
   📄 obliterated.py - /obliterated
      obliterated - Show obliterated models menu
      Functions: run
   📄 use.py - /use
      use - Switch active model
      Functions: run
   📄 __init__.py - Dynamic command registry

📁 core/ - 2 modules
   📄 state.py (1093 bytes)
      Model state management - with global sync
      Functions: get_active_model, set_active_model, get_model_paths
   📄 sync.py (2387 bytes)
      LLMClaw Integration - Updates global state with selected model
      Functions: sync_model_to_global_state, update_working_llms

📁 providers/ - 2 providers
   📄 obliterated.py
      Obliterated models provider
   📄 stock.py
      Stock models provider (Ollama)

📁 cli/ - 1 files
   📄 interface.py

📁 utils/ - 1 files (0 bytes)


================================================================================
🤖 AGENT: mathematicaclaw
================================================================================
Location: agents/mathematicaclaw/

📄 mathematicaclaw.py - MAIN ENTRY (1848 bytes)
   Purpose: MathematicaClaw - Mathematics and Visualization
   Functions: __init__, _init_visualizer, handle, visualize, _help, main
   Classes: MathematicaClawAgent

📁 commands/ - 8 commands
   📄 add.py - /add
      Add numbers
      Functions: run
   📄 algebra.py - /algebra
      Algebra commands for mathematicaclaw
      Functions: solve, simplify, factor, expand, evaluate
   📄 arithmetic.py - /arithmetic
      Arithmetic commands for mathematicaclaw
      Functions: add, subtract, multiply, divide, power, sqrt, percent
   📄 calculus.py - /calculus
      Calculus commands for mathematicaclaw
      Functions: derivative, integral, limit
   📄 math.py - /math
      Mathematics commands with chronicle learning
      Functions: get_chronicle, get_llm, solve, explain, search, stats, handle_solve, handle_explain, handle_search, handle_stats
   📄 plot.py - /plot
      Plot a mathematical function
      Functions: run
   📄 solve.py - /solve
      Solve equation
      Functions: run
   📄 system.py - /system
      Functions: test_command, help_command, quit_command

📁 core/ - 5 modules
   📄 agent.py (2300 bytes)
      Mathematicaclaw Agent - Fixed to use the dictionary
      Functions: __init__, _result, evaluate, solve, derivative, integral, simplify, factor, expand, limit, series, matrix, system, stats, get_stats
      Classes: MathematicaclawAgent
   📄 data.py (188 bytes)
      Functions: get_data_path
   📄 engine.py (7761 bytes)
      Mathematicaclaw Computation Engine
      Functions: __init__, solve_equation, derivative, integral, simplify, factor, expand, matrix_operations, statistics, evaluate, solve_system, limit, series
      Classes: MathEngine
   📄 math_engine.py (4354 bytes)
      Mathematicaclaw Math Engine - Pure sympy/numpy/matplotlib functions
      Functions: __init__, solve_equation, derivative, integral, limit, simplify, factor, expand, plot
      Classes: MathEngine
   📄 session_manager.py (795 bytes)
      Session Manager - Tracks queries and statistics
      Functions: __init__, add_query, get_stats
      Classes: SessionManager

📁 cli/ - 3 files
   📄 interface.py
   📄 main.py
   📄 parser.py

📁 utils/ - 2 files (343 bytes)

📁 handlers/ - 12 files (16 KB)

📁 data/ - 1 files (113 bytes)


================================================================================
🤖 AGENT: mediclaw
================================================================================
Location: agents/mediclaw/

📄 mediclaw.py - MAIN ENTRY (1301 bytes)
   Purpose: Mediclaw - Medical Information Agent
   Functions: process_command, main

📁 commands/ - 13 commands
   📄 base.py - /base
      Base Command
      Functions: name, execute
   📄 clinical_commands.py - /clinical_commands
      Clinical Command Handlers
      Functions: __init__, handle_procedure, handle_prognosis, handle_referral
   📄 commands.py - /commands
      Command handlers for Mediclaw - Enhanced
      Functions: __init__, handle_sources, handle_stats, handle_research, handle_diagnose, handle_treatment, handle_medications, handle_interactions, handle_emergency, handle_procedures, handle_prevention, handle_pediatrics, handle_geriatrics, handle_lab_tests, handle_diet, handle_exercise, handle_prognosis, handle_referral, handle_natural_remedies, handle_coding, handle_warnings, handle_clear
   📄 core_commands.py - /core_commands
      Core Command Handlers
      Functions: __init__, handle_sources, handle_stats, handle_research, handle_diagnose, handle_treatment
   📄 diagnose.py - /diagnose
      Diagnose Command
      Functions: name, execute
   📄 lifestyle_commands.py - /lifestyle_commands
      Lifestyle Command Handlers
      Functions: __init__, handle_prevention, handle_diet, handle_exercise, handle_natural
   📄 med.py - /med
      Medical research using LLM
      Functions: run
   📄 pharma_commands.py - /pharma_commands
      Pharmacology Command Handlers
      Functions: __init__, handle_medications, handle_interactions, handle_warnings
   📄 research.py - /research
      Medical research using chronicle index
      Functions: run
   📄 sources.py - /sources
      Sources Command
      Functions: name, execute
   📄 specialty_commands.py - /specialty_commands
      Specialty Command Handlers
      Functions: __init__, handle_pediatrics, handle_geriatrics, handle_lab, handle_icd
   📄 stats.py - /stats
      Stats Command
      Functions: name, execute
   📄 treatment.py - /treatment
      Treatment Command
      Functions: name, execute

📁 core/ - 2 modules
   📄 agent.py (387 bytes)
      Mediclaw Agent - Standalone
      Functions: __init__, search, get_stats
      Classes: MediclawAgent
   📄 engine.py (1281 bytes)
      Core Medical Engine
      Functions: __init__, generate, research, diagnose, treatment, list_sources
      Classes: MedicalEngine

📁 providers/ - 9 providers
   📄 anthropic.py
      Anthropic API Provider
   📄 api_provider.py
      API Provider - AI Capability
   📄 base.py
      Base provider interface
   📄 ollama.py
      Ollama Local Provider
   📄 ollama_provider.py
      Ollama local provider
   📄 openrouter.py
      OpenRouter API Provider
   📄 openrouter_provider.py
      OpenRouter API provider
   📄 providers.py
      Providers - API and Webclaw
   📄 webclaw_provider.py
      Webclaw Provider

📁 cli/ - 1 files
   📄 interface.py

📁 docs/ - 1 files (11 KB)

📁 utils/ - 2 files (343 bytes)


================================================================================
🤖 AGENT: plotclaw
================================================================================
Location: agents/plotclaw/

📄 plotclaw.py - MAIN ENTRY (1743 bytes)
   Purpose: plotclaw - Modular Agent
   Functions: __init__, handle, main, _search_chronicle
   Classes: plotclawAgent

📁 commands/ - 3 commands
   📄 bar.py - bar
      Bar command - Creates real bar charts
      Functions: run
   📄 pie.py - pie
      Pie command - Creates pie charts
      Functions: run
   📄 plot.py - plot
      Plot command - Line charts
      Functions: run

📁 core/ - 1 modules
   📄 agent.py (1557 bytes)
      plotclaw Core Logic
      Functions: process, process_command, main, _help
      Classes: plotclawCore

📁 exports/ - 4 files (175 KB)

📁 utils/ - 1 files (32 bytes)


================================================================================
🤖 AGENT: rustypycraw
================================================================================
Location: agents/rustypycraw/

📄 rustypycraw.py - MAIN ENTRY (1059 bytes)
   Purpose: RustyPyCraw - Simple working version
   Functions: __init__, handle, scan, search, main
   Classes: RustyPyCraw

📁 modules/ - 11 files (865 bytes)


================================================================================
🤖 AGENT: TXclaw
================================================================================
Location: agents/TXclaw/

📄 TXclaw.py - MAIN ENTRY (1168 bytes)
   Purpose: TXClaw - Blockchain Development Assistant
   Functions: __init__, handle, process, _process, main
   Classes: TXClaw

📁 commands/ - 0 commands

📁 core/ - 2 modules
   📄 agent.py (568 bytes)
      TXclaw Agent - Standalone
      Functions: __init__, get_balance, send_transaction, get_stats
      Classes: TXclawAgent
   📄 commands.py (3660 bytes)
      TX Blockchain Specific Commands
      Functions: __init__, transaction, block, address, token, validator, staking, gas, mempool, smart_contract, ecosystem, governance, network_stats
      Classes: TXCommands

📁 providers/ - 1 providers
   📄 api_provider.py
      API Provider for TXclaw - Handles LLM calls

📁 cli/ - 2 files
   📄 commands_list.py
   📄 interface.py

📁 references/ - 1 files (2 KB)

📁 utils/ - 1 files (2 KB)

📁 modules/ - 13 files (2 KB)


================================================================================
🤖 AGENT: webclaw
================================================================================
Location: agents/webclaw/

📄 webclaw.py - MAIN ENTRY (2731 bytes)
   Purpose: Webclaw - Fetches content from URLs with citations
   Functions: __init__, fetch_with_citation, process_command, main
   Classes: Webclaw

📁 commands/ - 12 commands
   📄 browse.py - /browse
      Browse web/cloud categories
      Functions: browse_command
   📄 cache_stats.py - /cache
      Cache statistics and management command
      Functions: cache_stats_command
   📄 chronicle.py - /chronicle
      Chronicle commands - URL context recovery and timeline
      Functions: run
   📄 fetch.py - /fetch
      Fetch and analyze URL content with caching, rate limiting, and content extractio
      Functions: fetch_command
   📄 help.py - /help
      Help command - show all WebClaw commands
      Functions: help_command
   📄 list.py - /list
      List available web/cloud categories
      Functions: list_command
   📄 llm.py - /llm
      LLM command - AI with shared memory
      Functions: llm_command
   📄 quit.py - /quit
      Quit command - Exit WebClaw
      Functions: quit_command
   📄 recall.py - /recall
      Recall command - Recall from webclaw memory
      Functions: recall_command
   📄 share.py - /share
      Share command - Query all agents' knowledge
      Functions: share_command
   📄 stats.py - /stats
      WebClaw statistics - shows reference database info
      Functions: stats_command
   📄 system.py - /system
      System command - System information
      Functions: system_command

📁 core/ - 9 modules
   📄 agent.py (2161 bytes)
      Webclaw Agent - Web crawling and references
      Functions: __init__, _register_tools, search_references_tool, fetch_url, list_references
      Classes: WebclawAgent
   📄 api.py (3420 bytes)
      WebClaw API - OpenRouter + Ollama fallback
      Functions: __init__, ask, fetch_url, get_api
      Classes: WebAPI
   📄 cache.py (4360 bytes)
      Caching system for WebClaw - store fetched content to avoid repeated requests
      Functions: __init__, _init_db, _get_url_hash, get, set, _clean_old_entries, clear, stats, get_cache
      Classes: WebCache
   📄 chronicle_ledger.py (6613 bytes)
      Chronicle Ledger System - Immutable URL tracking with context preservation
      Functions: to_dict, __init__, _load_ledger, _save_ledger, record_fetch, recover_by_context, get_timeline, get_stats, get_chronicle, create_timeline, add_sourced_entry, get_structured_context, create_timeline, get_sourced_context
      Classes: ChronicleCard, ChronicleLedger
   📄 config.py (899 bytes)
      WebClaw configuration
      Functions: load_env, get_config
   📄 data.py (263 bytes)
      Functions: get_data_path
   📄 pacer.py (3312 bytes)
      PACER (Public Access to Court Electronic Records) integration
      Functions: is_pacer_url, extract_case_number, get_pacer_base_url, format_pacer_docket, extract_judge_name, extract_filing_date, get_pacer
      Classes: PacerHandler
   📄 rate_limiter.py (4493 bytes)
      Rate limiting and robots.txt handling
      Functions: __init__, can_request, wait_if_needed, __init__, get_rules, is_allowed, get_crawl_delay, get_rate_limiter, get_robots_parser
      Classes: RateLimiter, RobotsTxtParser
   📄 shared_memory.py (3722 bytes)
      Shared memory for cross-agent learning
      Functions: __init__, _init_table, save, recall, query_all_agents, get_stats
      Classes: SharedMemory

📁 providers/ - 1 providers
   📄 webclaw_provider.py
      Webclaw Provider - Fast bitmap search for references

📁 cli/ - 1 files
   📄 parser.py

📁 references/ - 32182 files (18.4 MB)

📁 cache/ - 2 files (1.0 MB)

📁 docs/ - 1 files (23 KB)

📁 utils/ - 7 files (7 KB)
