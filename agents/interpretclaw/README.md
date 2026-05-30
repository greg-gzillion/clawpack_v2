# InterpretClaw — Translation & Language Interpreter

## What It Does
42-language translation with medical/legal term preservation.
Cross-platform text-to-speech. Braille accessibility (opt-in).
Live bidirectional interpreter mode. Speech-to-text input.

## Commands

| Command | Description |
|---------|-------------|
| /interpret | Live bidirectional interpreter — auto-detect, translate, speak |
| /translate <text> to <lang> | Translate text to any of 42 languages |
| /detect <text> | Detect language of text |
| /listen | Microphone input — transcribe and detect language |
| /speak <text> | Text-to-speech output |
| /braille <text> | Convert to Braille Unicode (opt-in) |
| /voice | Toggle system-wide voice mode |
| /languages | List all 42 supported languages |
| /delegate <agent> <task> | Send task to any agent |
| /stats | Agent statistics |

## Interpreter Mode

`ash
interpretclaw> /interpret
[ES -> EN] ¿Cuánto cuesta? -> How much does it cost? [spoken aloud]
[EN -> ES] Twenty dollars -> Veinte dólares [spoken aloud]
Two people, different languages. System auto-detects who's speaking, translates bidirectionally, and speaks the translation aloud. Type 'exit' to stop and get a full transcript.

Quick Start
bash
/translate The defendant has the right to remain silent to Spanish
/translate myocardial infarction to Latin
/detect Bonjour, comment allez-vous?
/speak hello world
/listen
/interpret
Supported Languages (42)
English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese,
Korean, Arabic, Hindi, Dutch, Polish, Swedish, Turkish, Vietnamese, Thai, Greek,
Hebrew, Czech, Danish, Finnish, Norwegian, Romanian, Slovak, Slovenian, Ukrainian,
Catalan, Croatian, Bulgarian, Serbian, Latvian, Lithuanian, Estonian, Hungarian,
Icelandic, Indonesian, Malay, Swahili, Welsh, Zulu, Latin, ASL (gloss)

Braille (Opt-In)
Use /braille <text> for Grade 1 Braille Unicode output.
Works with refreshable Braille displays.
System-wide toggle: Ctrl+Shift+B or menu key 'b'.
