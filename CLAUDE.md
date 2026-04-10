# Clawpack V2 - Knowledge Base

## Tech Stack
- Python 3.12+
- Ollama for local LLMs
- OpenRouter/Anthropic for cloud LLMs
- Matplotlib for plotting

## Design Preferences
- Modular: one agent per directory
- Routes: one file per agent
- Memory: file-based JSON
- No backups in root

## Never Do
- Don't put references in agent folders (use webclaw)
- Don't create backup files in root
- Don't use relative imports without sys.path
