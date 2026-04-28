# DocuClaw

Universal document generator with 21 format exports, translation, and template system.

## Commands

| Command | Description |
|---------|-------------|
| `/create <topic> [format]` | Generate document (default: md) |
| `/letter <topic> [format]` | Generate professional letter |
| `/report <topic> [format]` | Generate structured report |
| `/memo <topic> [format]` | Generate memo |
| `/resume <topic> [format]` | Generate resume/CV |
| `/proposal <topic> [format]` | Generate business proposal |
| `/import <filepath>` | Import file for processing |
| `/export <format> <content>` | Export content in any format |
| `/convert <format> <filepath>` | Convert file between formats |
| `/combine <file1> <file2> ...` | Merge multiple files into one |
| `/translate <lang> <text>` | Translate text via InterpretClaw |
| `/templates [category]` | List available templates |
| `/usetemplate <cat> <name>` | Load a template |
| `/list [format]` | List exported files |
| `/help` | Show commands |
| `/stats` | Show statistics |

## Supported Formats (21)

**Documents**: pdf, docx, rtf, md, html, txt
**Office**: xlsx, pptx
**Data**: json, csv, yaml, toml, xml, ini
**Images**: png, jpg, bmp, gif, tiff, webp
**Vector**: svg
**Archive**: zip

## Quick Start
/create a project kickoff agenda pdf
/letter cover letter for senior developer role
/report quarterly sales analysis md
/proposal mobile app development project pdf
/resume software engineer with 5 years experience

text

## Templates
/templates business
/usetemplate business meeting_agenda

text

Categories: business, education, personal, technical

## File Structure
agents/docuclaw/
├── agent_handler.py # A2A handler
├── templates/
│ ├── business/
│ ├── education/
│ ├── personal/
│ └── technical/
├── modules/
│ ├── ai/
│ ├── export/
│ ├── formatter/
│ ├── media/
│ └── templates/
└── processors/

text

## A2A Integration

```python
self.call_agent("docuclaw", "/create project proposal pdf")
self.call_agent("docuclaw", "/translate fr Welcome")
self.call_agent("docuclaw", "/convert pdf README.md")