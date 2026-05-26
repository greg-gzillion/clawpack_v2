import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.base_agent import BaseAgent

agent = BaseAgent("lawclaw")

# Test the full ask_llm path that lawclaw uses
query = "What is the Worcester MA police department address and chief name?"

# Step 1: search chronicle
chronicle_results = agent.search_chronicle(query, limit=10)
print(f"Step 1 - Chronicle results: {len(chronicle_results)}")
for r in chronicle_results[:2]:
    print(f"  URL: {r.get('url','')[:80]}")
    ctx = r.get('context','')
    print(f"  Context length: {len(ctx)} chars")
    print(f"  Context preview: {ctx[:200]}...")
    print()

# Step 2: check what ask_llm actually builds
print("\nStep 2 - Testing what ask_llm sends to llmclaw...")
# The ask_llm method builds context from chronicle results
if chronicle_results:
    lines = []
    for c in chronicle_results:
        ctx = c.get('context', '') if isinstance(c, dict) else str(c)
        if ctx:
            lines.append(ctx)
    context = "\n---\n".join(lines)
    print(f"Built context: {len(context)} chars")
    print(f"First 500 chars: {context[:500]}")
