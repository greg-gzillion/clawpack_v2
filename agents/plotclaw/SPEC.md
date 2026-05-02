# PlotClaw Constitutional Payload Spec v1

> *Law. Not suggestion. The contract between agents and the charting engine.*

---

## Canonical Payload

Every PlotClaw command accepts this structure. Schema validation at schema.py enforces it before any matplotlib execution.

`json
{
  "type": "bar",
  "intent": "generate_chart",
  "task_type": "code_generation",
  "confidence": 1.0,
  "source": "user",
  
  "series": [
    {"label": "Sales", "values": [45, 30, 25], "errors": [2.0, 1.5, 3.0]}
  ],
  
  "flags": {
    "title": "Chart Title",
    "theme": "default",
    "format": "png",
    "save_only": false,
    "dpi": 150,
    "fontsize": 11,
    "figsize": [10, 6]
  }
}
Required Fields
FieldTypeDescription
typestringChart type: bar, pie, plot, scatter, hist, box, heatmap, polar, surface, compare, animate, stats, dashboard
intentstringAlways "generate_chart" — for Truth Resolver routing
task_typestring"code_generation" — for LLM Router provider selection
confidencefloat0.0–1.0 — for Memory Guard persistence check
sourcestring"user", "agent", "csv", or "shared"
Data Fields (one required per chart type)
Chart TypeRequired FieldStructure
barseries[{"label": str, "values": [float], "errors": [float]?}]
pieseries[{"label": str, "values": [float]}]
plotexpressions["sin(x)", "cos(x)"]
scatterx_values, y_values[float], [float]
histvalues[float]
boxdatasets[[float], [float], ...]
heatmapmatrix[[float, float, ...], ...]
polarexpressions["sin(2*theta)"]
surfaceexpressions["sin(sqrt(x**2+y**2))"]
compareseries[{"label": str, "values": [float]}]
animateexpressions["sin(x+t)"]
statsvalues[float]
dashboardcharts[{"type": str, "label": str, "values": [float]}]
Flags (all optional)
FlagTypeDefaultApplies To
titlestringChart type nameAll
theme"default" | "dark""default"All
format"png" | "svg" | "pdf" | "gif""png"All
save_onlyboolfalseAll
dpiint150All
fontsizeint11All
figsize[float, float][10, 6]All
xlabelstring""bar, plot, scatter, hist
ylabelstring"Value"bar, plot, scatter, hist
ylim[float, float]autobar, scatter, hist, box, plot
xlim[float, float]autobar, scatter, hist, plot
colors[string]auto-palettebar
cmapstring"viridis"heatmap, surface
meanboolfalsebar
stdboolfalsebar
horizontalboolfalsebar, box
stackedboolfalsebar
donutboolfalsepie
explode[float][0, ...]pie
legendboolfalseplot
logxboolfalseplot
logyboolfalseplot
range[float, float][-10, 10]plot, polar, surface, animate
trendlineboolfalsescatter
binsint10hist
annotate{"text": str, "x": float, "y": float}noneplot, heatmap
framesint50animate
fpsint10animate
layout[int, int]autodashboard
Validation
All payloads pass through schema.validate() before execution:

python
from schema import validate

result = validate(payload)
if not result["valid"]:
    return f"[FAIL] Schema: {result['error']}"

execute(result["payload"])
Backward Compatibility
CLI strings are preserved as the human interface. cli_to_payload() converts them to the canonical dict before validation:

text
Human:  /bar sales:45,costs:30 --theme dark
          ↓ cli_to_payload()
Agent:  {"type":"bar","series":[...],"flags":{...}}
          ↓ schema.validate()
Engine: matplotlib figure
Constitutional Principles Enforced
PrincipleHow
AuditStructured payload → deterministic Chronicle logging
BudgetExplicit type field for cost classification
Truth Resolverintent field for inference tier routing
Memory Guardconfidence field validates persistence eligibility
EnforcementSchema validation before any side effects
Version 1.0 — Frozen. Changes require constitutional amendment.
