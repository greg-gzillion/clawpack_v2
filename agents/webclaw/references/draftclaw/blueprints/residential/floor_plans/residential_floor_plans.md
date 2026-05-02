# Residential Floor Plan Drafting Standards
## How to draw single-family and multi-family residential floor plans

## Drawing Scale and Sheet Size (per NCS)
| Drawing Type | Scale | Sheet Size | Source |
|-------------|-------|-----------|--------|
| Floor plan | 1/4" = 1'-0" | ARCH D (24" x 36") for full house, ARCH B (12" x 18") for small plans | https://www.nationalcadstandard.org/ |
| Enlarged kitchen/bath | 1/2" = 1'-0" | Same as floor plan or detail sheet | https://www.nationalcadstandard.org/ |
| Foundation/basement plan | 1/4" = 1'-0" | Same as floor plan | https://www.nationalcadstandard.org/ |
| Roof plan | 1/8" = 1'-0" | ARCH D for complex roofs | https://www.nationalcadstandard.org/ |

## Floor Plan Layer Standards (per NCS)
| Layer | Content | Line Weight | Source |
|-------|---------|------------|--------|
| A-FLOR-WALL | Walls (exterior and interior) | 0.5mm (thick) for cut elements | https://www.nationalcadstandard.org/ |
| A-FLOR-DOOR | Doors and door swings | 0.35mm (medium) | https://www.nationalcadstandard.org/ |
| A-FLOR-GLAZ | Windows and glazing | 0.25mm (thin) | https://www.nationalcadstandard.org/ |
| A-FLOR-FIXT | Plumbing fixtures and casework | 0.25mm (thin) | https://www.nationalcadstandard.org/ |
| A-FLOR-STRS | Stairs with directional arrow | 0.35mm (medium) | https://www.nationalcadstandard.org/ |
| A-ANNO-DIMS | Dimensions | 0.18mm (fine) | https://www.nationalcadstandard.org/ |
| A-ANNO-TEXT | Room labels, notes | 0.25mm (thin) | https://www.nationalcadstandard.org/ |

## Wall Drawing Conventions
| Wall Type | How to Draw | Notes | Source |
|-----------|------------|-------|--------|
| Exterior 2x6 wall | Two parallel lines 6" apart (at 1/4" scale = 1/8" gap). Solid hatch or dark fill between lines. | R-19 or R-21 batt insulation + R-5 continuous exterior insulation minimum per IECC | https://codes.iccsafe.org/content/IRC2021P1 |
| Interior bearing wall (2x4) | Two parallel lines 4" apart. Lighter fill than exterior. | No hatch needed unless rated assembly | https://codes.iccsafe.org/content/IRC2021P1 |
| Interior partition (2x4) | Two parallel lines 4" apart. No fill. | Lightest weight lines | https://codes.iccsafe.org/content/IRC2021P1 |
| Plumbing wall (2x6) | Two parallel lines 6" apart. Note "2x6 PLUMBING WALL" | Required for 3" drain pipes with fittings | https://codes.iccsafe.org/content/IRC2021P1 |
| Rated wall (1-hour) | Two parallel lines with diamond hatching between. Note "1-HR RATED" | Required between garage and dwelling; between dwelling units in multi-family | https://codes.iccsafe.org/content/IRC2021P1 |

## Door and Window Symbols
| Element | Symbol | Label | Source |
|---------|--------|-------|--------|
| Interior door (swing) | Opening in wall (2'-6", 2'-8", 3'-0") with 90-degree arc showing swing direction | Door number (D01, D02) with size | https://www.nationalcadstandard.org/ |
| Exterior door (swing) | Same as interior, thicker line for door panel | Label with type and size | https://www.nationalcadstandard.org/ |
| Sliding glass door | Narrow rectangle in wall with arrow showing slide direction | "36" x 80" SLIDING DOOR" or similar | https://www.nationalcadstandard.org/ |
| Bifold/Pocket door | Accordion symbol or dashed line for pocket | "BIFOLD" or "POCKET" noted | https://www.nationalcadstandard.org/ |
| Double-hung window | Three parallel lines in wall | Window type per schedule (W01, W02) | https://www.nationalcadstandard.org/ |
| Casement window | Three lines with arrow showing swing direction | Window type per schedule | https://www.nationalcadstandard.org/ |
| Fixed window | Three lines, no arrow | Window type per schedule | https://www.nationalcadstandard.org/ |

## Dimension String Order (from wall outward)
| String | What It Shows | Source |
|--------|--------------|--------|
| 1st string (closest to plan) | Interior partition locations, door/window openings, plumbing wall centers | https://www.nationalcadstandard.org/ |
| 2nd string | Overall room dimensions (face of stud to face of stud) | https://www.nationalcadstandard.org/ |
| 3rd string (furthest out) | Overall exterior dimensions including wall thicknesses | https://www.nationalcadstandard.org/ |

## Room Label Format
| Label Element | Example | Source |
|--------------|---------|--------|
| Room name | "LIVING ROOM" (all caps, architectural lettering) | https://www.nationalcadstandard.org/ |
| Room dimensions | 15'-4" x 20'-6" (width x length, face of stud) | https://www.nationalcadstandard.org/ |
| Floor area | "(307 SQ FT)" in parentheses below dimensions | https://www.nationalcadstandard.org/ |
| Ceiling height | "CLG: 9'-0" AFF" if different from typical | https://www.nationalcadstandard.org/ |
| Floor finish | "WOOD FLOORING" or "TILE" note in finish schedule | https://www.nationalcadstandard.org/ |

## Common Residential Room Size Targets
| Room | Typical Dimensions | Drawing Note | Source |
|------|-------------------|-------------|--------|
| Great room / Family room | 18' x 22' to 22' x 28' | "FAMILY ROOM" | https://www.nahb.org/ |
| Kitchen | 10' x 12' to 14' x 18' (not including eating area) | Show work triangle dimension | https://nkba.org/ |
| Primary bedroom | 14' x 16' to 16' x 20' | Show king bed dashed block for furniture layout | https://www.nahb.org/ |
| Secondary bedroom | 10' x 12' to 12' x 14' | Show twin or full bed dashed block | https://www.nahb.org/ |
| Primary bathroom | 8' x 10' to 10' x 14' | Show 5' turning radius for accessibility | https://nkba.org/ |
| Secondary bathroom | 5' x 8' to 6' x 10' | Minimum 30" x 30" shower compartment | https://codes.iccsafe.org/content/IRC2021P1 |
| Laundry room | 6' x 8' to 8' x 10' | Show washer/dryer with 36" clearance in front | https://www.nahb.org/ |
| Garage (2-car) | 20' x 20' to 22' x 24' | Show overhead door symbol and concrete approach apron | https://www.nahb.org/ |
