# Mediclaw AI Agent - Complete Medical Reference System

## Overview

Mediclaw is a professional medical reference AI agent that provides evidence-based medical information from authoritative sources. It is part of the Clawpack ecosystem - a modular, cross-learning AI agent system where multiple specialized agents share knowledge and maintain persistent memory.

### Core Capabilities

- **Live Medical Research** - Fetches real-time content from authoritative sources (CDC, WHO, NIH, Mayo Clinic, Cleveland Clinic)
- **Differential Diagnosis** - AI-powered diagnostic assistance with red flag identification
- **Treatment Guidelines** - Evidence-based treatment recommendations with first-line therapies
- **Pharmacology Reference** - Drug information, interactions, and FDA warnings
- **Specialty Coverage** - 48 medical specialties with comprehensive references
- **Citation Support** - Every response includes source URLs from authoritative medical institutions

## Architecture

### Directory Structure
mediclaw/
├── mediclaw.py # Main entry point (small, imports from modules)
├── cli/
│ └── interface.py # Command-line interface handler
├── commands/ # Individual command handlers
│ ├── research.py # /research command
│ ├── diagnose.py # /diagnose command
│ ├── treatment.py # /treatment command
│ ├── medications.py # /medications command
│ ├── interactions.py # /interactions command
│ ├── warnings.py # /warnings command
│ ├── pediatrics.py # /pediatrics command
│ ├── geriatrics.py # /geriatrics command
│ ├── lab_tests.py # /lab command
│ ├── icd10.py # /icd command
│ ├── prevention.py # /prevention command
│ ├── diet.py # /diet command
│ ├── exercise.py # /exercise command
│ ├── natural.py # /natural command
│ ├── procedure.py # /procedure command
│ ├── prognosis.py # /prognosis command
│ ├── referral.py # /referral command
│ ├── sources.py # /sources command
│ └── stats.py # /stats command
├── core/
│ ├── agent.py # Core agent logic with webclaw integration
│ └── engine.py # Query execution engine
├── providers/ # API providers
│ ├── openrouter.py # OpenRouter API (GPT-3.5-turbo)
│ ├── anthropic.py # Anthropic Claude (fallback)
│ └── ollama.py # Local Ollama models (fallback)
├── fetchers/
│ └── url_fetcher.py # URL content fetching with BeautifulSoup
├── config/
│ └── settings.py # Configuration (paths, API keys)
└── references/ # Linked to webclaw (see below)

text

### Webclaw Integration

Mediclaw references are stored in the shared webclaw directory:
webclaw/references/mediclaw/
├── anatomy/anatomy_references.md
├── cardiology/
│ ├── cardiology_references.md # URLs for heart disease
│ ├── hypertension.md # Full hypertension content
│ ├── heart_failure.md # Full heart failure content
│ └── coronary_artery_disease.md # Full CAD content
├── endocrinology/
│ ├── endocrinology_references.md # URLs for diabetes, thyroid
│ └── diabetes_type2.md # Full diabetes content
├── neurology/
│ ├── neurology_references.md # URLs for stroke, migraine
│ ├── stroke.md # Full stroke content
│ └── migraine.md # Full migraine content
└── [45 additional specialties...]

text

Each reference file contains authoritative URLs from:
- CDC (Centers for Disease Control)
- WHO (World Health Organization)
- NIH (National Institutes of Health)
- Mayo Clinic
- Cleveland Clinic
- Johns Hopkins Medicine
- Professional medical societies

## Installation

### Prerequisites

```bash
# Python 3.12 or higher
python --version

# Required packages
pip install requests beautifulsoup4 lxml python-dotenv
Configuration
API Key Setup (for AI fallback when webclaw has no content)

Create .env file in the root directory:

bash
C:/Users/greg/dev/clawpack_v2/.env
Add your OpenRouter API key:

text
OPENROUTER_API_KEY=sk-or-v1-your-key-here
Webclaw References

The medical reference files are already populated in:

text
C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/mediclaw/
Usage
Starting Mediclaw
bash
cd C:\Users\greg\dev\clawpack_v2\agents\mediclaw
python mediclaw.py
Command Reference
Core Medical Commands
Command	Description	Example
/research <topic>	Comprehensive medical research with citations	/research hypertension
/diagnose <symptoms>	Differential diagnosis with red flags	/diagnose chest pain
/treatment <condition>	Evidence-based treatment guidelines	/treatment diabetes
Pharmacology
Command	Description	Example
/medications <drug>	Drug information (dosing, side effects)	/medications metformin
/interactions <drugs>	Drug interaction analysis	/interactions lisinopril,ibuprofen
/warnings <drug>	FDA warnings and black box alerts	/warnings metformin
Special Populations
Command	Description	Example
/pediatrics <issue>	Pediatric-specific care	/pediatrics fever
/geriatrics <issue>	Elderly care considerations	/geriatrics fall risk
Diagnostics
Command	Description	Example
/lab <test>	Lab test interpretation	/lab CBC
/icd <diagnosis>	ICD-10 coding	/icd diabetes
Prevention & Lifestyle
Command	Description	Example
/prevention <condition>	Prevention guidelines	/prevention diabetes
/diet <condition>	Dietary recommendations	/diet hypertension
/exercise <condition>	Exercise guidance	/exercise arthritis
/natural <condition>	Natural remedies	/natural anxiety
Clinical Guidance
Command	Description	Example
/procedure <name>	Procedure information	/procedure colonoscopy
/prognosis <condition>	Disease prognosis	/prognosis cancer
/referral <condition>	Specialist referral	/referral back pain
Utilities
Command	Description
/sources	List all 48 medical specialties
/stats	Session statistics (queries, sources, API status)
/clear	Clear screen
/quit	Exit mediclaw
Example Sessions
Research Hypertension
text
mediclaw> /research hypertension

📚 **WEBCLAW CITATIONS - CARDIOLOGY**
🔍 hypertension

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 **WHO Hypertension Fact Sheet**
🔗 **Source:** https://www.who.int/news-room/fact-sheets/detail/hypertension

**Excerpt:**
An estimated 1.4 billion adults aged 30–79 years worldwide had hypertension in 2024;
this represents 33% of the population in this age range...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Diagnose Chest Pain
text
mediclaw> /diagnose chest pain

🩺 Diagnosing: chest pain

DIFFERENTIAL DIAGNOSIS:
- Acute Coronary Syndrome (heart attack) - EMERGENCY
- Stable Angina - cardiology referral
- GERD (acid reflux) - gastroenterology
- Costochondritis - musculoskeletal
- Pulmonary Embolism - EMERGENCY

RED FLAGS: Shortness of breath, radiation to arm/jaw, sweating
Treatment Diabetes
text
mediclaw> /treatment diabetes

💊 Treating: diabetes

FIRST-LINE:
- Metformin 500-2000mg daily
- Lifestyle modifications (diet, exercise)

SECOND-LINE:
- SGLT2 inhibitors (empagliflozin, dapagliflozin)
- GLP-1 agonists (semaglutide, liraglutide)

MONITORING:
- HbA1c every 3-6 months (goal <7%)
- Annual eye exam, foot exam, renal function
Data Flow
How Mediclaw Works
User enters command (e.g., /research hypertension)

Mediclaw searches webclaw for matching specialty:

Checks cardiology/ folder

Reads cardiology_references.md for URLs

Also checks topic files like hypertension.md

Fetches live content from authoritative URLs:

CDC, WHO, NIH, Mayo Clinic, Cleveland Clinic

Uses BeautifulSoup to extract main content

Respects rate limiting and timeout settings

Returns content with citations:

Shows source title and URL

Displays relevant excerpt

Preserves original formatting

Fallback to AI (if no webclaw URLs found):

Calls OpenRouter API (GPT-3.5-turbo)

Returns AI-generated medical information

Clearly marks as AI response

Provider Priority
text
1. Webclaw URLs (local reference files)
   ↓ (if no URLs found)
2. OpenRouter API (GPT-3.5-turbo)
   ↓ (if API fails)
3. Ollama (local LLM models)
Authoritative Sources
Mediclaw fetches content from these trusted sources:

Source	Type	URL
CDC	US Government	cdc.gov
WHO	UN Organization	who.int
NIH	US Government	nih.gov
Mayo Clinic	Academic Medical Center	mayoclinic.org
Cleveland Clinic	Academic Medical Center	clevelandclinic.org
Johns Hopkins	Academic Medical Center	hopkinsmedicine.org
American Heart Association	Professional Society	heart.org
American Diabetes Association	Professional Society	diabetes.org
Adding New Medical Content
Add a New Specialty
Create folder in webclaw:

bash
mkdir C:\Users\greg\dev\clackpack_v2\agents\webclaw\references\mediclaw\new_specialty
Create reference file:

bash
touch new_specialty/new_specialty_references.md
Add authoritative URLs to the reference file:

markdown
# NEW SPECIALTY - Medical References

## Authoritative Sources
- **Source Name**: https://authoritative-url.com
Add a New Topic to Existing Specialty
Navigate to specialty folder:

bash
cd C:\Users\greg\dev\clackpack_v2\agents\webclaw\references\mediclaw\cardiology
Create topic file:

bash
touch new_topic.md
Add medical content with sections:

markdown
# New Topic

## Definition
[Clinical definition]

## Diagnosis
[Diagnostic criteria]

## Treatment
[Treatment guidelines]

## References
- **Source**: https://url.com
Troubleshooting
Common Issues
Issue	Solution
"API key not configured"	Check .env file exists with OPENROUTER_API_KEY
"403 Forbidden"	URL requires authentication - replace with open-access source
"404 Not Found"	URL has moved - find updated URL
"No webclaw references found"	Add URLs to the specialty reference file
Webclaw path not found	Verify config/settings.py has correct WEBCLAW_PATH
Testing API Connection
bash
cd C:\Users\greg\dev\clackpack_v2
python -c "from shared.llm.api import test; print('API works:', test())"
Verifying Webclaw Files
bash
cd C:\Users\greg\dev\clackpack_v2\agents\webclaw\references\mediclaw
ls */**/*.md | Measure-Object  # Count all markdown files
Performance
First query: ~2-5 seconds (fetches live content from URLs)

Subsequent queries: ~1-3 seconds (cached connections)

API fallback: ~1-2 seconds (OpenRouter API)

Local webclaw content: Instant (reads from disk)

Security
API keys stored in .env (excluded from git via .gitignore)

No hardcoded credentials in source code

All external requests use timeout limits (30-60 seconds)

URL fetching respects robots.txt via User-Agent headers

Dependencies
text
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dotenv>=1.0.0
License
MIT License - Part of Clawpack ecosystem

Contributing
Add new URLs to webclaw reference files

Create new topic files with clinical content

Test commands before submitting

Ensure all URLs are from authoritative sources (.gov, .edu, major medical centers)

Related Agents
Polyclaw - Translation agent (20+ languages)

Lawclaw - Legal reference agent

TX-Agent - Blockchain reference agent

Webclaw - General web/cloud reference agent

Claw-coder - Programming assistant agent