# AutoCAD 2D Commands - Reference
## Primary Authority: Autodesk AutoCAD 2025 Official Documentation

## Drawing Commands
| Command | Shortcut | Function | Source |
|---------|----------|----------|--------|
| LINE | L | Draw straight line segments | https://help.autodesk.com/view/ACD/2025/ENU/ |
| POLYLINE | PL | Connected line and arc segments as single object | https://help.autodesk.com/view/ACD/2025/ENU/ |
| RECTANGLE | REC | Draw rectangle by two opposite corners | https://help.autodesk.com/view/ACD/2025/ENU/ |
| CIRCLE | C | Center point radius; or 3P, 2P, TTR methods | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ARC | A | 3-point default; Start-Center-End, Start-End-Radius | https://help.autodesk.com/view/ACD/2025/ENU/ |
| HATCH | H | Fill enclosed area with pattern (ANSI31, AR-CONC, EARTH) | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Modify Commands
| Command | Shortcut | Function | Source |
|---------|----------|----------|--------|
| ERASE | E | Delete selected objects | https://help.autodesk.com/view/ACD/2025/ENU/ |
| COPY | CO | Copy objects with base point displacement | https://help.autodesk.com/view/ACD/2025/ENU/ |
| MIRROR | MI | Mirror objects about a line (great for symmetrical plans) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| OFFSET | O | Create parallel copy at specified distance (walls, property lines) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ARRAY | AR | Rectangular, polar, or path array of objects | https://help.autodesk.com/view/ACD/2025/ENU/ |
| MOVE | M | Move objects from base point to destination | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ROTATE | RO | Rotate objects by angle about base point | https://help.autodesk.com/view/ACD/2025/ENU/ |
| SCALE | SC | Scale objects by factor (12 for inches to feet, 25.4 for inches to mm) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| TRIM | TR | Trim objects to cutting edges | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXTEND | EX | Extend objects to boundary edges | https://help.autodesk.com/view/ACD/2025/ENU/ |
| BREAK | BR | Break object at one or two points | https://help.autodesk.com/view/ACD/2025/ENU/ |
| JOIN | J | Join separate objects into one (lines, arcs, polylines) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| FILLET | F | Rounded corner with specified radius (zero for sharp corner) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| CHAMFER | CHA | Beveled corner with two distances | https://help.autodesk.com/view/ACD/2025/ENU/ |
| STRETCH | S | Move objects within crossing window, stretching connected lines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXPLODE | X | Break complex objects into components (blocks, polylines, dimensions) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PEDIT | PE | Edit polyline: close, open, join, width, fit curve, spline | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Object Snaps (OSNAP) - Essential for Precision
| Snap Mode | Shortcut | Snaps To | Source |
|-----------|----------|----------|--------|
| ENDpoint | END | Endpoint of lines, arcs, polylines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| MIDpoint | MID | Midpoint of lines and arcs | https://help.autodesk.com/view/ACD/2025/ENU/ |
| CENter | CEN | Center point of circles, arcs, ellipses | https://help.autodesk.com/view/ACD/2025/ENU/ |
| INTersection | INT | Intersection of any two objects | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PERpendicular | PER | Point perpendicular to line, arc, or circle | https://help.autodesk.com/view/ACD/2025/ENU/ |
| TANgent | TAN | Point tangent to arc or circle | https://help.autodesk.com/view/ACD/2025/ENU/ |
| NEArest | NEA | Nearest point on any object | https://help.autodesk.com/view/ACD/2025/ENU/ |
| QUAdrant | QUA | 0, 90, 180, 270 degree points on circles/arcs | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Dimension Commands
| Command | Shortcut | Function | Source |
|---------|----------|----------|--------|
| DIMLINEAR | DLI | Horizontal or vertical dimension | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMALIGNED | DAL | Dimension parallel to angled object | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMANGULAR | DAN | Dimension angle between two lines | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMRADIUS | DRA | Radius dimension (R prefix) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMDIAMETER | DDI | Diameter dimension (0 prefix) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMCONTINUE | DCO | Continue from previous dimension | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DIMBASELINE | DBA | Stacked dimensions from common baseline | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Inquiry and Utility Commands
| Command | Function | Source |
|---------|----------|--------|
| DIST (DI) | Measure distance and angle between two points | https://help.autodesk.com/view/ACD/2025/ENU/ |
| AREA (AA) | Calculate area and perimeter of objects or defined points | https://help.autodesk.com/view/ACD/2025/ENU/ |
| LIST (LI) | Display properties of selected objects (layer, length, area) | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ID | Display coordinates of a point | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PROPERTIES (PR) | Open Properties palette for detailed object editing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| MATCHPROP (MA) | Match properties from source object to destination | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PURGE (PU) | Remove unused layers, blocks, styles, linetypes from drawing | https://help.autodesk.com/view/ACD/2025/ENU/ |
| AUDIT | Check and repair drawing file integrity | https://help.autodesk.com/view/ACD/2025/ENU/ |
