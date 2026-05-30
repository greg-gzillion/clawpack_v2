# LangClaw — Language Teaching Agent

## What It Does
Interactive language learning with lessons, vocabulary, conversation practice,
and cross-platform text-to-speech for pronunciation.

## Commands

| Command | Description |
|---------|-------------|
| `/lesson <topic> in <language>` | Generate a language lesson |
| `/vocab <topic> in <language>` | Vocabulary list with examples |
| `/practice <language>` | Conversation practice |
| `/teach <language> <concept>` | Teach a specific language concept |
| `/speak <text>` | Text-to-speech pronunciation |
| `/delegate <agent> <task>` | Send task to any agent |
| `/stats` | Agent statistics |

## Quick Start

/lesson greetings in Spanish
/vocab medical terms in German
/practice French
/teach Japanese particles
/speak hola mundo

text

## Architecture
- **TTS**: Windows SAPI, macOS say, Linux espeak
- **Memory**: All lessons cached for cross-agent recall
- **Constitutional**: 23-system boundary, 36 shared systems
