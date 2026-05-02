# PlotClaw — Charting Agent

13 chart types. CSV import. Shared memory. Cross-agent delegation.
Built on matplotlib + numpy + sympy + scipy.

## Quick Start

/bar sales:45,costs:30,profit:15 --colors red,orange,green --mean --std --theme dark
/pie market:40,30,20,10 --explode 0,0.1,0,0 --donut --theme dark
/plot sin(x),cos(x) --range -6.28,6.28 --legend
/scatter 1,2,3,4,5 2,4,6,8,10 --trendline
/hist 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5 --bins 5
/box 1,2,3,4,5 2,3,4,5,6 3,4,5,6,7 --labels A,B,C
/heatmap 1,2,3;4,5,6;7,8,9 --cmap magma --annotate
/polar sin(2*theta) --range 0,6.28
/surface sin(sqrt(x**2+y**2)) --range -5,5 --cmap magma
/compare A:45,30,25 B:35,40,25
/animate sin(x+t) --range -5,5 --frames 30 --fps 10
/stats 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5
/dashboard bar:sales:45,30,15 pie:market:40,30,20,10 line:growth:1,2,4,8,16

## Agent Contract

PlotClaw accepts both CLI strings (human) and structured dicts (agent).
The canonical payload contract is defined in [SPEC.md](SPEC.md).

`python
# Agent-to-agent call
result = call_agent("plotclaw", {
    "type": "bar",
    "series": [{"label": "Sales", "values": [45, 30, 25]}],
    "flags": {"theme": "dark", "mean": True}
})
Data & Delegation
/data # List CSV/JSON files
/csv sales.csv revenue bar # Chart from CSV
/shared read # Read shared memory
/shared write key:value # Write shared memory
/delegate interpretclaw <task> # Delegate to other agents

Architecture
plotclaw/
schema.py Constitutional payload spec + validator
SPEC.md Frozen payload contract v1.0
agent_handler.py A2A routing, delegation, shared I/O
data_io.py CSV/JSON import, shared memory
commands/ 13 chart type modules (v5 dual interface)
data/ CSV/JSON files
exports/ Generated charts (PNG/SVG/PDF/GIF)

Dependencies
pip install matplotlib numpy sympy scipy pillow
