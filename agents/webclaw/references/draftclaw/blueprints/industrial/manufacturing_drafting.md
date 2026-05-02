# Industrial Blueprint Standards - Manufacturing & Warehouse
## How to draw industrial facility plans, sections, and details

## Industrial Plan Symbols (per NCS / ANSI)
| Symbol | Represents | Drawing Convention | Source |
|--------|-----------|-------------------|--------|
| Heavy solid line with dimension | Exterior wall (8"-12" CMU or insulated metal panel) | Label wall type and fire rating | https://www.nationalcadstandard.org/ |
| Light solid line with note | Interior partition (chain-link, weld screen, or CMU) | Note height and material | https://www.nationalcadstandard.org/ |
| Dashed rectangle with label | Overhead door (coiling, sectional, or high-speed) | Dimension width x height, label type | https://www.nationalcadstandard.org/ |
| Circle with cross through it | Column (steel HSS or wide flange) | Call out size (W12x40, HSS8x8x1/2) in schedule | https://www.nationalcadstandard.org/ |
| Heavy line with tick marks | Crane runway beam | Show rail centerline, support spacing, and capacity | https://www.aisc.org/ |
| Rectangle with label | Forklift / industrial vehicle path | Show aisle width (12'-15' minimum) and turning radius | https://www.osha.gov/warehousing |
| Stippled area with note | Concrete slab depression or pit | Note depth and reinforcing | https://www.concrete.org/ |

## Manufacturing Floor Plan Layout
| Zone | Area Allocation | Drawing Detail Required | Source |
|------|---------------|------------------------|--------|
| Receiving / Raw materials | 5-10% total | Show dock positions, staging area, receiving office, quality inspection station | https://www.osha.gov/warehousing |
| Production / Assembly | 40-60% total | Show machine locations, operator workstations, conveyor/AGV paths, tool storage | https://www.osha.gov/warehousing |
| Work-in-process (WIP) storage | 5-10% total | Show racking type (selective, drive-in, push-back), aisle widths, load capacities | https://www.osha.gov/warehousing |
| Finished goods warehouse | 10-20% total | Show rack layout (single or double deep), aisle widths per forklift type | https://www.osha.gov/warehousing |
| Shipping / Outbound | 5-10% total | Show dock positions, manifest station, trailer parking, truck courts (70'-130' apron) | https://www.osha.gov/warehousing |
| Maintenance / Tool room | 2-4% total | Show workbench layout, parts storage, equipment access clearance | https://www.osha.gov/warehousing |
| Quality control / Lab | 2-4% total | Show equipment layout, environmental controls, clean room if applicable | https://www.osha.gov/warehousing |
| Offices / Admin | 5-8% total | Draw per commercial office standards; show fire separation from production | https://codes.iccsafe.org/content/IBC2021P1 |
| Break room / Locker rooms | 2-3% total | Show plumbing fixture layout, locker banks, vending area | https://www.osha.gov/warehousing |

## Warehouse Rack Layout Standards
| Rack Type | Aisle Width | Height | Load Capacity | Source |
|-----------|------------|--------|--------------|--------|
| Selective (single deep) | 12'-13' for counterbalance forklift | Up to 40' (per rack design) | 2,000-4,000 lbs per pallet position typical | https://www.rmiracksafety.org/ |
| Double deep | 12'-13' | Up to 35' | 2,000-3,000 lbs per position | https://www.rmiracksafety.org/ |
| Push-back | 10'-12' | Up to 30' | 1,500-3,000 lbs per position (2-6 deep) | https://www.rmiracksafety.org/ |
| Drive-in / Drive-through | 10'-11' | Up to 24' | 1,500-2,500 lbs per position | https://www.rmiracksafety.org/ |
| Pallet flow | 10'-12' | Up to 30' | 2,000-4,000 lbs per lane per level | https://www.rmiracksafety.org/ |
| Very Narrow Aisle (VNA) | 5.5'-6.5' (guided turret truck) | Up to 60' | 2,000-3,500 lbs per position | https://www.rmiracksafety.org/ |
| Cantilever (long loads) | 10'-12' | Up to 24' | Per arm capacity (1,000-5,000 lbs per arm) | https://www.rmiracksafety.org/ |

## Section Drawing Requirements for Industrial
| Section Cut | What to Show | Source |
|-------------|-------------|--------|
| Building cross-section | Column grid, roof structure (joist/joist girder or truss), wall bracing, crane runway if present, clear heights at each bay | https://www.aisc.org/ |
| Wall section | Exterior wall construction: metal panel/CMU, insulation R-value, air/vapor barrier, girt spacing, foundation connection | https://www.mbma.com/ (Metal Building Manufacturers Association) |
| Dock section | Dock leveler pit dimensions, dock seal/shelter projection, grade slope (1% max away), trench drain location, truck restraint detail | https://www.osha.gov/warehousing |
| Mezzanine section | Beam sizes (W-shape), column spacing, deck type (composite or non-composite), stair location, guardrail at 42" | https://www.aisc.org/ |
| Pit/trench section | Depth, width, reinforcing (per ACI 318), grating or cover plate spec, drainage slope | https://www.concrete.org/ |

## Mezzanine Design Standards (per AISC Design Guide 7)
| Element | Standard | Source |
|---------|----------|--------|
| Column spacing | 20' x 20' to 30' x 30' typical, per beam capacity and deck span | https://www.aisc.org/ |
| Deck type | 1-1/2" Type B roof deck (22 or 20 gauge) for non-composite; 2"-3" composite deck with shear studs for composite | https://www.aisc.org/ |
| Live load | 125 psf minimum for storage mezzanine; 100 psf for office/light use; 250 psf for heavy storage | https://codes.iccsafe.org/content/IBC2021P1 |
| Guardrail | 42" minimum height, 4" maximum sphere passage for guardrail openings (industrial exception: 21" for industrial platforms not open to public) | https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.29 |
| Stair width | 36" minimum (industrial), 44" minimum if serving >50 occupants | https://codes.iccsafe.org/content/IBC2021P1 |
| Egress from mezzanine | Maximum travel distance 250' (sprinklered), 200' (unsprinklered); open stairs count as 1 exit, enclosed stairs count as 2 | https://codes.iccsafe.org/content/IBC2021P1 |

## Concrete Slab Design for Industrial
| Element | Specification | Source |
|---------|--------------|--------|
| Slab thickness (light industrial) | 5" minimum, 4,000 psi, #4 bars at 18" o.c. each way | https://www.concrete.org/ |
| Slab thickness (heavy industrial/forklift) | 6"-8", 4,000-5,000 psi, #4 or #5 bars at 12" o.c. each way | https://www.concrete.org/ |
| Joint spacing | 12'-15' maximum in each direction (25 to 36 times slab thickness) | https://www.concrete.org/ |
| Floor flatness (standard warehouse) | FF 25 / FL 20 | https://www.concrete.org/ |
| Floor flatness (VNA/guided vehicles) | FF 50 / FL 35 minimum | https://www.concrete.org/ |
| Floor flatness (high-precision manufacturing) | FF 75 / FL 50 minimum | https://www.concrete.org/ |
| Vapor barrier | 10-15 mil polyethylene under slab, taped at all seams and penetrations | https://www.concrete.org/ |
| Control joints (saw-cut) | 1/4 slab depth, 1/8" width, sealed with semi-rigid epoxy joint filler | https://www.concrete.org/ |
