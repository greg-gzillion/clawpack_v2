# Panelboards and Circuit Protection - NEC Reference
## All URLs verified May 2026

## Panelboard Standards (NEC Article 408)
| Requirement | NEC Section | Standard | Source |
|-------------|------------|----------|--------|
| Panelboard definition | NEC 408.2 | "A single panel or group of panel units designed for assembly in the form of a single panel...including buses and automatic overcurrent devices." | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| Working clearance (depth) | NEC 110.26(A)(1) | 3 feet minimum for 0-150V to ground; 3.5 feet for 151-600V | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| Working clearance (width) | NEC 110.26(A)(2) | 30 inches or width of equipment, whichever is greater | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| Working clearance (height) | NEC 110.26(A)(3) | 6.5 feet or height of equipment; clear from floor to structural ceiling | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| Panelboard in bathroom prohibited | NEC 240.24(E) | Overcurrent devices shall not be located in bathrooms of dwelling units | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| Panelboard in clothes closet prohibited | NEC 240.24(D) | Overcurrent devices shall not be located in clothes closets | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |

## Circuit Breakers (NEC Article 240)
| Type | Application | Source |
|------|------------|--------|
| Standard thermal-magnetic | General branch circuit protection; inverse time trip curve | https://en.wikipedia.org/wiki/Circuit_breaker |
| GFCI (Class A) | Trips at 5mA leakage; required for bathroom, kitchen counter, garage, outdoor, crawl space, unfinished basement receptacles per NEC 210.8 | https://en.wikipedia.org/wiki/Residual-current_device |
| AFCI (combination type) | Detects series and parallel arc faults; required for dwelling unit circuits per NEC 210.12: kitchens, family rooms, dining rooms, living rooms, parlors, libraries, dens, bedrooms, sunrooms, recreation rooms, closets, hallways, laundry areas | https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70 |
| GFPE (30mA) | Equipment protection, not personnel; for heating cables, commercial kitchen equipment per NEC 210.8(B) | https://en.wikipedia.org/wiki/Residual-current_device |

## Panel Schedule (Drawing Convention)
| Field | What to Show | Source |
|-------|-------------|--------|
| Circuit number | Sequential: 1,2 (Phase A), 3,4 (Phase B), 5,6 (Phase C) for three-phase; 1,2 (L1), 3,4 (L2) for split-phase | Standard electrical drafting practice |
| Load description | Room or equipment served: "Kitchen GFCI", "Master Bedroom Lights", "A/C Condenser" | Standard electrical drafting practice |
| Wire size | AWG per NEC ampacity: #14 Cu for 15A, #12 Cu for 20A, #10 Cu for 30A | Standard electrical drafting practice |
| Breaker size | 15A, 20A (general), 30A (dryer/water heater), 40A-50A (range), 60A+ (subpanel/EV charger) | Standard electrical drafting practice |
| Connected load (VA) | Sum of all loads on circuit for load calculation | Standard electrical drafting practice |
