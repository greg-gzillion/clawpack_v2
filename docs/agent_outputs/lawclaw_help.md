# lawclaw: /help


============================================================
  LAWCLAW — Legal Research & Document Agent
  Constitutional Reference Implementation
============================================================

CORE LEGAL RESEARCH
  /law [topic]           Search case law via CourtListener + Chronicle
                         Example: /law qualified immunity
  /docket [case|URL]     Fetch docket entries, jury demand, summaries
                         Example: /docket 42 USC 1983
  /cite [citation]       Parse and retrieve legal citations
                         Example: /cite Miranda v Arizona
  /precedent [doctrine]  Track doctrine by circuit with case law
                         Example: /precedent qualified immunity
  /oral [case]           Find oral argument audio and transcripts
                         Example: /oral Dobbs
  /statute [citation]    Look up statutes via law.cornell.edu
                         Example: /statute 42 USC 1983
  /summarize [text|URL]  Summarize legal documents or case URLs
                         Example: /summarize https://courtlistener.com/...

COURT SYSTEMS
  /federal [query]       Federal court info, circuits, SCOTUS, PACER
                         Example: /federal fourth amendment
  /state [code] [county] State and county court lookup
                         Example: /state VA Bedford
  /court [location]      Court info by city and state
                         Example: /court Denver CO

JUDICIAL & CIVIC INTELLIGENCE
  /judge [name]          Federal judge biography + CourtListener
                         Example: /judge Sotomayor
  /jurisdiction [city]   Complete civic profile (3800+ cities)
                         Example: /jurisdiction Daytona Beach FL
  /police [city] [state] Police department lookup
                         Example: /police Miami FL
  /detention [city]      Jail/detention facility lookup
                         Example: /detention Bedford VA
  /library [city]        Public library with legal resources
                         Example: /library Tampa FL
  /hospital [city]       Hospital lookup with GPS coordinates
                         Example: /hospital Daytona Beach FL

DOCUMENT GENERATION & TRANSLATION
  /doc [specs]           Generate legal documents via docuclaw
                         Supports: - plaintiff: - defendant: - case: - grounds:
                         Example: /doc motion to dismiss Miami FL
                                  - plaintiff: John Smith - defendant: ABC Corp
                                  - case: 2024-CV-1234 - grounds: failure to state a claim
  /draft [specs]         Alias for /doc
  /translate [text|doc]  Legal translation with term preservation
                         Example: /translate the contract to German
                                  /translate res judicata
  /correct [fact|URL]    Submit correction via consensus engine
                         Example: /correct salazar-limon url https://oyez.org/...

NAVIGATION & UTILITY
  /list [state]          Browse jurisdiction database
                         Example: /list FL
  /browse [location]     View jurisdiction files, auto-open URLs
                         Example: /browse MA Worcester
  /search [query]        Search local legal reference files
                         Example: /search Miranda
  /analyze [text]        Comprehensive legal text analysis
                         Example: /analyze [paste contract text]
  /ask [question]        AI legal Q&A with Chronicle context
                         Example: /ask what is qualified immunity
  /brief [case]          Generate case brief
                         Example: /brief Miranda v Arizona
  /stats                 System statistics
  /voice                 Voice mode - speak in any language
  /voice                 Voice mode - speak in any language

CROSS-AGENT COMMANDS (routed via capability registry)
  /plot [data]           Route to plotclaw for charts
  /code [specs]          Route to claw_coder for code generation
  /math [expression]     Route to mathematicaclaw
  /design [brief]        Route to designclaw
  /translate [text]      Route to interpretclaw (generic)
  ...any command not listed above routes to the appropriate agent

GETTING STARTED
  1. Try: /jurisdiction [your city] [your state]
  2. Try: /law [any legal topic]
  3. Try: /doc service agreement between [Company A] and [Company B]
  4. Try: /translate the contract to [language]

CONSTITUTIONAL RUNTIME: 23-system boundary active. 100% shared infrastructure.
All commands are memory-wired. Cross-agent delegation via capability registry.
