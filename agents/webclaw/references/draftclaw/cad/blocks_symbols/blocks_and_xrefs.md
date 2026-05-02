# Blocks and Symbol Libraries - Reference
## Creating and managing reusable drawing components

## Block Commands
| Command | Shortcut | Function | Source |
|---------|----------|----------|--------|
| BLOCK | B | Create block definition from selected objects within current drawing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| WBLOCK | W | Write block to external .dwg file (creates standalone block library file) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| INSERT | I | Insert block or drawing into current drawing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| BEDIT | BE | Open Block Editor to modify block definition (all instances update) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ATTDEF | ATT | Define attribute definition (text fields that can vary per block instance) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EATTEDIT | — | Edit attribute values in Enhanced Attribute Editor | https://help.autodesk.com/view/ACD/2025/ENU/ |
| BATTMAN | — | Block Attribute Manager: edit attribute order and properties | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ATTSYNC | — | Synchronize block attributes when definition changes | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXPLODE | X | Break block into component objects (loses block intelligence) | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Standard Architectural Block Library Contents
| Block | Should Include | Source |
|-------|---------------|--------|
| Door (single swing) | Door panel, swing arc (90 degrees), frame lines. Dynamic: stretchable width and flip direction. | https://www.nationalcadstandard.org/ |
| Door (double) | Two panels, both swing arcs. Dynamic: equal or unequal leaf widths. | https://www.nationalcadstandard.org/ |
| Window (plan view) | Three parallel lines, sill line offset from wall face. Dynamic: stretchable width. | https://www.nationalcadstandard.org/ |
| Toilet | Bowl outline, tank, seat. Top view plan symbol. | https://www.nationalcadstandard.org/ |
| Sink/Lavatory | Bowl outline with drain circle. Top view plan symbol. | https://www.nationalcadstandard.org/ |
| Bathtub | Rectangular outline with curved end. Standard 5'-0" x 2'-6" or 5'-0" x 3'-0". | https://www.nationalcadstandard.org/ |
| Shower | Square outline with diagonal drain lines. 36" x 36" minimum. | https://www.nationalcadstandard.org/ |
| Stair (straight run) | Tread lines with directional arrow and "DN" or "UP" label. | https://www.nationalcadstandard.org/ |
| Kitchen sink (double bowl) | Two rectangular bowls with drain circles and faucet dot. | https://www.nationalcadstandard.org/ |
| Range/Stove | Rectangular outline with burner circles. 30" wide standard. | https://www.nationalcadstandard.org/ |
| Refrigerator | Rectangular outline with dashed door swing area in front. 36" wide standard. | https://www.nationalcadstandard.org/ |
| Title block | Project name, client, address, date, scale, drawn by, checked by, sheet number, revision block with attributes. | https://www.nationalcadstandard.org/ |
| North arrow | Arrow pointing north with "N" label; dynamic rotation. | https://www.nationalcadstandard.org/ |
| Graphic scale | Bar scale with alternating black/white segments; labeled with feet/meters. | https://www.nationalcadstandard.org/ |

## Dynamic Block Capabilities
| Property | What It Does | Source |
|----------|-------------|--------|
| Linear stretch | Stretch object within defined range (door width, window width) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Flip | Mirror object about axis (door swing direction) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Visibility | Toggle between different block states (elevation vs. plan vs. section view) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Array | Repeat object at defined spacing (stair treads, parking stalls) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Rotate | Rotate object within block (north arrow orientation) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Lookup table | Select from predefined sizes (e.g., door widths: 2'-6", 2'-8", 3'-0") | https://help.autodesk.com/view/ACD/2025/ENU/ |

## External References (XREFs)
| Command | Function | Source |
|---------|----------|--------|
| XATTACH (XA) | Attach external DWG as reference (backgrounds, site plans, structural grids) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| XREF | Open External References palette to manage attachments | https://help.autodesk.com/view/ACD/2025/ENU/ |
| XCLIP | Clip XREF to defined boundary (show only portion of referenced drawing) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| REFEDIT | Edit XREF in-place within host drawing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| NCOPY | Copy objects from XREF into current drawing | https://help.autodesk.com/view/ACD/2025/ENU/ |
