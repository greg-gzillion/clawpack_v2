#!/usr/bin/env python3
"""Clawpack V2 System Scan"""
import json, sqlite3, requests, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
A2A = "http://127.0.0.1:8766"
G = "[92m"; R = "[91m"; Y = "[93m"; C = "[96m"; B = "[1m"; X = "[0m"

def ok(m): print(f"  {G}[OK]{X}  {m}")
def bad(m): print(f"  {R}[FAIL]{X} {m}")
def warn(m): print(f"  {Y}[WARN]{X} {m}")
def sec(t):
    print()
    print(f"{B}{C}{chr(61)*60}{X}")
    print(f"{B}{C}  {t}{X}")
    print(f"{B}{C}{chr(61)*60}{X}")

print(f"{B}{chr(61)*60}{X}")
print(f"{B}  CLAWPACK V2 SYSTEM SCAN{X}")
print(f"{B}{chr(61)*60}{X}")
print(f"  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
v = ROOT / "VERSION"
ver = v.read_text().strip() if v.exists() else "?"
print(f"  Version: {ver}")

sec("1. SYSTEM IDENTITY")
print("  21-agent local-first AI runtime")
print("  A2A routing on port 8766")
print("  Chronicle SQLite FTS5 (448MB)")
print("  BM25 retrieval with source confidence")
print("  DataClaw cache for local-first knowledge")
print("  Constitutional governance")
print("  Provider chain: Groq -> Ollama -> OpenRouter -> Anthropic")

sec("2. RUNTIME HEALTH")
server_online = False
try:
    r = requests.get(f"{A2A}/health", timeout=5)
    d = r.json()
    ok(f"Server ONLINE: {d.get("agents","?")} agents")
    server_online = True
except:
    bad("Server OFFLINE -- start with: python a2a_server.py")

db_paths = [ROOT / "runtime" / "chronicle.db", ROOT / "data" / "chronicle.db"]
db = None
for p in db_paths:
    if p.exists(): db = p; break
if db:
    size_mb = db.stat().st_size / (1024*1024)
    ok(f"Chronicle: {size_mb:.0f} MB at {db.relative_to(ROOT)}")
else:
    bad("Chronicle database missing")

m = ROOT / "models" / "active_model.json"
if m.exists():
    md = json.loads(m.read_text())
    ok(f"Active model: {md.get("model","?")} ({md.get("source","?")})")
else:
    bad("No active model configured")

ok(".env present") if (ROOT / ".env").exists() else warn(".env missing")

sec("3. CACHE STATUS")
try:
    from shared.search_cache import get_cache_stats
    stats = get_cache_stats()
    agents_cached = len(stats.get("agents", {}))
    total = stats.get("total_entries", 0)
    hits = stats.get("total_hits", 0)
    ok(f"Cache: {total} entries, {hits} hits across {agents_cached} agents")
    for agent, s in stats.get("agents", {}).items():
        print(f"    {agent}: {s["entries"]} entries, {s["hits"]} hits")
    if agents_cached <= 1:
        warn("Cache largely unused — only lawclaw actively populating")
except Exception as e:
    warn(f"Cache stats unavailable: {e}")

sec("4. AGENT VALIDATION")
agents = ["lawclaw","claw_coder","crustyclaw","mediclaw","designclaw","draftclaw","dreamclaw","interpretclaw","langclaw","liberateclaw","dataclaw","drawclaw","flowclaw","docuclaw","llmclaw","mathematicaclaw","plotclaw","rustypycraw","txclaw","webclaw","fileclaw"]
valid = 0; issues = 0
for a in agents:
    hp = ROOT / "agents" / a / "agent_handler.py"
    rp = ROOT / "agents" / a / "README.md"
    if not hp.exists():
        bad(f"{a}: no handler"); issues += 1; continue
    content = hp.read_text(encoding="utf-8-sig", errors="ignore")
    flags = []
    if "BaseAgent" not in content: flags.append("no BaseAgent")
    if "call_agent" not in content: flags.append("no delegation")
    if "cached_search" in content: flags.append("uses cached_search")
    for banned in ["import anthropic","import groq","import openai","import ollama"]:
        if banned in content and "from shared.llm" not in content:
            flags.append(f"Article I: direct {banned.split()[1]} import"); break
    if not rp.exists(): flags.append("no README")
    if flags:
        bad_flags = [f for f in flags if "Article I" in f or "no " in f]
        good_flags = [f for f in flags if f not in bad_flags]
        if bad_flags:
            warn(f"{a}: {chr(44).join(bad_flags)}"); issues += 1
        else:
            valid += 1
    else:
        valid += 1
ok(f"Valid: {valid}/{len(agents)}")
if issues > 0: warn(f"Issues: {issues}")

sec("5. CONSTITUTIONAL AUDIT")
art1 = 0; art7 = 0; ns_bad = 0
for hp in (ROOT / "agents").rglob("agent_handler.py"):
    content = hp.read_text(encoding="utf-8-sig", errors="ignore")
    agent = hp.parent.name
    for banned in ["import anthropic","import groq","import openai","import ollama"]:
        if banned in content and "from shared.llm" not in content:
            warn(f"Article I: {agent} has direct {banned.split()[1]} import"); art1 += 1; break
    lns = content.splitlines()
    for i, line in enumerate(lns):
        if line.strip() == "except:" and i+1 < len(lns):
            if lns[i+1].strip() == "pass":
                warn(f"Article VII: {agent} bare except:pass at line {i+1}"); art7 += 1; break
    if "gather_context" in content and "ns:" not in content and "cached_search" not in content:
        warn(f"Namespace: {agent} _gather_context missing ns: prefix"); ns_bad += 1
if art1 == 0: ok("Article I (Sovereignty): clean")
else: bad(f"Article I violations: {art1}")
if art7 == 0: ok("Article VII (Silent Failure): clean")
else: bad(f"Article VII violations: {art7}")
if ns_bad == 0: ok("Namespace scoping: clean")
else: bad(f"Namespace violations: {ns_bad}")

sec("6. RETRIEVAL ARCHITECTURE")
bm25_agents = 0; cached_agents = 0
for hp in (ROOT / "agents").rglob("agent_handler.py"):
    content = hp.read_text(encoding="utf-8-sig", errors="ignore")
    if "cached_search" in content: cached_agents += 1
print(f"  Agents using cached_search(): {cached_agents}")
print(f"  Target: all retrieval-heavy agents")
print(f"  BM25 pipeline: provider + chronicle + dedup + source_weight")

sec("7. TECHNICAL DEBT")
fv = len(list((ROOT / "agents" / "flowclaw").glob("flowclaw*.py"))) - 1
dv = len(list((ROOT / "agents" / "docuclaw").glob("docuclaw*.py"))) - 1
if fv > 0: warn(f"FlowClaw variants: {fv}")
else: ok("FlowClaw: single implementation")
if dv > 0: warn(f"DocuClaw variants: {dv}")
else: ok("DocuClaw: single implementation")
bk = len(list(ROOT.rglob("*backup*"))) + len(list(ROOT.rglob("*_backup*")))
if bk > 0: warn(f"Backup files/dirs: {bk}")
else: ok("No backup cruft")

sec("8. BETA GATES (5/10)")
gates = [
    ("Enforcement blocks violations", True),
    ("21 agents online", True),
    ("Constitutional ledger stable", True),
    ("WebClaw BM25 operational", True),
    ("Validation harness operational", True),
    ("Cache population working", False),
    ("Retrieval standardization", False),
    ("FlowClaw consolidation", False),
    ("Enforcement activation", False),
    ("Beta readiness review", False),
]
done = 0
for gate, status in gates:
    if status:
        print(f"  {G}[DONE]{X}   {gate}")
        done += 1
    else:
        print(f"  {Y}[TODO]{X}  {gate}")
print(f"\n  {done}/10 complete")

sec("9. NEXT PRIORITIES")
print("  1. Cache population — investigate why only lawclaw has entries")
print("  2. BM25 visibility — split /search (raw) from normal requests (LLM)")
print("  3. _gather_context() migration — 12 agents to cached_search()")
print("  4. FlowClaw consolidation — 13 variants -> 1")
print("  5. Enforcement activation — blocking, not just detection")

sec("SCAN SUMMARY")
print(f"  Version: {ver}")
if db: print(f"  Chronicle: {size_mb:.0f} MB")
print(f"  Agents valid: {valid}/{len(agents)}")
print(f"  Article I violations: {art1}")
print(f"  Article VII violations: {art7}")
print(f"  Namespace violations: {ns_bad}")
print(f"  cached_search() adoption: {cached_agents}/21 agents")
print(f"  Beta gates: {done}/10")
print()
print("  python scripts/onboard.py        -- full system documentation")
print("  python scripts/validate_agents.py -- test all 21 agents")
print("  python a2a_server.py             -- start the server")
print(f"\n{B}{chr(61)*60}{X}")
