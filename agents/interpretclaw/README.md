# InterpretClaw — Translation & Language Interpreter

## What It Does
42-language translation with medical/legal term preservation.
Cross-platform text-to-speech. Braille accessibility (opt-in).

## Commands

| Command | Description |
|---------|-------------|
| `/translate <text> to <lang>` | Translate text to any of 42 languages |
| `/detect <text>` | Detect language of text |
| `/languages` | List all 42 supported languages |
| `/braille <text>` | Convert to Braille (opt-in: INTERPRETCLAW_BRAILLE=1) |
| `/speak <text>` | Text-to-speech (Windows SAPI, macOS say, Linux espeak) |
| `/delegate <agent> <task>` | Send task to any agent |
| `/stats` | Agent statistics |

## Quick Start

/translate The defendant has the right to remain silent to Spanish
/translate myocardial infarction to Latin
/detect Bonjour, comment allez-vous?
/speak hello world

text

## Supported Languages (42)
English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese,
Korean, Arabic, Hindi, Dutch, Polish, Swedish, Turkish, Vietnamese, Thai, Greek,
Hebrew, Czech, Danish, Finnish, Norwegian, Romanian, Slovak, Slovenian, Ukrainian,
Catalan, Croatian, Bulgarian, Serbian, Latvian, Lithuanian, Estonian, Hungarian,
Icelandic, Indonesian, Malay, Swahili, Welsh, Zulu, Latin, ASL (gloss)

## Braille (Opt-In)
Set INTERPRETCLAW_BRAILLE=1 to enable Grade 1 and Grade 2 Braille ASCII output.
Best results with reasoning models (deepseek-r1, claude, gpt-4).
