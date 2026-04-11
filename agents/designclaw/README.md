\# 🎨 DESIGNCLAW



> Creative Professional Design Assistant with AI, Preview \& Export



\## Overview



DesignClaw is a modular AI-powered design assistant that helps with brand identity, mood boards, color palettes, typography, and design concepts. It generates \*\*HTML previews\*\* that open in your browser and saves all work to an organized exports folder.



\*\*DesignClaw vs DraftClaw:\*\*

\- \*\*DesignClaw\*\*: Creative concepts, branding, mood, identity, visual direction

\- \*\*DraftClaw\*\*: Technical drawings, CAD, blueprints, precise measurements



\---



\## 🚀 Quick Start



```bash

\# Interactive mode (guided brief)

python designclaw.py /interactive



\# Quick AI generation

python designclaw.py "brand identity for sustainable fashion startup"

python designclaw.py "mood brutalist tech"

python designclaw.py "color palette for luxury spa"



\# View commands

python designclaw.py /help

📁 Modular Structure

text

designclaw/

├── designclaw.py              # Main entry point

├── core/

│   └── agent.py               # Core logic \& AI integration

├── utils/

│   ├── preview.py             # HTML preview generator

│   └── input\_handler.py       # Interactive input collector

├── commands/                  # Command implementations

├── providers/                 # External services

└── exports/                   # Generated files (symlink to root)

🎯 Commands

Interactive Mode

Command	Description

/interactive	Step-by-step design brief collection

/preview	Reopen last generated preview

/export	Show exports folder location

/stats	View usage statistics

/help	Show all commands

/quit	Exit

Quick Generation

Command	Example

brand identity for \[name]	brand identity for Acme Corp

mood \[aesthetic]	mood dark academia

color palette for \[mood]	color palette for tech startup

typography advice	typography for luxury brand

slogan for \[brand]	slogan for AI productivity tool

🎨 Interactive Workflow

Brand Identity Brief

text

1\. Brand/Company name

2\. Industry (Tech, Healthcare, Luxury, Creative, Corporate, Startup)

3\. Brand tone (Professional, Friendly, Innovative, etc.)

4\. Core values (select 2-4)

5\. Target audience

6\. Competitors (optional)

7\. Unique value proposition

Mood Board Brief

text

1\. Project name

2\. Aesthetic (Minimal, Brutalist, Organic, Retro, Futuristic, etc.)

3\. Color mood (Warm, Cool, Neutral, Vibrant, Muted)

4\. Inspiration sources

5\. What to avoid

📂 Exports

All designs are saved to:



text

C:/Users/greg/dev/clawpack\_v2/exports/designclaw/

File Naming Convention

Brand: brand\_\[name]\_\[timestamp].html



Mood: mood\_\[name]\_\[timestamp].html



Preview Features

Brand Identity: Full preview card with colors, typography, and concept



Mood Board: Atmospheric preview with color dots and description



One-click browser open after generation



🤖 AI Integration

DesignClaw uses the shared LLMManager from Clawpack core:



Anthropic Claude (default) - Creative concept generation



OpenAI GPT - Fallback option



Local Ollama - Offline fallback



Configure via .env in root:



env

ANTHROPIC\_API\_KEY=your\_key\_here

OPENAI\_API\_KEY=your\_key\_here

🎨 Design Knowledge Base

Built-in design theory (used when AI unavailable):



Color Palettes

Industry	Colors

Tech	#0066FF, #1E1E2E, #FFFFFF, #00D4AA

Healthcare	#2ECC71, #3498DB, #FFFFFF, #F5F5F5

Luxury	#2C2C2C, #D4AF37, #FFFFFF, #8B7355

Creative	#FF6B6B, #4ECDC4, #FFE66D, #292F36

Corporate	#003366, #FFFFFF, #666666, #F0F0F0

Startup	#FF6B35, #004E89, #FFFFFF, #1A1A1A

Typography Pairings

Playfair Display + Source Sans Pro (elegant)



Montserrat + Merriweather (bold/readable)



Inter + Georgia (contemporary/classic)



Poppins + Open Sans (friendly/neutral)



Design Principles

Contrast, Repetition, Alignment, Proximity



Balance, Hierarchy, White Space, Scale



🔗 Integration with Clawpack

DesignClaw inherits from BaseAgent giving it access to:



Method	Description

ask\_webclaw(query)	Search 13,484 reference URLs

ask\_dataclaw(query)	Query local data files

learn(key, value)	Store in shared memory

recall(key)	Retrieve from memory

learn\_fact(fact)	Share with all agents

track\_interaction()	Usage analytics

📊 Examples

Example 1: Tech Startup Brand

bash

$ python designclaw.py /interactive

> Choose 1 (Brand Identity)

> Name: CloudScale

> Industry: Tech/Software

> Tone: Innovative

> Values: Innovation, Simplicity, Speed

> Audience: DevOps engineers

> Unique: AI-powered auto-scaling



🎨 BRAND IDENTITY: CloudScale

\[AI generates concept]

📁 Preview saved: brand\_CloudScale\_20260409\_143022.html

🌐 Open in browser? \[Y/n]: y

Example 2: Quick Mood Board

bash

$ python designclaw.py "mood dark academia"



🎭 MOOD: Dark Academia

Colors: #2C2C2C, #8B7355, #D4AF37, #1A1A1A

\[AI generates atmospheric description]

📁 Preview saved: mood\_dark\_academia\_20260409\_143145.html

🛠️ Dependencies

text

requests>=2.28.0

aiohttp>=3.8.0

All already in root requirements.txt



📝 License

Part of Clawpack v2 - MIT License



Made with 🎨 by the Clawpack Team

'@ | Out-File -FilePath "README.md" -Encoding utf8



Write-Host "✅ README.md created!" -ForegroundColor Green

Write-Host ""

Write-Host "📄 View it: cat README.md" -ForegroundColor Cyan

