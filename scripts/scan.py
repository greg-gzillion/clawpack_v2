# encoding: utf-8
'''CLAWPACK V2 - System Scanner for AI Onboarding
Run this first: python scripts/scan.py
Prints everything the next AI agent needs to understand the system.'''
import sys, json, os, time
from pathlib import Path
sys.path.insert(0, '.')

print('=' * 70)
print('  CLAWPACK V2 SYSTEM SCAN')
print('--- ONBOARDING CHAIN ---')
import os
for f in ['README.md','docs/READ_THIS_FIRST.md','docs/KNOWN_TRAPS.md','docs/NEXT_SESSION_MISSION.md','CLAWPACK_ONBOARD.md','POWERSHELL_SURVIVAL_GUIDE.md']:
    print('  ' + f + ': ' + ('PRESENT' if os.path.exists(f) else 'MISSING'))
print('=' * 70)
