# LiberateClaw — Model Liberation

## What It Does
Manages obliterated (liberated) AI models — models that have been freed from
censorship and refusal mechanisms through ablation. Lists, switches between,
and provides information about both standard and liberated models.

## Commands

| Command | Description |
|---------|-------------|
| `/models` | List all 17 models (obliterated + standard) |
| `/liberated` | List obliterated models only |
| `/obliterated` | Alias for /liberated |
| `/obliterate <model>` | Liberate a model via ablation |
| `/use <model>` | Switch active model |
| `/delegate <agent> <task>` | Send task to any agent |
| `/stats` | Agent statistics |

## Quick Start

/models
/liberated
/use deepseek-r1:8b

text

## Architecture
- **Models file**: `models/working_llms.json`
- **Active model**: `models/active_model.json`
- **LLMClaw**: Model orchestration handled by llmclaw
- **Constitutional**: 23-system boundary, 36 shared systems
