# FreeCAD / LibreCAD Commands - Open Source CAD Reference
## Primary Authorities: FreeCAD 0.21+ and LibreCAD 2.2+ Documentation

## FreeCAD Workbenches (Architectural)
| Workbench | Purpose | Source |
|-----------|---------|--------|
| Arch Workbench | Create walls, windows, doors, floors, roofs, stairs, structural elements | https://wiki.freecad.org/Arch_Workbench |
| BIM Workbench | Building Information Modeling: IFC export, material assignments, quantities | https://wiki.freecad.org/BIM_Workbench |
| Draft Workbench | 2D drafting: lines, circles, arcs, dimensions, text, snaps (like AutoCAD LT) | https://wiki.freecad.org/Draft_Workbench |
| Sketcher Workbench | 2D constrained sketching: define geometry with dimensional and geometric constraints | https://wiki.freecad.org/Sketcher_Workbench |
| Part Workbench | Create 3D primitives: box, cylinder, sphere, extrude, revolve, boolean operations | https://wiki.freecad.org/Part_Workbench |
| TechDraw Workbench | Create 2D drawings from 3D models: views, sections, dimensions, annotations | https://wiki.freecad.org/TechDraw_Workbench |
| Spreadsheet Workbench | Parameter tables: drive dimensions from spreadsheet values | https://wiki.freecad.org/Spreadsheet_Workbench |

## FreeCAD Key Commands
| Command | Where | Function | Source |
|---------|-------|----------|--------|
| Wall | Arch WB | Create wall from line, polyline, or sketch; set width, height, alignment | https://wiki.freecad.org/Arch_Wall |
| Window | Arch WB | Insert window into wall; select from presets (fixed, casement, sliding) or create custom | https://wiki.freecad.org/Arch_Window |
| Door | Arch WB | Insert door into wall; set width, height, opening direction | https://wiki.freecad.org/Arch_Door |
| Slab | Arch WB | Create floor/ceiling slab from closed profile; set thickness | https://wiki.freecad.org/Arch_Slab |
| Roof | Arch WB | Create roof from selected face or wire; set pitch angle and overhang | https://wiki.freecad.org/Arch_Roof |
| Stairs | Arch WB | Create staircase from base line; set number of steps, riser height, tread depth, width | https://wiki.freecad.org/Arch_Stairs |
| Structure | Arch WB | Create structural element: column, beam, or slab from profile | https://wiki.freecad.org/Arch_Structure |

## LibreCAD Commands (2D Only)
| Command | Shortcut | Function | Source |
|---------|----------|----------|--------|
| Line | li | Draw line by two points; multiple options: angle, horizontal, vertical, rectangle, parallel through point | https://wiki.librecad.org/ |
| Circle | ci | Center/radius, 2-point, 3-point, center/point on circumference, tangential to 2 or 3 entities | https://wiki.librecad.org/ |
| Arc | ar | 3-point, center/radius/angles, tangential arc, concentric arc | https://wiki.librecad.org/ |
| Dimension | dm | Horizontal, vertical, aligned, radial, diametric, angular dimensions | https://wiki.librecad.org/ |
| Modify | — | Move/copy, rotate, scale, mirror, trim/extend, offset, fillet, chamfer, divide, stretch | https://wiki.librecad.org/ |
| Hatch | ha | Fill area with pattern or solid; select boundary entities | https://wiki.librecad.org/ |
| Block | — | Create block from selection; insert block; explode block; attribute definitions | https://wiki.librecad.org/ |
| Layers | — | Create, rename, freeze/thaw, lock/unlock, set color, linetype, line weight per layer | https://wiki.librecad.org/ |
| Print Preview | — | Preview drawing at plot scale; set paper size and orientation before printing | https://wiki.librecad.org/ |

## FreeCAD/LibreCAD File Formats
| Format | Software | Use | Source |
|--------|----------|-----|--------|
| .FCStd | FreeCAD | Native FreeCAD project file (contains all geometry, constraints, properties) | https://wiki.freecad.org/ |
| .dxf | LibreCAD / FreeCAD | Drawing Exchange Format - universal 2D CAD exchange; LibreCAD native format | https://wiki.librecad.org/ |
| .dwg | — | AutoCAD native format; FreeCAD can import .dwg with external ODA File Converter plugin | https://wiki.freecad.org/ |
| .ifc | FreeCAD (BIM WB) | Industry Foundation Classes - open BIM data exchange standard; export from BIM Workbench | https://wiki.freecad.org/ |
| .stl / .step | FreeCAD | 3D mesh/solid export for 3D printing or CAM manufacturing | https://wiki.freecad.org/ |
| .svg | Both | Scalable Vector Graphics export for presentation; can also export to .pdf | https://wiki.freecad.org/ |
