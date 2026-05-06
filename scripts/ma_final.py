import pathlib
MA = pathlib.Path(r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\MA")

# ===== BERKSHIRE =====
(MA / "Berkshire" / "law_resources.md").write_text("""# Berkshire County — Local Law Resources
## Universities
- Williams College — https://www.williams.edu/
- Massachusetts College of Liberal Arts — https://www.mcla.edu/
## Law Enforcement
- Berkshire County Sheriff — https://www.berkshiresheriff.org/
- Pittsfield Police — https://www.cityofpittsfield.org/police/
- Massachusetts State Police — https://www.mass.gov/orgs/massachusetts-state-police
## Courts
- Berkshire County Superior Court — https://www.mass.gov/courts/court-info/superior-court/
## County Attorney / Defender
- Berkshire District Attorney — https://www.mass.gov/orgs/berkshire-district-attorneys-office
- Committee for Public Counsel Services — https://www.publiccounsel.net/
## Hunting Regulations
- MA Hunting Regulations — https://www.mass.gov/hunting-regulations
- October Mountain State Forest — https://www.mass.gov/locations/october-mountain-state-forest
## Fishing Regulations
- MA Freshwater Fishing — https://www.mass.gov/freshwater-fishing
- Housatonic River — trout — https://www.mass.gov/housatonic-river-fishing
- Onota Lake — bass, trout
- Pontoosuc Lake — bass
## Legal Aid
- Community Legal Aid — https://www.communitylegal.org/
## Corrections
- Berkshire County Jail — https://www.berkshiresheriff.org/
## Municipal Codes
- Pittsfield — https://www.cityofpittsfield.org/
""", encoding="utf-8")

# ===== FRANKLIN_MA =====
(MA / "Franklin" / "law_resources.md").write_text("""# Franklin County — Local Law Resources
## Universities
- University of Massachusetts Amherst (adjacent) — https://www.umass.edu/
## Law Enforcement
- Franklin County Sheriff — https://www.fcso-ma.us/
- Greenfield Police — https://www.greenfield-ma.gov/departments/police_department
- Massachusetts State Police — https://www.mass.gov/orgs/massachusetts-state-police
## Courts
- Franklin County Superior Court — https://www.mass.gov/courts/court-info/superior-court/
## County Attorney / Defender
- Northwestern District Attorney — https://www.mass.gov/orgs/northwestern-district-attorneys-office
- Committee for Public Counsel Services — https://www.publiccounsel.net/
## Hunting Regulations
- MA Hunting Regulations — https://www.mass.gov/hunting-regulations
## Fishing Regulations
- MA Freshwater Fishing — https://www.mass.gov/freshwater-fishing
- Connecticut River — bass, shad, striped bass
- Deerfield River — trout — https://www.mass.gov/deerfield-river-fishing
- Millers River — trout
## Legal Aid
- Community Legal Aid — https://www.communitylegal.org/
## Corrections
- Franklin County Jail — https://www.fcso-ma.us/
## Municipal Codes
- Greenfield — https://www.greenfield-ma.gov/
""", encoding="utf-8")

# ===== DUKES (MARTHA'S VINEYARD) =====
(MA / "Dukes" / "law_resources.md").write_text("""# Dukes County — Local Law Resources
## Law Enforcement
- Dukes County Sheriff — https://www.dukescountysheriff.org/
- Edgartown Police — https://www.edgartownpd.org/
- Massachusetts State Police — https://www.mass.gov/orgs/massachusetts-state-police
## Courts
- Dukes County Superior Court — https://www.mass.gov/courts/court-info/superior-court/
## County Attorney / Defender
- Cape & Islands District Attorney — https://www.mass.gov/orgs/cape-and-islands-district-attorneys-office
- Committee for Public Counsel Services — https://www.publiccounsel.net/
## Hunting Regulations
- MA Hunting Regulations — https://www.mass.gov/hunting-regulations
- Martha's Vineyard — limited deer hunting
## Fishing Regulations
- MA Saltwater Fishing — https://www.mass.gov/saltwater-fishing
- MA Freshwater Fishing — https://www.mass.gov/freshwater-fishing
- Atlantic Ocean — striped bass, bluefish, bonito, false albacore
- Martha's Vineyard Striped Bass & Bluefish Derby — https://www.mvderby.com/
- Vineyard Sound — striped bass, fluke
## Legal Aid
- South Coastal Counties Legal Services — https://www.sccls.org/
## Corrections
- Dukes County Jail — https://www.dukescountysheriff.org/
## Municipal Codes
- Edgartown — https://www.edgartown-ma.us/
""", encoding="utf-8")

# ===== NANTUCKET =====
(MA / "Nantucket" / "law_resources.md").write_text("""# Nantucket County — Local Law Resources
## Law Enforcement
- Nantucket Police — https://www.nantucketpolice.com/
- Massachusetts State Police — https://www.mass.gov/orgs/massachusetts-state-police
## Courts
- Nantucket County Superior Court — https://www.mass.gov/courts/court-info/superior-court/
## County Attorney / Defender
- Cape & Islands District Attorney — https://www.mass.gov/orgs/cape-and-islands-district-attorneys-office
- Committee for Public Counsel Services — https://www.publiccounsel.net/
## Hunting Regulations
- MA Hunting Regulations — https://www.mass.gov/hunting-regulations
- Nantucket — deer hunting program
## Fishing Regulations
- MA Saltwater Fishing — https://www.mass.gov/saltwater-fishing
- Atlantic Ocean — striped bass, bluefish, bonito, false albacore
- Nantucket Sound — striped bass, fluke
- Great Point — surf fishing
- Nantucket Bay scallops — https://www.mass.gov/nantucket-bay-scallops
## Military
- U.S. Coast Guard Station Brant Point — https://www.atlanticarea.uscg.mil/
## Legal Aid
- South Coastal Counties Legal Services — https://www.sccls.org/
## Corrections
- Nantucket County Jail
## Municipal Codes
- Nantucket — https://www.nantucket-ma.gov/
""", encoding="utf-8")

print("Massachusetts complete: 14/14 counties with law_resources.md")
