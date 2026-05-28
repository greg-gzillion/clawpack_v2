import sys
sys.path.insert(0, '.')
from agents.webclaw.core.chronicle_ledger import get_chronicle
c = get_chronicle()
for q in ['federal court circuit', 'federal district court', 'federal appellate', 'supreme court federal']:
    r = c.recover_by_context(q, limit=3)
    print(f'{q}: {len(r)} results')
    for x in r[:1]:
        print(f'  {x["url"][:80]}')
