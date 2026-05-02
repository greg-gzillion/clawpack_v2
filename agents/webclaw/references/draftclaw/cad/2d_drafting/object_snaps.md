# AutoCAD Object Snaps and Precision Drawing
## Primary Authority: Autodesk AutoCAD 2025

## Object Snap Modes (OSNAP) - how to precisely snap to geometry
| Snap | Abbreviation | Function | Use Case | Source |
|------|-------------|----------|----------|--------|
| ENDpoint | END | Snaps to closest endpoint of line, arc, polyline segment | Connecting walls at corners; starting dimension extension lines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| MIDpoint | MID | Snaps to midpoint of line, arc, polyline segment | Centering doors in walls; finding center of room wall | https://help.autodesk.com/view/ACD/2025/ENU/ |
| INTersection | INT | Snaps to intersection of two objects | Wall intersections; column grid intersections | https://help.autodesk.com/view/ACD/2025/ENU/ |
| APParent Intersection | APP | Snaps to apparent intersection of objects that don't physically cross (different Z elevations or 2D appearance) | 2D drawings where lines cross visually but not in 3D | https://help.autodesk.com/view/ACD/2025/ENU/ |
| CENter | CEN | Snaps to center of circle, arc, ellipse | Locating column centers; bolt circle centers in mechanical | https://help.autodesk.com/view/ACD/2025/ENU/ |
| QUAdrant | QUA | Snaps to 0, 90, 180, 270 degree points on circle or arc | Drawing lines tangent to circle edges | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PERpendicular | PER | Snaps to point perpendicular to selected object | Drawing walls perpendicular to existing wall; dimension lines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| TANgent | TAN | Snaps to point of tangency on circle or arc | Drawing lines tangent to arcs or circles; mechanical detailing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| NEArest | NEA | Snaps to nearest point on object | Quick snapping when precision not critical | https://help.autodesk.com/view/ACD/2025/ENU/ |
| NODE | NOD | Snaps to point object (POINT command or dimension definition points) | Locating survey points, grid intersection points | https://help.autodesk.com/view/ACD/2025/ENU/ |
| INSertion | INS | Snaps to insertion point of block, text, or attribute | Placing blocks precisely; aligning text | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXTension | EXT | Displays temporary extension line from endpoint; allows drawing from projected location | Aligning walls across openings; extending lines to meet imaginary intersection | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PARallel | PAR | Snaps parallel to selected line; shows temporary parallel alignment path | Drawing walls parallel to existing walls | https://help.autodesk.com/view/ACD/2025/ENU/ |
| FROm | FRO | Establishes temporary reference point for next point entry. Use with other snaps: "FROM END, @5'<0" means 5 feet right of endpoint | Placing objects at offset from known point without construction lines | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Running Object Snaps vs. Temporary Overrides
| Setting | How to Use | Source |
|---------|-----------|--------|
| Running OSNAPs | OSNAP command or F3 key. Select snaps that remain active: END, MID, INT, CEN for architectural work | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Temporary override | Hold SHIFT + right-click during command. Single-use snap overrides running snaps. SHIFT+E for ENDpoint, SHIFT+V for MIDpoint | https://help.autodesk.com/view/ACD/2025/ENU/ |
| OSNAP tracking (F11) | Displays alignment paths from acquired snap points. Essential for aligning without construction lines | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Polar Tracking and Ortho Mode
| Mode | Key | Function | Use Case | Source |
|------|-----|----------|----------|--------|
| ORTHO | F8 | Restricts cursor to 0, 90, 180, 270 degrees | Drawing perfectly horizontal/vertical walls; dimension lines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| POLAR | F10 | Restricts cursor to specified angle increments. Set additional angles for roof pitches (e.g., 33.69 degrees for 8:12 pitch) | Drawing at specific angles: 45 degrees for isometric, 30/60 for mechanical | https://help.autodesk.com/view/ACD/2025/ENU/ |
| POLAR tracking | F10 with tracking | Shows alignment path with distance and angle from acquired points | Locating points by distance and angle without construction lines | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Coordinate Entry Methods
| Method | Format | Example | Source |
|--------|--------|---------|--------|
| Absolute coordinates | X,Y | 10',15' Draws from origin (0,0) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Relative coordinates | @X,Y | @10',0 Draws 10 feet right from last point | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Relative polar | @distance<angle | @20'<45 Draws at 45-degree angle, 20 feet from last point | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Direct distance entry | Move cursor in desired direction (ORTHO or POLAR), type distance, Enter | Point ortho right, type 10', Enter = 10-foot horizontal line | https://help.autodesk.com/view/ACD/2025/ENU/ |
