# PlotClaw — Sovereign Charting Agent

> *The empire visualizes. Not with tools. With sovereignty.*

---

## Overview

PlotClaw generates **13 chart types** with full styling control, imports data from CSV/JSON files, reads/writes to **shared agent memory**, and **delegates tasks** to other agents in the Clawpack empire. Built on matplotlib + numpy + sympy + scipy.

All model access routes through the **Sovereign Gateway** — every chart generation is audited, budgeted, and constitutionally governed.

---

## Quick Start

/bar sales:45,costs:30,profit:15 --colors red,orange,green --mean --std --theme dark
/pie market:40,30,20,10 --explode 0,0.1,0,0 --donut --theme dark
/plot sin(x),cos(x) --range -6.28,6.28 --legend
/scatter 1,2,3,4,5 2,4,6,8,10 --trendline
/hist 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5 --bins 5
/box 1,2,3,4,5 2,3,4,5,6 3,4,5,6,7 --labels A,B,C
/heatmap 1,2,3;4,5,6;7,8,9 --labels A,B,C --ylabels X,Y,Z --cmap magma --annotate
/polar sin(2*theta) --range 0,6.28 --theme dark
/surface sin(sqrt(x2+y2)) --range -5,5 --cmap magma
/compare A:45,30,25 B:35,40,25 --title Q1vsQ2
/animate sin(x+t) --range -5,5 --frames 30 --fps 10
/stats 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5
/dashboard bar:sales:45,30,15 pie:market:40,30,20,10 line:growth:1,2,4,8,16

text

---

## Data Import
/data # List all CSV/JSON files in the project
/csv sales.csv revenue bar # Bar chart from CSV column
/csv sales.csv profit pie # Pie chart from CSV column
/import data.json # Load JSON file

text

Place CSV files in gents/plotclaw/data/ or project exports/. Format:
`csv
month,revenue,costs,profit
Jan,45,30,15
Feb,52,28,24
Shared Memory & Cross-Agent Communication
PlotClaw participates in the empire-wide shared memory system at shared/shared_data.json:

text
/shared read                             # Read all shared data
/shared read my_key                      # Read specific key
/shared write my_key:my_value            # Write data for other agents
/publish chart_results                   # Quick publish to shared
Delegate tasks to other agents:

text
/delegate docuclaw create a chart analysis report
/delegate interpretclaw translate hello to Spanish
/delegate dataclaw search revenue trends
/delegate webclaw stock market data
/delegate mathematicaclaw derivative of x**2
Universal Flags
All chart types support:

FlagExampleDescription
--theme darkDark backgroundDark mode for all charts
--ylim 0,100Y-axis rangeLock axis limits
--xlim -5,5X-axis rangeLock axis limits
--figsize 12,8Figure dimensionsWidth, height in inches
--dpi 200ResolutionOutput DPI
--fontsize 12Font sizeBase font size
--cmap magmaColor mapviridis, magma, plasma, inferno, coolwarm
--format svgExport formatpng (default), svg, pdf
--save-onlyNo pop-upSave file without opening
--title My ChartChart titleCustom title
--labels A,B,CCustom labelsOverride auto-labels
--colors red,blueCustom colorsNamed or hex colors
--meanMean lineAdd mean reference line
--stdStd dev bandAdd ±1σ shaded band
--legendShow legendMulti-series legend
--annotate text,x,yAnnotationArrow annotation at point
Chart Reference
/bar — Bar Charts
text
/bar 10,20,15,30,25
/bar sales:45,costs:30,profit:15 --colors red,orange,green --mean --std
/bar sales:45,30,15 costs:20,25,10 --stacked
/bar 10,20,15 --horizontal --errors 1,2,0.5
/pie — Pie & Donut Charts
text
/pie 30,20,50
/pie market:40,30,20,10 --explode 0,0.1,0,0 --donut --theme dark
/plot — Mathematical Functions
text
/plot sin(x) --range -10,10
/plot sin(x),cos(x) --range -6.28,6.28 --legend --annotate peak,1.57,1
/plot exp(x) --range 0.1,5 --logy
/plot x**2 --range 1,10 --logx --logy
/scatter — Scatter Plots
text
/scatter 1,2,3,4,5 2,4,6,8,10 --trendline
/hist — Histograms
text
/hist 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5 --bins 5
/box — Box & Whisker Plots
text
/box 1,2,3,4,5 2,3,4,5,6 3,4,5,6,7 --labels A,B,C --horizontal
/heatmap — 2D Heatmaps
text
/heatmap 1,2,3;4,5,6;7,8,9 --labels A,B,C --ylabels X,Y,Z --cmap magma --annotate
/polar — Polar Coordinate Plots
text
/polar sin(2*theta) --range 0,6.28
/polar 1+cos(theta) --range 0,6.28 --theme dark
/surface — 3D Surface Plots
text
/surface sin(sqrt(x**2+y**2)) --range -5,5 --cmap magma
/surface x**2+y**2 --range -3,3 --cmap viridis
/compare — Side-by-Side Comparison
text
/compare A:45,30,25 B:35,40,25 --title Q1vsQ2
/compare Jan:45,30,25 Feb:52,28,24 Mar:48,32,16
/animate — Animated GIF
text
/animate sin(x+t) --range -5,5 --frames 60 --fps 15
/animate sin(x*t) --range -3,3 --frames 40 --fps 10
/stats — Statistical Dashboard
text
/stats 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5
/stats 72,68,75,70,71,69,73,74,68,76,71,70,69,73,72,75
Generates: histogram + box plot + Q-Q normality plot + 14 statistical measures (mean, median, std dev, variance, min/max, Q1/Q3, IQR, skewness, kurtosis).

/dashboard — Multi-Chart Dashboard
text
/dashboard bar:sales:45,30,15 pie:market:40,30,20,10 line:growth:1,2,4,8,16
/dashboard bar:Q1:45,52,48 pie:Q1:40,30,20,10 bar:Q2:55,60,58 --layout 1,3
Architecture
text
plotclaw/
├── agent_handler.py      # A2A handler — routing, delegation, shared I/O
├── data_io.py            # CSV/JSON import, shared memory read/write
├── flags.py              # Universal flag parser + styling helpers
├── commands/
│   ├── bar.py            # Bar charts (horizontal, stacked, error bars)
│   ├── pie.py            # Pie/donut charts
│   ├── plot.py           # Mathematical function plotting (log scale, sympy)
│   ├── scatter.py        # Scatter plots with trendline
│   ├── hist.py           # Histograms
│   ├── box.py            # Box & whisker plots
│   ├── heatmap.py        # 2D heatmaps
│   ├── polar.py          # Polar coordinate plots
│   ├── surface.py        # 3D surface plots
│   ├── compare.py        # Side-by-side comparison
│   ├── animate.py        # Animated GIF generation
│   ├── stats.py          # Statistical analysis dashboard
│   └── dashboard.py      # Multi-chart dashboards
├── data/                 # CSV/JSON data files
└── exports/              # Generated chart files (PNG, SVG, PDF, GIF)
Dependencies
text
pip install matplotlib numpy sympy scipy pillow
Constitutional Compliance
All chart generation is governed by the Clawpack constitution:

Sovereign Gateway: Model access routed through LLMClaw

Audit: Every command logged to Chronicle

Budget: Usage tracked against LLM budget

Enforcement: Import scanner, guarded executor, execution policy apply

Truth Resolver: Chart outputs classified as inference tier

Memory Guard: Inference-tier data never persisted unless confidence > 0.75

Integration
Other agents can call PlotClaw via A2A:

python
result = self.call_agent("plotclaw", "/bar sales:45,30,15 --theme dark")
Or through the delegation registry:

python
from shared.registry import delegate
delegate("docuclaw", "chart", data="sales.csv", type="bar")
*PlotClaw v4 — 13 chart types, CSV import, shared memory, cross-agent delegation. The empire visualizes with sovereignty.*
