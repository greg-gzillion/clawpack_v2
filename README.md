🦞 Clawpack V2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Unified AI Agent Ecosystem** - 15 specialized agents working as one.

## Quick Start

```bash
git clone https://github.com/greg-gzillion/clawpack_v2.git
cd clawpack_v2
pip install -r requirements.txt
python clawpack.py
Unified Commands
Command	Agent	Description
translate Hello to Spanish	interpretclaw	Translation + auto-speak
speak Hello world	interpretclaw	Text-to-speech
solve x**2 = 4	mathematicaclaw	Math equations
plot sin(x)	plotclaw	Charts & graphs
dream a lobster	dreamclaw	AI image prompts
analyze photo.jpg	dreamclaw	Vision analysis (qwen3-vl)
flowchart A->B->C	flowclaw	Diagrams
/lesson es greetings	langclaw	Language lessons
Agents
Agent	Purpose
🦞 clawpack	Unified router (all agents)
🌐 interpretclaw	Translation + TTS
📐 mathematicaclaw	Math computation
📊 plotclaw	Charts & graphs
🎨 dreamclaw	AI vision & generation
🔷 flowclaw	Diagrams & flowcharts
📏 draftclaw	Technical drawings
🎯 designclaw	Graphic design
📝 docuclaw	Document processing
📈 dataclaw	Data analysis
🌍 webclaw	Web search
💰 txclaw	Blockchain
🏥 mediclaw	Medical references
⚖️ lawclaw	Legal references
📚 langclaw	Language teacher
LLMs
16 working LLMs detected and available:

10 local Ollama models (FREE)

4 OpenRouter models (FREE)

1 Anthropic Claude model

Individual Agents
Run any agent directly:

bash
python claw.py lang      # Language teacher
python claw.py interpret # Translator
python claw.py math      # Math solver
python claw.py plot      # Charts
python claw.py dream     # AI vision
License
MIT License - see LICENSE