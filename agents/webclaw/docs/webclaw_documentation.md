powershell

cd C:\\Users\\greg\\dev\\clawpack\_v2\\agents\\webclaw



\# Create docs folder if it doesn't exist

New-Item -ItemType Directory -Force -Path docs | Out-Null



\# Create README.md

@'

\# 🌐 WebClaw - Web Research \& Security Agent



WebClaw is a modular web research and security analysis agent that provides web fetching, content extraction, caching, rate limiting, and AI-powered research capabilities for the Clawpack ecosystem.



\## 📋 Table of Contents



\- \[Overview](#overview)

\- \[Features](#features)

\- \[Installation](#installation)

\- \[Configuration](#configuration)

\- \[Commands](#commands)

\- \[Architecture](#architecture)

\- \[Caching System](#caching-system)

\- \[Content Extraction](#content-extraction)

\- \[Rate Limiting](#rate-limiting)

\- \[PACER Integration](#pacer-integration)

\- \[AI Integration](#ai-integration)

\- \[Cross-Agent Learning](#cross-agent-learning)

\- \[API Reference](#api-reference)

\- \[Troubleshooting](#troubleshooting)



\## Overview



WebClaw serves as the central web service layer for all Clawpack agents (LawClaw, Mediclaw, Polyclaw, etc.). It provides:



\- \*\*Web fetching\*\* with smart caching

\- \*\*Content extraction\*\* (HTML stripping, text cleaning)

\- \*\*Rate limiting\*\* respecting robots.txt

\- \*\*PACER court document detection\*\*

\- \*\*Legal citation extraction\*\*

\- \*\*AI-powered research\*\* via OpenRouter/Ollama

\- \*\*Cross-agent knowledge sharing\*\*



\## Features



\### ✅ Implemented



| Feature | Description | Status |

|---------|-------------|--------|

| URL Fetching | HTTP/HTTPS requests with custom headers | ✅ |

| Smart Caching | SQLite-based cache with 24-hour TTL | ✅ |

| Content Extraction | Strips HTML, removes scripts/styles | ✅ |

| Rate Limiting | Respects robots.txt crawl delays | ✅ |

| PACER Detection | Identifies federal court dockets | ✅ |

| Legal Citations | Extracts case citations from text | ✅ |

| AI Questions | OpenRouter API + Ollama fallback | ✅ |

| Cache Management | View stats and clear cache | ✅ |

| Cross-Agent Memory | SQLite shared database | ✅ |



\### 🚧 Planned



| Feature | Status |

|---------|--------|

| Web Scraping Framework | 📅 Planned |

| API Rate Limiting | 📅 Planned |

| User-Agent Rotation | 📅 Planned |

| Proxy Support | 📅 Planned |



\## Installation



\### Prerequisites



\- Python 3.12+

\- requests library

\- sqlite3 (built-in)

\- Optional: Ollama for local LLM



\### Setup



```bash

\# Clone the repository

git clone https://github.com/greg-gzillion/clawpack.git

cd clawpack/agents/webclaw



\# Install dependencies

pip install requests



\# Set up API key (optional, for OpenRouter)

echo "OPENROUTER\_API\_KEY=your-key-here" > .env



\# Run WebClaw

python webclaw.py

Configuration

Environment Variables (.env)

Create a .env file in the webclaw root directory:



env

OPENROUTER\_API\_KEY=sk-or-v1-your-api-key-here

Configuration File (core/config.py)

python

ROOT\_DIR = Path(r"C:\\Users\\greg\\dev\\clawpack\_v2")

WEB\_REFS = Path(\_\_file\_\_).parent.parent / "references"

SHARED\_DB = Path.home() / ".claw\_memory" / "shared\_memory.db"

Commands

Core Commands

Command	Description	Example

/fetch <url>	Fetch and extract web content	/fetch https://www.uscourts.gov

/llm <question>	Ask AI a question	/llm What is habeas corpus?

/cache	Show cache statistics	/cache

/cache clear	Clear entire cache	/cache clear

/stats	System statistics	/stats

/list	List categories	/list

/search <term>	Search references	/search bankruptcy

/browse <category>	Browse category	/browse courts

/share <query>	Query all agents	/share "federal courts"

/recall <query>	Recall from memory	/recall "Supreme Court"

/help	Show help menu	/help

/quit	Exit WebClaw	/quit

Natural Language Queries

WebClaw also accepts natural language questions without the /llm prefix:



text

What is the federal court system?

How does PACER work?

Explain the 1st Amendment

Architecture

Directory Structure

text

webclaw/

├── webclaw.py              # Entry point

├── core/

│   ├── \_\_init\_\_.py

│   ├── api.py              # OpenRouter + Ollama

│   ├── cache.py            # SQLite caching

│   ├── config.py           # Configuration

│   ├── pacer.py            # PACER integration

│   ├── rate\_limiter.py     # robots.txt, rate limiting

│   └── shared\_memory.py    # Cross-agent database

├── commands/

│   ├── \_\_init\_\_.py

│   ├── fetch.py            # Fetch command

│   ├── cache\_stats.py      # Cache management

│   ├── llm.py              # AI questions

│   ├── stats.py            # Statistics

│   ├── list.py             # List categories

│   ├── search.py           # Search references

│   ├── browse.py           # Browse categories

│   ├── share.py            # Cross-agent query

│   ├── recall.py           # Memory recall

│   ├── help.py             # Help menu

│   └── quit.py             # Exit

├── utils/

│   └── content\_parser.py   # HTML extraction

├── references/             # Reference data

├── cache/                  # Cache database (auto-created)

└── docs/                   # Documentation

Data Flow

text

User Input → CLI Parser → Command Handler

&#x20;                             ↓

&#x20;                       ┌─────┴─────┐

&#x20;                       ↓           ↓

&#x20;                   Fetch URL    AI Query

&#x20;                       ↓           ↓

&#x20;                  Check Cache   OpenRouter

&#x20;                       ↓           ↓

&#x20;                   Fetch/Store    Ollama

&#x20;                       ↓           ↓

&#x20;                  Extract Text    Response

&#x20;                       ↓           ↓

&#x20;                   Display Result ←┘

Caching System

Overview

WebClaw uses a SQLite-based cache with Time-To-Live (TTL) to avoid redundant web requests.



Cache Features

24-hour TTL by default



Automatic expiration of old entries



Hit count tracking for analytics



Manual cache clearing with /cache clear



Cache Database Schema

sql

CREATE TABLE cache (

&#x20;   url TEXT PRIMARY KEY,

&#x20;   content TEXT,

&#x20;   content\_type TEXT,

&#x20;   size INTEGER,

&#x20;   fetched\_at REAL,

&#x20;   expires\_at REAL,

&#x20;   hit\_count INTEGER DEFAULT 1

);

Cache Commands

bash

/cache              # Show statistics

/cache clear        # Clear entire cache

Cache Statistics Example

text

📦 CACHE STATISTICS

==================================================

Entries: 1

Total hits: 2

Average hits per entry: 2.0

==================================================

Content Extraction

Features

The content extractor (utils/content\_parser.py) provides:



HTML tag removal - Strips all HTML tags



Script/style removal - Removes JavaScript and CSS



Entity decoding - Converts HTML entities to text



Whitespace normalization - Collapses multiple spaces



Length limiting - Configurable max length



Legal citation extraction - Finds case citations



Link extraction - Extracts and normalizes URLs



Legal Citation Patterns

The extractor recognizes common legal citation formats:



Citation Type	Pattern	Example

Supreme Court	\\d+\\s+U\\.?S\\.?\\s+\\d+	410 U.S. 113

Federal Reporter	\\d+\\s+F\\.?\\d\*\\s+\\d+	123 F.3d 456

Federal Supplement	\\d+\\s+F\\.\\s+Supp\\.?\\s+\\d+	456 F. Supp. 2d 789

Supreme Court Reporter	\\d+\\s+S\\.?\\s+Ct\\.?\\s+\\d+	123 S. Ct. 456

US Code	\\d+\\s+U\\.?\\s+S\\.?\\s+C\\.?\\s+§\\s\*\\d+	11 U.S.C. § 362

Usage Example

python

from utils.content\_parser import get\_extractor



extractor = get\_extractor()

clean\_text = extractor.strip\_html(html\_content, max\_length=5000)

citations = extractor.extract\_legal\_citations(clean\_text)

links = extractor.extract\_links(html\_content, base\_url)

Rate Limiting

robots.txt Support

WebClaw respects robots.txt directives:



Disallow rules - Prevents crawling of restricted paths



Allow overrides - Handles allow/disallow conflicts



Crawl delay - Enforces specified delays between requests



Rate Limiter

python

from core.rate\_limiter import get\_rate\_limiter, get\_robots\_parser



rate\_limiter = get\_rate\_limiter()

rate\_limiter.wait\_if\_needed(url)



robots = get\_robots\_parser()

if robots.is\_allowed(url):

&#x20;   # Proceed with fetch

Default Settings

Default crawl delay: 1 second



User agent: WebClaw (configurable)



Cache duration: 24 hours



PACER Integration

Overview

PACER (Public Access to Court Electronic Records) integration helps identify and parse federal court documents.



Features

URL detection - Identifies PACER and court URLs



Case number extraction - Parses case numbers from text



Judge name extraction - Finds presiding judges



Filing date extraction - Identifies filing dates



Docket URL formatting - Generates CourtListener URLs



Supported Courts

Court Code	Name

SCOTUS	Supreme Court

1CA-11CA	Circuit Courts of Appeals

FED	Federal Circuit

DC	District of Columbia

Usage Example

python

from core.pacer import get\_pacer



pacer = get\_pacer()

if pacer.is\_pacer\_url(url):

&#x20;   case\_number = pacer.extract\_case\_number(content)

&#x20;   judge = pacer.extract\_judge\_name(content)

&#x20;   filing\_date = pacer.extract\_filing\_date(content)

AI Integration

OpenRouter API

WebClaw uses OpenRouter for AI-powered legal research:



Model: deepseek/deepseek-chat



Temperature: 0.3 (low for factual accuracy)



Max tokens: 2000



Timeout: 60 seconds



Ollama Fallback

If OpenRouter is unavailable, WebClaw falls back to local Ollama:



Model: deepseek-coder:6.7b



Timeout: 120 seconds



Environment Setup

bash

\# Set OpenRouter API key

export OPENROUTER\_API\_KEY="sk-or-v1-your-key"



\# Or use .env file

echo "OPENROUTER\_API\_KEY=sk-or-v1-your-key" > .env

Usage

bash

\# Using /llm command

/llm What is the federal court system?



\# Natural language

What is the federal court system?

Cross-Agent Learning

Shared Memory Database

WebClaw uses a shared SQLite database at \~/.claw\_memory/shared\_memory.db for cross-agent knowledge sharing.



Database Schema

sql

\-- Web research cache

CREATE TABLE web\_research (

&#x20;   id INTEGER PRIMARY KEY,

&#x20;   query TEXT UNIQUE,

&#x20;   content\_summary TEXT,

&#x20;   source\_agent TEXT,

&#x20;   timestamp TEXT,

&#x20;   category TEXT

);



\-- Shared knowledge

CREATE TABLE shared\_knowledge (

&#x20;   id INTEGER PRIMARY KEY,

&#x20;   topic TEXT UNIQUE,

&#x20;   content TEXT,

&#x20;   source TEXT,

&#x20;   confidence REAL

);

Commands

Command	Description

/share <query>	Query all agents for knowledge

/recall <query>	Recall from shared memory

API Reference

Core Modules

core/cache.py

python

class WebCache:

&#x20;   def get(url: str, max\_age\_hours: int = 24) -> Optional\[Dict]

&#x20;   def set(url: str, content: str, content\_type: str, ttl\_hours: int = 24)

&#x20;   def clear()

&#x20;   def stats() -> Dict

core/api.py

python

class WebAPI:

&#x20;   def ask(question: str, context: str = "", timeout: int = 30) -> str

&#x20;   def fetch\_url(url: str, timeout: int = 15) -> Optional\[str]

utils/content\_parser.py

python

class ContentExtractor:

&#x20;   def strip\_html(html\_content: str, max\_length: int = 5000) -> str

&#x20;   def extract\_links(html\_content: str, base\_url: str = "") -> list

&#x20;   def extract\_legal\_citations(text: str) -> list

&#x20;   def is\_legal\_site(url: str) -> bool

Command Interface

Each command module exports:



python

name = "/command\_name"      # Command string

run = command\_function      # Function to execute

Troubleshooting

Common Issues

DNS Resolution Failed

text

❌ Cannot resolve domain: www.example.com

Solution: Check internet connection or try a different URL.



403 Forbidden

text

❌ Failed to fetch (status 403)

Solution: The website blocks automated requests. Try using /llm instead.



API Key Not Working

text

⚠️ API error: 401

Solution: Check your OpenRouter API key in .env file.



Ollama Not Found

text

🦙 Using Ollama fallback...

Error: \[Errno 2] No such file or directory

Solution: Install Ollama from https://ollama.com or set OpenRouter API key.



Debugging

Enable verbose logging by modifying webclaw.py:



python

import logging

logging.basicConfig(level=logging.DEBUG)

Logs

WebClaw logs to console only. For persistent logging, redirect output:



bash

python webclaw.py > webclaw.log 2>\&1

License

MIT License - See LICENSE file for details



Contributing

Fork the repository



Create a feature branch



Make your changes



Submit a pull request



Support

Issues: GitHub Issues



Documentation: /docs folder



Examples: See command examples above



Built with 🦞 by the Clawpack Team

'@ | Out-File -FilePath docs/README.md -Encoding utf8 -Force



Write-Host "✅ Created docs/README.md" -ForegroundColor Green



text



Now create additional documentation files:



```powershell

\# Create API documentation

@'

\# WebClaw API Documentation



\## Core API



\### Cache Module (`core/cache.py`)



\#### `WebCache` Class



SQLite-based cache for web content with TTL.



```python

from core.cache import get\_cache



cache = get\_cache()



\# Get cached content

cached = cache.get("https://example.com")

if cached:

&#x20;   print(f"Hit count: {cached\['hit\_count']}")

&#x20;   print(f"Content: {cached\['content']\[:100]}")



\# Store content

cache.set("https://example.com", html\_content, "text/html", ttl\_hours=24)



\# Clear cache

cache.clear()



\# Get statistics

stats = cache.stats()

print(f"Entries: {stats\['entries']}")

print(f"Total hits: {stats\['total\_hits']}")

Rate Limiter Module (core/rate\_limiter.py)

RateLimiter Class

Enforces delays between requests to the same domain.



python

from core.rate\_limiter import get\_rate\_limiter



limiter = get\_rate\_limiter()

limiter.wait\_if\_needed("https://example.com")

\# Proceed with request

RobotsTxtParser Class

Parses and respects robots.txt directives.



python

from core.rate\_limiter import get\_robots\_parser



robots = get\_robots\_parser()



\# Check if URL is allowed

if robots.is\_allowed("https://example.com/private/"):

&#x20;   # Proceed



\# Get crawl delay

delay = robots.get\_crawl\_delay("https://example.com")

PACER Module (core/pacer.py)

PacerHandler Class

Detects and parses PACER court documents.



python

from core.pacer import get\_pacer



pacer = get\_pacer()



\# Check if URL is from PACER

if pacer.is\_pacer\_url("https://ecf.dcd.uscourts.gov"):

&#x20;   # Extract case information

&#x20;   case\_num = pacer.extract\_case\_number(text)

&#x20;   judge = pacer.extract\_judge\_name(text)

&#x20;   filing\_date = pacer.extract\_filing\_date(text)

Content Extractor (utils/content\_parser.py)

ContentExtractor Class

Extracts clean text and legal citations from HTML.



python

from utils.content\_parser import get\_extractor



extractor = get\_extractor()



\# Strip HTML

clean\_text = extractor.strip\_html(html, max\_length=5000)



\# Extract links

links = extractor.extract\_links(html, base\_url="https://example.com")



\# Extract legal citations

citations = extractor.extract\_legal\_citations(clean\_text)



\# Check if legal site

is\_legal = extractor.is\_legal\_site("https://www.uscourts.gov")

API Module (core/api.py)

WebAPI Class

Handles AI queries with OpenRouter and Ollama fallback.



python

from core.api import get\_api



api = get\_api()



\# Ask a question

response = api.ask("What is habeas corpus?")

print(response)



\# Fetch URL

content = api.fetch\_url("https://example.com")

Command Interface

Each command module must export:



python

name = "/command\_name"  # Command string (e.g., "/fetch")

run = function\_name     # Function to execute

Command functions receive an optional args parameter:



python

def my\_command(args=None):

&#x20;   """Handle command"""

&#x20;   if args:

&#x20;       print(f"Arguments: {args}")

&#x20;   # Command logic

Shared Memory Database

The shared database is located at \~/.claw\_memory/shared\_memory.db.



Tables

web\_research

Stores web research results for cross-agent learning.



sql

CREATE TABLE web\_research (

&#x20;   id INTEGER PRIMARY KEY,

&#x20;   query TEXT UNIQUE,

&#x20;   content\_summary TEXT,

&#x20;   source\_agent TEXT,

&#x20;   timestamp TEXT,

&#x20;   category TEXT

);

shared\_knowledge

Stores general knowledge shared across agents.



sql

CREATE TABLE shared\_knowledge (

&#x20;   id INTEGER PRIMARY KEY,

&#x20;   topic TEXT UNIQUE,

&#x20;   content TEXT,

&#x20;   source TEXT,

&#x20;   confidence REAL

);

Environment Variables

Variable	Description	Required

OPENROUTER\_API\_KEY	API key for OpenRouter AI	No (Ollama fallback)

Return Codes

Command functions can return:



None - Continue running



True - Exit the application (for /quit command)



Error Handling

WebClaw handles errors gracefully:



Network errors → User-friendly messages



DNS failures → Suggestions for resolution



API errors → Fallback to Ollama



Cache errors → Continue without cache

'@ | Out-File -FilePath docs/API.md -Encoding utf8 -Force



Write-Host "✅ Created docs/API.md" -ForegroundColor Green



Create commands documentation

@'



WebClaw Commands Reference

Core Commands

/fetch <url>

Fetches and extracts content from a URL.



Features:



Smart caching (24-hour TTL)



Content extraction (HTML stripping)



Legal citation detection



PACER court document detection



Rate limiting (respects robots.txt)



Examples:



bash

/fetch https://www.uscourts.gov

/fetch https://www.courtlistener.com

/fetch https://www.supremecourt.gov/opinions

Output includes:



HTTP status code



Content type and size



Extracted clean text



Related links



Legal citations (if found)



PACER case info (if applicable)



/llm <question>

Asks AI a question using OpenRouter (with Ollama fallback).



Examples:



bash

/llm What is the federal court system?

/llm Explain the 1st Amendment

/llm How does PACER work?

Natural language also works:



bash

What is habeas corpus?

How many Supreme Court justices are there?

/cache

Shows cache statistics.



Output:



text

📦 CACHE STATISTICS

==================================================

Entries: 1

Total hits: 2

Average hits per entry: 2.0

==================================================

/cache clear

Clears the entire cache.



Example:



bash

/cache clear

Confirmation required before clearing.



/stats

Shows system statistics.



Output includes:



Python version



WebClaw version



Cache status



API configuration



/list

Lists available categories.



Example:



bash

/list

/search <term>

Searches reference data for a term.



Examples:



bash

/search bankruptcy

/search "federal courts"

/search "1st amendment"

/browse <category>

Browses a reference category.



Examples:



bash

/browse courts

/browse cybersecurity

/browse cloud

/share <query>

Queries all agents for knowledge.



Examples:



bash

/share "federal courts"

/share "Supreme Court cases"

/recall <query>

Recalls knowledge from shared memory.



Examples:



bash

/recall "bankruptcy"

/recall "1st amendment"

/help

Shows the help menu with all commands.



/quit

Exits WebClaw.



Command Aliases

Command	Alias

/quit	/exit

Natural Language

WebClaw accepts natural language queries without the /llm prefix:



text

What is the federal court system?

Explain the difference between district and circuit courts.

How do I access PACER?

Command Flow

text

User Input

&#x20;   ↓

Starts with '/'? → Yes → Command handler

&#x20;   ↓                     ↓

No                    Parse command

&#x20;   ↓                     ↓

Natural language    Execute command

&#x20;   ↓                     ↓

AI handler          Display result

Exit Codes

Normal exit: 0



Keyboard interrupt: 130



Error: 1

'@ | Out-File -FilePath docs/COMMANDS.md -Encoding utf8 -Force



Write-Host "✅ Created docs/COMMANDS.md" -ForegroundColor Green



Create CHANGELOG.md

@'



Changelog

\[2.0.0] - 2026-04-08

Added

SQLite-based caching system with 24-hour TTL



Content extraction with HTML stripping



Legal citation detection (supports SCOTUS, Federal Reporter, US Code)



PACER court document detection and parsing



robots.txt parsing and rate limiting



Cache management commands (/cache, /cache clear)



Link extraction from HTML content



Cross-agent shared memory integration



OpenRouter API support with Ollama fallback



Natural language query support



Changed

Improved error handling with user-friendly messages



Enhanced fetch command with multiple User-Agent attempts



Better DNS resolution checking



SSL error fallback



Fixed

Module import issues in command system



Cache hit tracking



robots.txt parsing for complex rules



\[1.0.0] - 2026-04-05

Added

Initial WebClaw release



Basic web fetching



Command-line interface



Reference data browsing



Shared memory database



Basic AI integration

'@ | Out-File -FilePath docs/CHANGELOG.md -Encoding utf8 -Force



Write-Host "✅ Created docs/CHANGELOG.md" -ForegroundColor Green



Verify documentation

Write-Host "`n=== DOCUMENTATION CREATED ===" -ForegroundColor Cyan

Get-ChildItem docs -File | Select-Object Name, Length



Write-Host "`n✅ WebClaw documentation complete!" -ForegroundColor Green

Write-Host "Documentation available at: C:\\Users\\greg\\dev\\clawpack\_v2\\agents\\webclaw\\docs" -ForegroundColor Yellow



text



Now you have complete documentation:



1\. \*\*README.md\*\* - Full user guide with features, installation, commands, architecture

2\. \*\*API.md\*\* - Developer API reference for all modules

3\. \*\*COMMANDS.md\*\* - Detailed command reference with examples

4\. \*\*CHANGELOG.md\*\* - Version history and updates



The documentation covers everything WebClaw can do, with examples and troubleshooting tips.



