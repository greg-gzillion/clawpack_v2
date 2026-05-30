# DrawClaw — AI Drawing & Art Agent

## What It Does
14 commands for AI-assisted art creation, illustration, and image manipulation.
Uses Sovereign Gateway for prompt generation.

## Commands

| Command | Description |
|---------|-------------|
| `/draw <description>` | Generate drawing prompt |
| `/sketch <description>` | Quick sketch concept |
| `/paint <description>` | Painting-style prompt |
| `/illustrate <description>` | Illustration prompt |
| `/cartoon <description>` | Cartoon-style prompt |
| `/doodle <description>` | Doodle concept |
| `/compose <description>` | Composition design |
| `/style <description>` | Style transfer prompt |
| `/filter <description>` | Filter effect prompt |
| `/canvas <size>` | Canvas setup |
| `/describe <image>` | Describe an image concept |
| `/prompt <description>` | Raw prompt generation |
| `/animate <description>` | Animation concept |
| `/library <city ST>` | Look up local library/resources for art references |
| `/delegate <agent> <task>` | Send task to any agent |
| `/stats` | Agent statistics |

## Quick Start

/draw sunset over mountains with lake reflection
/sketch urban skyline
/cartoon friendly robot
/library Denver CO

text

## Architecture
- **Jurisdiction access**: Library URLs from 3,800+ city files for art references
- **Constitutional**: 23-system boundary, 36 shared systems, circuit breaker protected
