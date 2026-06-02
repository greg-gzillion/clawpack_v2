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
- About 10GB of free disk space (for the AI models)
- That's it. No cloud accounts required.

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
