from pathlib import Path
import re

agents_dir = Path("agents")
results = {}

for agent_dir in sorted(agents_dir.iterdir()):
    if not agent_dir.is_dir() or agent_dir.name.startswith("_"): continue
    handler = agent_dir / "agent_handler.py"
    if not handler.exists(): continue
    
    content = handler.read_text(encoding="utf-8", errors="ignore")
    
    calls = re.findall(r'call_agent\([\"\'](\\w+)[\"\']', content)
    delegates = re.findall(r'delegate\([\"\'](\\w+)[\"\']', content)
    
    all_calls = list(set(calls + delegates))
    outbound = len(all_calls)
    has_helpers = "_agent_helpers" in content
    has_base = "BaseAgent" in content
    
    results[agent_dir.name] = {
        "outbound": outbound,
        "calls": sorted(all_calls),
        "helpers": has_helpers,
        "base": has_base
    }

print(f'{"AGENT":<18} {"OUT":>4} {"HELPERS":>8} {"CONNECTS TO"}')
print("-" * 60)
total_outbound = 0
total_helpers = 0
for agent, data in sorted(results.items()):
    calls_str = ", ".join(data["calls"][:5])
    if len(data["calls"]) > 5:
        calls_str += f" +{len(data['calls'])-5} more"
    print(f"{agent:<18} {data['outbound']:>4} {'YES' if data['helpers'] else 'NO':>8} {calls_str}")
    total_outbound += data["outbound"]
    if data["helpers"]:
        total_helpers += 1

print("-" * 60)
print(f"Total outbound connections: {total_outbound}")
print(f"Agents with _agent_helpers: {total_helpers}/21")
print(f"Agents with BaseAgent: {sum(1 for d in results.values() if d['base'])}/21")

isolated = [a for a, d in results.items() if d["outbound"] == 0]
if isolated:
    print(f"\nISOLATED (0 outbound): {isolated}")
else:
    print(f"\nNo isolated agents — all connected.")
