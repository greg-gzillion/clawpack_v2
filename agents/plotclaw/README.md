# PlotClaw — Charting Agent

13 chart types with CSV import, shared memory I/O, and cross-agent delegation.
Built on matplotlib + numpy + sympy + scipy.

## Quick Start

/bar sales:45,costs:30,profit:15 --colors red,orange,green --mean --std --theme dark
/pie market:40,30,20,10 --explode 0,0.1,0,0 --donut --theme dark
/plot sin(x),cos(x) --range -6.28,6.28 --legend
/scatter 1,2,3,4,5 2,4,6,8,10 --trendline
/hist 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5 --bins 5
/box 1,2,3,4,5 2,3,4,5,6 3,4,5,6,7 --labels A,B,C
/heatmap 1,2,3;4,5,6;7,8,9 --labels A,B,C --ylabels X,Y,Z --cmap magma --annotate
/polar sin(2*theta) --range 0,6.28
/surface sin(sqrt(x**2+y**2)) --range -5,5 --cmap magma
/compare A:45,30,25 B:35,40,25 --title Q1vsQ2
/animate sin(x+t) --range -5,5 --frames 30 --fps 10
/stats 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5
/dashboard bar:sales:45,30,15 pie:market:40,30,20,10 line:growth:1,2,4,8,16

## Data Import

Place CSV files in agents/plotclaw/data/ or project exports/.

/data                                    # List available CSV/JSON files
/csv sales.csv revenue bar               # Bar chart from CSV column
/csv sales.csv profit pie                # Pie chart from CSV column

CSV format:
month,revenue,costs,profit
Jan,45,30,15
Feb,52,28,24

## Shared Memory & Delegation

/shared read                             # Read all shared data
/shared write key:value                  # Write for other agents
/delegate interpretclaw translate hello to Spanish
/delegate docuclaw create analysis report

## Universal Flags

--theme dark        Dark mode
--ylim 0,100        Y-axis range
--figsize 12,8      Figure dimensions
--dpi 200           Resolution
--fontsize 12       Base font size
--cmap magma        Color map (viridis, magma, plasma, inferno, coolwarm)
--format svg        Export format (png, svg, pdf)
--save-only         Save without opening
--title My Chart    Custom title
--labels A,B,C      Custom labels
--colors red,blue   Custom colors

## Architecture

plotclaw/
  agent_handler.py    A2A routing, delegation, shared I/O
  data_io.py          CSV/JSON import, shared memory
  flags.py            Universal flag parser
  commands/           13 chart type modules
  data/               CSV/JSON files
  exports/            Generated charts

## Dependencies

pip install matplotlib numpy sympy scipy pillow
