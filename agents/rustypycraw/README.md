# RustyPyCraw — Code Crawler & Analyzer

## What It Does
AST-based code crawling, pattern detection, and code analysis across projects.

## Commands

| Command | Description |
|---------|-------------|
| `/crawl <path>` | Crawl codebase structure |
| `/scan <pattern>` | Scan for code patterns |
| `/analyze <file>` | Analyze code file |
| `/delegate <agent> <task>` | Send task to any agent |
| `/stats` | Agent statistics |

## Quick Start

/crawl src/
/scan singleton pattern
/analyze main.py

text

## Architecture
- **Delegates to**: claw_coder, crustyclaw, webclaw, dataclaw
- **Constitutional**: 23-system boundary, 36 shared systems, circuit breaker protected
