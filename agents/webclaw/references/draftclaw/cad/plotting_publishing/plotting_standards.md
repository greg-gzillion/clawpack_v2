# Plotting and Publishing Standards
## How to set up sheets, plot styles, and publish drawing sets

## Paper Space (Layout) Setup
| Element | Standard | Source |
|---------|----------|--------|
| Layout tabs | One per sheet: "A-101 FIRST FLOOR", "A-201 RCP", "A-301 ELEVATIONS" | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Page setup manager | Right-click layout tab → Page Setup Manager or PAGESETUP command | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Sheet size | ARCH D (24" x 36") for full size, ARCH B (12" x 18") for half size, ANSI D (22" x 34") for engineering | https://www.nationalcadstandard.org/ |
| Plot scale (viewport) | 1/4" = 1'-0" = 1:48 (standard architectural); 1/8" = 1'-0" = 1:96 (commercial plans) | https://www.nationalcadstandard.org/ |
| Viewport lock | Lock viewport after setting scale to prevent accidental zoom changes | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Annotation scale | Set to match viewport scale so text, dimensions, and symbols appear at correct plotted size | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Plot Style Tables (CTB/STB)
| Setting | Standard | Source |
|---------|----------|--------|
| Line weights (NCS) | 0.18mm (fine), 0.25mm (thin), 0.35mm (medium), 0.50mm (thick), 0.70mm (very thick) | https://www.nationalcadstandard.org/ |
| Color-dependent (CTB) | Red (1) = 0.18mm, Yellow (2) = 0.25mm, Green (3) = 0.35mm, Cyan (4) = 0.50mm, Blue (5) = 0.70mm (typical office standard) | Firm-dependent; NCS provides guidance |
| Screening | 100% for new work, 50% for existing to remain, 25% for backgrounds/XREFs | Standard architectural convention |
| Monochrome plotting | All colors plot black with line weights controlling emphasis (most common for construction documents) | https://www.nationalcadstandard.org/ |
| Color plotting | Used for presentation drawings, color-coded plans (zoning, life safety, finishes) | Firm preference |

## PDF/DWF Publishing
| Command | Function | Source |
|---------|----------|--------|
| PLOT (Ctrl+P) | Plot single layout to PDF, DWF, or physical printer | https://help.autodesk.com/view/ACD/2025/ENU/ |
| PUBLISH | Batch plot multiple layouts to single PDF or plotter | https://help.autodesk.com/view/ACD/2025/ENU/ |
| EXPORTPDF | Export drawing directly to PDF without page setup | https://help.autodesk.com/view/ACD/2025/ENU/ |
| ETRANSMIT | Package drawing with all dependencies (XREFs, fonts, plot styles, images) for sending to consultants | https://help.autodesk.com/view/ACD/2025/ENU/ |
| DWG to PDF.pc3 | Standard AutoCAD PDF driver; produces vector PDF with layer information | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Sheet Set Manager
| Feature | Function | Source |
|---------|----------|--------|
| Sheet Set (DST file) | Organize all sheets in a project: cover sheet, plans, elevations, sections, details | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Sheet numbering | Auto-increment sheet numbers; reference other sheets with field codes (e.g., "SEE SHEET A-102") | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Callout blocks | Place detail or section callouts that automatically reference the correct sheet number | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Publish entire set | One-click batch plot all sheets in the set to PDF or plotter | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Sheet index table | Auto-generate sheet index on cover sheet listing all sheets in set | https://help.autodesk.com/view/ACD/2025/ENU/ |

## Drawing Checklist Before Plot
| Check | What to Verify | Source |
|-------|---------------|--------|
| All XREFs loaded | No missing reference notifications | https://help.autodesk.com/view/ACD/2025/ENU/ |
| Viewport scale correct | Verify with scale bar or dimension check | Best practice |
| Layers thawed/on | All required layers visible; no frozen layers needed for that sheet | Best practice |
| Plot style assigned | Correct CTB/STB file attached to layout | Firm standard |
| Line weights display | Preview plot to verify line weights read correctly | Best practice |
| Text readable | Minimum plotted text height 3/32" (2.5mm) for notes, 1/8" (3mm) for titles | https://www.nationalcadstandard.org/ |
| Dims associative | All dimensions update when geometry changes | https://help.autodesk.com/view/ACD/2025/ENU/ |
| No proxy objects | PURGE and AUDIT drawing before final plot | https://help.autodesk.com/view/ACD/2025/ENU/ |
