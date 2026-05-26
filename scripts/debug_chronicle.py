import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.webclaw.core.chronicle_ledger import get_chronicle
from shared.base_agent import BaseAgent

# Test the exact code path
agent = BaseAgent("lawclaw")
print(f"Agent name: {agent.name}")

# Manually do what search_chronicle does
try:
    chronicle = get_chronicle()
    print(f"Chronicle loaded: {chronicle.db_path}")
    results = chronicle.recover_by_context("Worcester MA police chief", limit=5, source_filter="lawclaw")
    print(f"Manual results: {len(results)}")
except Exception as e:
    print(f"Manual error: {e}")

# Now test the actual method
print("\n--- Testing actual search_chronicle ---")
results = agent.search_chronicle("Worcester MA police chief", limit=5)
print(f"search_chronicle results: {len(results)}")
for r in results:
    print(f"  {r.get('url','')[:80]}")
