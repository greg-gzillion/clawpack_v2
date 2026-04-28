# DraftClaw

Technical drawings, blueprints, CAD schematics, and circuit diagrams with PIL image generation.

## Commands

| Command | Description |
|---------|-------------|
| `/blueprint <specs>` | Generate PIL blueprint image + auto-save PNG |
| `/floorplan <rooms>` | Same as /blueprint |
| `/cad <specs>` | Generate CAD/schematic with measurements (ASCII) |
| `/schematic <specs>` | Same as /cad |
| `/circuit <design>` | Circuit/wiring diagram with component specs |
| `/wiring <design>` | Same as /circuit |
| `/specs <project>` | Technical specifications with dimensions and tolerances |
| `/export <fmt> <content>` | Export via FileClaw (21 formats) |
| `/help` | Show commands |
| `/stats` | Show statistics |

## Quick Start
/blueprint apartment layout 30x40 with kitchen bedroom bathroom
/cad mechanical gear assembly with 4 gears
/circuit LED strip controller with Arduino
/specs conference table with cable management

text

## Output

- **Blueprints**: PNG images generated with PIL, saved to `exports/`
- **CAD Schematics**: ASCII diagrams with measurements, material specs, assembly notes
- **Circuits**: ASCII diagrams with component specifications, current budgets, connection tables
- **Specifications**: Professional-grade technical documents with tolerances, standards, assembly instructions

## File Structure
agents/draftclaw/
├── agent_handler.py # A2A handler
├── commands/
│ └── blueprint.py # PIL blueprint generation
├── core/ # Core engine
├── exports/ # Generated blueprints
└── providers/ # External services

text

## A2A Integration

```python
self.call_agent("draftclaw", "/blueprint office floorplan 40x60")
self.call_agent("draftclaw", "/cad mechanical gear assembly")
self.call_agent("draftclaw", "/circuit Arduino LED controller")