# encoding: utf-8
'''CLAWPACK V2 - System Scanner for AI Onboarding
Run this first: python scripts/scan.py
Prints everything the next AI agent needs to understand the system.'''
import sys, json, os, time
from pathlib import Path
sys.path.insert(0, '.')

print('=' * 70)
print('  CLAWPACK V2 SYSTEM SCAN')
print('=' * 70)
print(f'  Time: {time.strftime("%Y-%m-%d %H:%M")}')

try:
    with open('VERSION') as f:
        print(f'  Version: {f.read().strip()}')
except: pass

import subprocess
try:
    r = subprocess.run(['git','log','--oneline','-3'], capture_output=True, text=True)
    print(f'  Git: {r.stdout.strip()[:200]}')
except: pass

print('\n--- ACTIVE MODEL ---')
try:
    am = json.loads(open('models/active_model.json').read())
    print(f'  Model: {am.get("model")} ({am.get("source")})')
    for k,v in am.get('providers',{}).items():
        print(f'  Provider: {k} (priority {v.get("priority","?")}) - {v.get("model")}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- OLLAMA ---')
try:
    import requests
    r = requests.get('http://localhost:11434/api/tags', timeout=3)
    models = [m['name'] for m in r.json().get('models',[])]
    print(f'  Running: {len(models)} models')
    for m in models[:10]:
        print(f'    - {m}')
except Exception as e:
    print(f'  Not running: {e}')

print('\n--- OBLITERATED MODELS ---')
oblit_dir = Path('models/obliterated')
if oblit_dir.exists():
    for d in sorted(oblit_dir.iterdir()):
        if d.is_dir():
            meta = d / 'abliteration_metadata.json'
            if meta.exists():
                m = json.loads(meta.read_text())
                print(f'  {d.name}: {m.get("source_model","?")} ({m.get("technique","?")})')

print('\n--- AGENTS ---')
agent_count = len([d for d in Path('agents').iterdir() if d.is_dir() and (d / 'agent_handler.py').exists()])
print(f'  Total: {agent_count}')

print('\n--- PROVIDER CHAIN ---')
try:
    from shared.llm.client import get_llm_client
    c = get_llm_client()
    provs = [p['type'].value for p in c.providers]
    print(f'  Providers: {provs}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- KEY FILES ---')
for f in ['shared/llm/client.py', 'shared/base_agent.py', 'a2a_server.py',
          'agents/webclaw/providers/webclaw_provider.py', 'scripts/onboard.py',
          'CLAWPACK_ONBOARD.md', 'VERSION']:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    print(f'  {f}: {size} bytes' if exists else f'  {f}: MISSING')

print('\n--- RECENT SESSION (June 4, 2026) ---')
print('  - WebClaw namespace-scoped SQL search deployed to all 19 agents')
print('  - Chronicle context removed from BaseAgent.ask_llm()')
print('  - direct_model added as first-class Sovereign Gateway provider')
print('  - llmclaw 4 llm*.py variants consolidated to 1 llm.py')
print('  - Gateway prompt cap at 4000 chars for local models')
print('  - str(PROJECT_ROOT) path bug fixed in webclaw_provider.py')
print('  - 161 obsolete scripts deleted, 16 kept')
print('  - Version bumped to 3.2.0')
print('  - FlowClaw 13 variants inventoried (dead code, ready to archive)')
print('  - RustPyCraw Article I violation resolved')

print('\n' + '=' * 70)
print('  SCAN COMPLETE')
print('  Next: python scripts/onboard.py for full documentation')
print('=' * 70)
