# MedicLaw — Constitutional Medical AI Agent

## What It Does
Medical diagnosis, emergency triage, hospital geolocation, and document generation.
Serves both healthcare professionals and laypersons with authoritative sourcing.

## Commands

### Core Medical
| Command | Description |
|---------|-------------|
| `/diagnose <symptoms>` | Differential diagnosis with urgency triage + hospital routing |
| `/treatment <condition>` | Evidence-based treatment recommendations |
| `/research <topic>` | Medical research with authoritative sources |
| `/med <query>` | General medical query |

### Emergency & Routing
| Command | Description |
|---------|-------------|
| `/emergency <symptoms>` | Emergency triage with automatic ER lookup |
| `/er <city ST>` | Find emergency departments by city |
| `/nearest <lat>,<lon>` | Find nearest hospital to GPS coordinates |
| `/hospital <city ST>` | List all hospitals with GPS, phone, URL |
| `/specialty <type> in <city ST>` | Find hospitals by specialty (cardiac, pediatric, etc.) |
| `/referral <condition>` | Specialist recommendation with facility enrichment |

### Documents
| Command | Description |
|---------|-------------|
| `/doc medical report <condition>` | Generate structured medical report |
| `/doc referral letter <condition> to <specialty>` | Generate referral letter |
| `/doc treatment plan <condition>` | Generate comprehensive treatment plan |
| `/doc discharge <condition>` | Generate discharge instructions |

### Pharmacy & Labs
| Command | Description |
|---------|-------------|
| `/medications <drug>` | Drug information |
| `/interactions <drugs>` | Drug interaction check |
| `/warnings <drug>` | Drug warnings and side effects |

### Cross-Agent
| Command | Description |
|---------|-------------|
| `/translate <text> to <lang>` | Medical translation with term preservation |
| `/delegate <agent> <task>` | Send task to any agent in the mesh |
| `/shared read [key]` | Read from shared memory |
| `/shared write key:value` | Write to shared memory |
| `/stats` | Agent statistics |

## Quick Start

/diagnose chest pain in Denver CO
/emergency difficulty breathing
/hospital Miami FL
/specialty cardiac in Denver CO
/nearest 39.7392,-104.9903
/doc medical report hypertension - patient: John Doe
/translate the diagnosis to Spanish

text

## Architecture
- **Hospital geolocation**: 3,800+ city jurisdiction files via Chronicle FTS5
- **Urgency triage**: Professional/layperson detection with appropriate response depth
- **Cross-agent**: Delegates to interpretclaw for translation, docuclaw for formatting
- **Memory**: All diagnoses and research cached for cross-agent recall
- **Constitutional**: 23-system boundary, 36 shared systems, circuit breaker protected

## Sources
NIH (nih.gov), CDC (cdc.gov), Mayo Clinic (mayoclinic.org), peer-reviewed literature.
Educational purposes only. Always consult a healthcare professional.
