# AutoCAD 3D Modeling Commands
## Primary Authority: Autodesk AutoCAD 2025

## Viewing 3D Models
| Command | Function | Source |
|---------|----------|--------|
| 3DORBIT | Free orbit around model. Click and drag to rotate. Right-click menu for constrained orbit, continuous orbit, and preset views | https://help.autodesk.com/view/ACD/2025/ENU/ |
| VIEW | Save and restore named views. Set up Top, Front, Right, Isometric views for quick navigation | https://help.autodesk.com/view/ACD/2025/ENU/ |
| VISUALSTYLES | VS | Set display style: 2D Wireframe, Conceptual, Realistic, X-Ray. Use Conceptual for client presentation, Wireframe for working | https://help.autodesk.com/view/ACD/2025/ENU/ |
| UCS | Set user coordinate system. Align XY plane with face of 3D object (UCS > Face). UCS > World resets to WCS. Essential for drawing on non-orthogonal faces | https://help.autodesk.com/view/ACD/2025/ENU/ |
| NAVVCUBE | Display/view control cube for switching between standard and isometric views with one click | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Solid Modeling Commands
| Command | Function | Source |
|---------|----------|--------|
| BOX | Create 3D solid box. Specify corners and height. Foundation blocks, simple buildings | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXTRUDE | EXTRUDE or EXT | Extend 2D shape (closed polyline, circle, region) into 3D solid. Draw wall profile, extrude to height. Essential command: draw floor plan outline as polyline, extrude to wall height | https://help.autodesk.com/view/ACD/2025/ENU/ |
| REVOLVE | REV | Revolve 2D profile around axis to create 3D solid. Use for turned parts, columns, circular stairs | https://help.autodesk.com/view/ACD/2025/ENU/ |
| SWEEP | Sweep 2D shape along 3D path. Use for piping, railings, moldings along curved path | https://help.autodesk.com/view/ACD/2025/ENU/ |
| LOFT | Create 3D solid by blending between cross-sections. Use for complex organic shapes, terrain, hull forms | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PRESSPULL | Press or pull bounded area to create 3D solid or void. CTRL+click to select bounded area on 3D solid face. Use for window/door openings in walls: draw rectangle on face, presspull inward | https://help.autodesk.com/view/ACD/2025/ENU/ |
| UNION | UNI | Combine two or more 3D solids into single solid. Use after building wall segments to create monolithic building | https://help.autodesk.com/view/ACD/2025/ENU/ |
| SUBTRACT | SU | Subtract one solid from another. Draw wall as solid, subtract door/window solids to create openings | https://help.autodesk.com/view/ACD/2025/ENU/ |
| INTERSECT | IN | Create solid from intersection of two or more solids. Use for complex joint details | https://help.autodesk.com/view/ACD/2025/ENU/ |
| SLICE | SL | Cut 3D solid along plane. Define plane by 3 points, planar object, surface, or Z axis. Use for section cuts through buildings | https://help.autodesk.com/view/ACD/2025/ENU/ |
| SECTIONPLANE | Create section object that generates 2D cross-section from 3D model. Generate 2D block from section for detailing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| FILLETEDGE | Apply rounded edges to 3D solids. Select edges, enter radius. Use for counter edges, furniture, aesthetic softening | https://help.autodesk.com/view/ACD/2025/ENU/ |
| CHAMFEREDGE | Apply beveled edges to 3D solids. Select edges, enter distances. Use for chamfered concrete edges, mechanical parts | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Converting 2D to 3D Workflow (Architectural)
| Step | Commands | Source |
|------|----------|--------|
| 1. Draw floor plan in 2D | LINE, PLINE, OFFSET, TRIM - standard 2D commands | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 2. Join walls into closed polylines | PEDIT > Join > select all lines forming closed loop | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 3. Extrude walls to height | EXTRUDE > select all wall polylines > enter height (e.g., 9' for 9-foot walls) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 4. Create door/window openings | Draw rectangle on wall face. PRESSPULL inward to create opening | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 5. Add floor slab | Draw slab outline. EXTRUDE to slab thickness (6") | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 6. Add roof | Draw roof profile. EXTRUDE or LOFT between ridge and eave profiles | https://help.autodesk.com/view/ACD/2025/ENU/ |
| 7. Generate 2D elevations | SECTIONPLANE from front/back/sides. Generate 2D block for annotation | https://help.autodesk.com/view/ACD/2025/ENU/ |
