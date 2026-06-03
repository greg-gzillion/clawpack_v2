#!/usr/bin/env python3
"""Print every file the next AI agent needs to read, in order."""
import os

FILES = [
    ("POWERSHELL_SURVIVAL_GUIDE.md", "How to work in this environment"),
    ("CLAWPACK_ONBOARD.md", "Architecture, rules, session log, next mission"),
    ("docs/WEBCLAW_ARCHITECTURE.md", "Central knowledge system - CRITICAL"),
    ("shared/CONSTITUTION_v1.md", "Supreme law - NON-NEGOTIABLE"),
    ("BASEAGENT_GUIDE.md", "What every agent inherits"),
    ("AGENT_CAPABILITIES.md", "Which agent owns which capability"),
    ("CHRONICLE_GUIDE.md", "How the knowledge database works"),
    ("DECISION_LOG.md", "Why architectural decisions were made"),
    ("docs/reports/STATE_OF_CLAWPACK_V2_2026_06_02.md", "Audit snapshot"),
]

for i, (filepath, desc) in enumerate(FILES, 1):
    print(f"\n{"=" * 70}")
    print(f"  FILE {i}/9: {filepath}")
    print(f"  {desc}")
    print(f"{"=" * 70}\n")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print(f"  [FILE NOT FOUND: {filepath}]")
    print()