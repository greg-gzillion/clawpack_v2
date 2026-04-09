# Language Reference Guide

## Available Languages in Webclaw

The following languages have reference files in webclaw:

| Code | Language | Resources |
|------|----------|-----------|
| es | Spanish | dictionaries, grammar, pronunciation, tts |
| fr | French | dictionaries, grammar, pronunciation, tts |
| de | German | dictionaries, grammar, pronunciation, tts |
| it | Italian | dictionaries, grammar, pronunciation, tts |
| pt | Portuguese | dictionaries, grammar, pronunciation, tts |
| ja | Japanese | dictionaries, grammar, pronunciation, tts |
| ko | Korean | dictionaries, grammar, pronunciation, tts |
| zh | Chinese | dictionaries, grammar, pronunciation, tts |
| ru | Russian | dictionaries, grammar, pronunciation, tts |
| ar | Arabic | dictionaries, grammar, pronunciation, tts |
| hi | Hindi | dictionaries, grammar, pronunciation, tts |
| vi | Vietnamese | dictionaries, grammar, pronunciation, tts |
| th | Thai | dictionaries, grammar, pronunciation, tts |

## How It Works

1. User requests translation via /translate
2. Langclaw searches webclaw/languages/{code}/ folders
3. Extracts URLs from .md files in dictionaries/, learning/, grammar/
4. Fetches live content from those URLs
5. Returns translation with citations
