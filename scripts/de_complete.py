import pathlib
DE = pathlib.Path(r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\DE")

# ===== NEW CASTLE =====
(DE / "New_Castle" / "law_resources.md").write_text("""# New Castle County — Local Law Resources
## Law Schools & Universities
- Widener University Delaware Law School — Wilmington — https://delawarelaw.widener.edu/
  - Delaware Law Clinics — https://delawarelaw.widener.edu/academics/clinics/
  - Delaware Law Library — https://delawarelaw.widener.edu/library/
- University of Delaware — Pre-Law — https://www.udel.edu/academics/colleges/cas/undergraduate-programs/pre-law/
## Law Enforcement
- New Castle County Police — https://www.nccpdnews.com/
- Wilmington Police — https://www.wilmingtonde.gov/government/public-safety/police-department
- Delaware State Police — https://dsp.delaware.gov/
## Courts
- New Castle County Superior Court — Wilmington — https://courts.delaware.gov/superior/
- Delaware Supreme Court — Wilmington — https://courts.delaware.gov/supreme/
- U.S. District Court District of Delaware — https://www.ded.uscourts.gov/
## County Attorney / Defender
- Delaware Attorney General — https://attorneygeneral.delaware.gov/
- Delaware Public Defender — https://publicdefender.delaware.gov/
## Hunting Regulations
- DE Hunting & Trapping Guide — https://dnrec.delaware.gov/fish-wildlife/hunting/
- Deer seasons, zones — https://dnrec.delaware.gov/fish-wildlife/hunting/deer/
- Waterfowl — Bombay Hook NWR — https://www.fws.gov/refuge/bombay-hook/
## Fishing Regulations
- DE Fishing Guide — https://dnrec.delaware.gov/fish-wildlife/fishing/
- Delaware River — striper, shad, catfish — https://dnrec.delaware.gov/fish-wildlife/fishing/where-to-fish/
- Delaware Bay — striper, weakfish, bluefish
- Brandywine Creek — trout
- White Clay Creek — trout
- Lums Pond — bass, trout
## Legal Aid
- Delaware Legal Help Link — https://www.delegalhelplink.org/
- Community Legal Aid Society — https://www.declasi.org/
## Corrections
- Howard R. Young Correctional Institution — https://doc.delaware.gov/facilities/hryci/
- Baylor Women's Correctional Institution — https://doc.delaware.gov/facilities/bwci/
## Municipal Codes
- Wilmington — https://www.wilmingtonde.gov/
- Newark — https://www.newarkde.gov/
""", encoding="utf-8")

# ===== KENT (DOVER) =====
(DE / "Kent" / "law_resources.md").write_text("""# Kent County — Local Law Resources
## Universities
- Delaware State University — Pre-Law — https://www.desu.edu/
## Law Enforcement
- Dover Police — https://www.cityofdoverpolice.org/
- Delaware State Police HQ — Dover — https://dsp.delaware.gov/
## Courts
- Kent County Superior Court — Dover — https://courts.delaware.gov/superior/
- Delaware Court of Chancery — https://courts.delaware.gov/chancery/
## County Attorney / Defender
- Delaware Attorney General — https://attorneygeneral.delaware.gov/
- Delaware Public Defender — https://publicdefender.delaware.gov/
## Military
- Dover AFB Legal — https://www.dover.af.mil/About-Us/Legal-Office/
## Hunting Regulations
- DE Hunting & Trapping Guide — https://dnrec.delaware.gov/fish-wildlife/hunting/
- Deer seasons — https://dnrec.delaware.gov/fish-wildlife/hunting/deer/
- Waterfowl — Bombay Hook NWR — https://www.fws.gov/refuge/bombay-hook/
- Little Creek WMA — https://dnrec.delaware.gov/fish-wildlife/wildlife-areas/little-creek/
## Fishing Regulations
- DE Fishing Guide — https://dnrec.delaware.gov/fish-wildlife/fishing/
- Delaware Bay — striper, weakfish, bluefish, croaker
- Killens Pond — bass, trout — https://destateparks.com/pondsrivers/killenspond
- Moores Lake — bass
- St. Jones River — fishing
## Legal Aid
- Delaware Legal Help Link — https://www.delegalhelplink.org/
## Corrections
- James T. Vaughn Correctional Center — Smyrna — https://doc.delaware.gov/facilities/jtvcc/
- Sussex Correctional Institution (nearby) — https://doc.delaware.gov/facilities/sci/
## Municipal Codes
- Dover — https://www.cityofdover.com/
""", encoding="utf-8")

# ===== SUSSEX =====
(DE / "Sussex" / "law_resources.md").write_text("""# Sussex County — Local Law Resources
## Universities
- none in county (nearest: Delaware State, UD, Widener Law)
## Law Enforcement
- Delaware State Police — https://dsp.delaware.gov/
- Rehoboth Beach Police — https://www.rehobothpolice.org/
## Courts
- Sussex County Superior Court — Georgetown — https://courts.delaware.gov/superior/
## County Attorney / Defender
- Delaware Attorney General — https://attorneygeneral.delaware.gov/
- Delaware Public Defender — https://publicdefender.delaware.gov/
## Hunting Regulations
- DE Hunting & Trapping Guide — https://dnrec.delaware.gov/fish-wildlife/hunting/
- Deer seasons — https://dnrec.delaware.gov/fish-wildlife/hunting/deer/
- Waterfowl — Prime Hook NWR — https://www.fws.gov/refuge/prime-hook/
- Assawoman WMA — https://dnrec.delaware.gov/fish-wildlife/wildlife-areas/assawoman/
## Fishing Regulations
- DE Fishing Guide — https://dnrec.delaware.gov/fish-wildlife/fishing/
- Atlantic Ocean — striper, flounder, bluefish, tautog — surf/pier fishing
- Delaware Bay — striper, weakfish, croaker
- Indian River Inlet — striper, flounder — https://destateparks.com/beaches/indianriver
- Rehoboth Bay — flounder, striper
- Trap Pond — bass — https://destateparks.com/pondsrivers/trappond
## Legal Aid
- Delaware Legal Help Link — https://www.delegalhelplink.org/
## Corrections
- Sussex Correctional Institution — Georgetown — https://doc.delaware.gov/facilities/sci/
## Municipal Codes
- Georgetown — https://www.georgetowndel.com/
- Rehoboth Beach — https://www.cityofrehoboth.com/
""", encoding="utf-8")

print("Delaware complete: 3/3 counties with law_resources.md")
