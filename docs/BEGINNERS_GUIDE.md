# Clawpack V2 ? Beginner's Guide

## What is Clawpack?

Clawpack is a program that runs on your computer and gives you access to
multiple AI assistants, each with a different role. Some are domain experts
(legal research, medical analysis, code generation). Others are system
utilities (file operations, web search, model management). They communicate
through a central hub and can delegate work to each other.

Think of it as a team of specialists on your laptop, with a shared memory
and rules they all follow.

## What do I need?

- A Windows, Mac, or Linux computer
- Python 3.10 or newer installed
- At least 8GB of free disk space for models
- That is it. No cloud accounts required.

## Choosing a Model

Clawpack works with many AI models. The model you choose depends on your hardware and how thorough you want the answers to be. This is not a one-size-fits-all decision ? it is a feature.

### If you have a GPU with 4GB+ VRAM (like GTX 970, RTX 2060)
These models run fast on your graphics card:
- gemma3:4b (3.3GB) ? Fast, capable, fits comfortably. Recommended default.
- phi2 (2.7GB) ? Microsoft model, good quality for size. Obliterated (no refusals).
- smollm2:1.7b (3.4GB) ? Small but capable. Obliterated.

### If you have a GPU with 8GB+ VRAM (like RTX 3070, RTX 4070)
You can run larger models that give more thorough answers:
- deepseek-r1:8b (5.2GB) ? Strong reasoning, detailed responses
- codellama:7b (3.8GB) ? Good for code generation
- gemma3:12b (8.1GB) ? Very capable general purpose model

### If you only have CPU (no dedicated GPU)
Models will work but will be slower (30-120 seconds per response):
- tinyllama:1.1b (637MB) ? Fastest, basic responses
- gemma3:1b (815MB) ? Small but capable
- gemma3:4b (3.3GB) ? Works on CPU, just slower

### If you want cloud models (no local hardware needed)
Add API keys to the .env file. Cloud models are fast but may have rate limits or costs:
- Groq (free tier) ? Very fast, rate-limited
- OpenRouter (free tier available) ? Good fallback
- Anthropic (paid) ? Highest quality, costs per use

### How to switch models
From the menu, press m to open the model manager. Or from any agent, type:
/use gemma3:4b
/use deepseek-r1:8b
/use phi2

### The trade-off
Smaller models = faster responses, lower quality, fits less hardware
Larger models = slower responses, more thorough answers, needs better hardware
Cloud models = fast and capable, but need internet and may have limits

This is by design. You choose based on what matters to you: speed, quality, privacy, or cost.

## How do I install it?

### Step 1: Get the code

Download from github.com/greg-gzillion/clawpack_v2 or open a terminal and type:
git clone https://github.com/greg-gzillion/clawpack_v2.git
cd clawpack_v2

text

### Step 2: Install the AI engine (Ollama)

Ollama runs AI models on your computer. Download it from ollama.com.

Once installed, open a terminal and pull a model:
ollama pull deepseek-r1:8b

text

This downloads about 5GB ? the AI brain that Clawpack uses to think.

### Step 3: Install Python packages
pip install -r requirements.txt

text

### Step 4: Start Clawpack

You need two terminal windows.

**Terminal 1 ? the server:**
python a2a_server.py

text
Leave this running. It's the central hub.

**Terminal 2 ? the menu:**
python clawpack.py

text
Shows the menu of all agents.

## Your first commands

From the menu, type 1 and press Enter to open the legal agent.

Try these:
/court Denver CO
/help
exit

text

## What are all these agents?

### Domain Specialists (do the thinking)

| # | Agent | What it does |
|---|-------|-------------|
| 1 | lawclaw | Legal research, court info, case law, jurisdiction lookup |
| 4 | mathematicaclaw | Math, calculus, equations, plotting |
| 7 | interpretclaw | Translation between 42 languages |
| 8 | langclaw | Language teaching and practice |
| 9 | claw_coder | Code generation in 39 programming languages |
| 14 | mediclaw | Medical research, diagnosis assistance, hospital lookup |
| 15 | dreamclaw | AI image generation and vision |
| 16 | designclaw | Graphic design, logos, brand identity |
| 17 | draftclaw | Technical drawings, blueprints, CAD |
| 18 | crustyclaw | Rust programming language specialist |
| 20 | drawclaw | AI drawing, sketching, illustration |

### System Utilities (make everything work)

| # | Agent | What it does |
|---|-------|-------------|
| 2 | flowclaw | Creates diagrams, flowcharts, mindmaps from text |
| 3 | docuclaw | Document creation, formatting, PDF export |
| 10 | dataclaw | Local data processing and search |
| 11 | webclaw | Web search, URL fetching, knowledge indexing |
| 12 | fileclaw | File operations, format conversion |
| 13 | plotclaw | Charts, graphs, data visualization |
| 19 | rustypycraw | Code analysis and crawling |

### System Infrastructure

| # | Agent | What it does |
|---|-------|-------------|
| 5 | liberateclaw | AI model liberation and management |
| 6 | txclaw | Blockchain transactions and smart contracts |
| 21 | llmclaw | AI model selection and provider management |

## Getting Help

Every agent responds to /help ? it will show you all commands that agent
understands. Type exit to return to the menu. Type q to quit.

## What if something goes wrong?

- Make sure Terminal 1 (the server) is still running
- Check that Ollama is running (look for the llama icon in your taskbar)
- Try /stats in any agent ? if it responds, the system is working
