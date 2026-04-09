"""Mediclaw CLI Interface"""

import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import MediclawAgent

class MediclawCLI:
    def __init__(self):
        self.agent = MediclawAgent()
    
    def run(self):
        self._show_header()
        
        while True:
            try:
                cmd = input("\n📋 > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/clear":
                    os.system('cls')
                elif cmd == "/sources":
                    self._show_sources()
                elif cmd == "/stats":
                    self._show_stats()
                elif cmd.startswith("/research"):
                    self._research(cmd[9:].strip())
                elif cmd.startswith("/diagnose"):
                    self._diagnose(cmd[9:].strip())
                elif cmd.startswith("/treatment"):
                    self._treatment(cmd[10:].strip())
                elif cmd.startswith("/medications"):
                    self._medications(cmd[12:].strip())
                elif cmd.startswith("/interactions"):
                    self._interactions(cmd[13:].strip())
                elif cmd.startswith("/warnings"):
                    self._warnings(cmd[9:].strip())
                elif cmd.startswith("/pediatrics"):
                    self._pediatrics(cmd[11:].strip())
                elif cmd.startswith("/geriatrics"):
                    self._geriatrics(cmd[11:].strip())
                elif cmd.startswith("/lab"):
                    self._lab(cmd[4:].strip())
                elif cmd.startswith("/icd"):
                    self._icd(cmd[4:].strip())
                elif cmd.startswith("/prevention"):
                    self._prevention(cmd[11:].strip())
                elif cmd.startswith("/diet"):
                    self._diet(cmd[5:].strip())
                elif cmd.startswith("/exercise"):
                    self._exercise(cmd[9:].strip())
                elif cmd.startswith("/natural"):
                    self._natural(cmd[8:].strip())
                elif cmd.startswith("/procedure"):
                    self._procedure(cmd[10:].strip())
                elif cmd.startswith("/prognosis"):
                    self._prognosis(cmd[10:].strip())
                elif cmd.startswith("/referral"):
                    self._referral(cmd[9:].strip())
                else:
                    self._show_help()
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def _show_header(self):
        print("\n" + "="*70)
        print("MEDICLAW AI AGENT".center(70))
        print("="*70)
        print(f"Webclaw Sources: {len(self.agent.webclaw_sources())}")
        print("="*70)
        self._show_help()
    
    def _show_help(self):
        print("""
COMMANDS:
  /research <topic>      - Medical research
  /diagnose <symptoms>   - Differential diagnosis
  /treatment <condition> - Treatment guidelines
  /medications <drug>    - Drug information
  /interactions <drugs>  - Drug interactions
  /warnings <drug>       - FDA warnings
  /pediatrics <issue>    - Pediatric care
  /geriatrics <issue>    - Elderly care
  /lab <test>            - Lab test interpretation
  /icd <diagnosis>       - ICD-10 coding
  /prevention <condition>- Prevention guidelines
  /diet <condition>      - Dietary recommendations
  /exercise <condition>  - Exercise guidance
  /natural <condition>   - Natural remedies
  /procedure <name>      - Procedure information
  /prognosis <condition> - Disease prognosis
  /referral <condition>  - Specialist referral
  /sources               - List medical sources
  /stats                 - Session statistics
  /clear                 - Clear screen
  /quit                  - Exit
""")
    
    def _show_sources(self):
        sources = self.agent.webclaw_sources()
        print(f"\n📚 Medical Sources ({len(sources)}):")
        for i, s in enumerate(sources[:30], 1):
            print(f"   {i:3}. {s}")
        if len(sources) > 30:
            print(f"   ... and {len(sources)-30} more")
    
    def _show_stats(self):
        print(f"\n📊 Session Statistics:")
        print(f"   Queries: {len(self.agent.session['queries'])}")
        print(f"   Sources: {len(self.agent.webclaw_sources())}")
    
    def _research(self, q):
        if q:
            print(f"\n🔬 Researching: {q}")
            print(self.agent.research(q))
            self.agent.session['queries'].append(q)
        else:
            print("Usage: /research hypertension")
    
    def _diagnose(self, s):
        if s:
            print(f"\n🩺 Diagnosing: {s}")
            print(self.agent.diagnose(s))
            self.agent.session['queries'].append(s)
        else:
            print("Usage: /diagnose chest pain")
    
    def _treatment(self, c):
        if c:
            print(f"\n💊 Treating: {c}")
            print(self.agent.treatment(c))
            self.agent.session['queries'].append(c)
        else:
            print("Usage: /treatment diabetes")
    
    def _medications(self, d):
        if d:
            print(f"\n💊 Medication: {d}")
            print(self.agent.medications(d))
        else:
            print("Usage: /medications metformin")
    
    def _interactions(self, d):
        if d:
            print(f"\n⚠️ Interactions: {d}")
            print(self.agent.interactions(d))
        else:
            print("Usage: /interactions lisinopril,ibuprofen")
    
    def _warnings(self, d):
        if d:
            print(f"\n⚠️ Warnings: {d}")
            print(self.agent.warnings(d))
        else:
            print("Usage: /warnings metformin")
    
    def _pediatrics(self, i):
        if i:
            print(f"\n👶 Pediatrics: {i}")
            print(self.agent.pediatrics(i))
        else:
            print("Usage: /pediatrics fever")
    
    def _geriatrics(self, i):
        if i:
            print(f"\n👴 Geriatrics: {i}")
            print(self.agent.geriatrics(i))
        else:
            print("Usage: /geriatrics fall risk")
    
    def _lab(self, t):
        if t:
            print(f"\n🔬 Lab Test: {t}")
            print(self.agent.lab_tests(t))
        else:
            print("Usage: /lab CBC")
    
    def _icd(self, d):
        if d:
            print(f"\n📋 ICD-10: {d}")
            print(self.agent.coding(d))
        else:
            print("Usage: /icd diabetes")
    
    def _prevention(self, c):
        if c:
            print(f"\n🛡️ Prevention: {c}")
            print(self.agent.prevention(c))
        else:
            print("Usage: /prevention diabetes")
    
    def _diet(self, c):
        if c:
            print(f"\n🥗 Diet: {c}")
            print(self.agent.diet(c))
        else:
            print("Usage: /diet hypertension")
    
    def _exercise(self, c):
        if c:
            print(f"\n🏃 Exercise: {c}")
            print(self.agent.exercise(c))
        else:
            print("Usage: /exercise arthritis")
    
    def _natural(self, c):
        if c:
            print(f"\n🌿 Natural Remedies: {c}")
            print(self.agent.natural(c))
        else:
            print("Usage: /natural anxiety")
    
    def _procedure(self, p):
        if p:
            print(f"\n🔪 Procedure: {p}")
            print(self.agent.procedure(p))
        else:
            print("Usage: /procedure colonoscopy")
    
    def _prognosis(self, c):
        if c:
            print(f"\n📈 Prognosis: {c}")
            print(self.agent.prognosis(c))
        else:
            print("Usage: /prognosis cancer")
    
    def _referral(self, c):
        if c:
            print(f"\n🏥 Referral: {c}")
            print(self.agent.referral(c))
        else:
            print("Usage: /referral back pain")
