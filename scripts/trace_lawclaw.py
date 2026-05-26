import sys
sys.path.insert(0, '.')
from shared.base_agent import BaseAgent

agent = BaseAgent('lawclaw')

# Step 1: What does search_chronicle return?
results = agent.search_chronicle('Richmond VA court', limit=5)
print(f'Chronicle results: {len(results)}')
for r in results:
    print(f'  {r.get("url","")[:80]}')

# Step 2: What does ask_llm return with the same query?
print('\n--- ask_llm ---')
result = agent.ask_llm('Richmond VA court')
print(f'Length: {len(result)}')
print(result[:500])
