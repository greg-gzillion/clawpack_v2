import pathlib
VA = pathlib.Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\VA')

# These are the folders that are STILL MISSING law_resources.md
# Write to ALL of them with basic info
missing = [
    "Alexandria", "Alexandria_City",
    "Bristol", "Bristol_City",
    "Buena_Vista", "Buena_Vista_City",
    "Charlottesville", "Charlottesville_City",
    "Chesapeake", "Chesapeake_City",
    "Colonial_Heights", "Colonial_Heights_City",
    "Covington", "Covington_City",
    "Danville", "Danville_City",
    "Emporia", "Emporia_City",
    "Falls_Church", "Falls_Church_City",
    "Franklin_City",
    "Fredericksburg", "Fredericksburg_City",
    "Frederick_County",
    "Galax", "Galax_City",
    "Hampton", "Hampton_City",
    "Harrisonburg", "Harrisonburg_City",
    "Hopewell", "Hopewell_City",
    "Lexington", "Lexington_City",
    "Lynchburg", "Lynchburg_City",
    "Manassas", "Manassas_City", "Manassas_Park", "Manassas_Park_City",
    "Martinsville", "Martinsville_City",
    "Newport_News", "Newport_News_City",
    "Norfolk", "Norfolk_City",
    "Norton", "Norton_City",
    "Petersburg", "Petersburg_City",
    "Poquoson", "Poquoson_City",
    "Portsmouth", "Portsmouth_City",
    "Radford", "Radford_City",
    "Richmond", "Richmond_City",
    "Roanoke", "Roanoke_City",
    "Rockbridge",
    "Rockingham",
    "Russell",
    "Salem", "Salem_City",
    "Scott",
    "Shenandoah",
    "Smyth",
    "Southampton",
    "Spotsylvania",
    "Stafford",
    "Staunton", "Staunton_City",
    "Suffolk", "Suffolk_City",
    "Surry",
    "Sussex",
    "Tazewell",
    "Virginia_Beach", "Virginia_Beach_City",
    "Warren",
    "Washington",
    "Waynesboro", "Waynesboro_City",
    "Westmoreland",
    "Williamsburg", "Williamsburg_City",
    "Winchester", "Winchester_City",
    "Wise",
    "Wythe",
    "York",
]

content_template = """# {display} — Local Law Resources
## Law Enforcement
- Sheriff or Police Chief
- Virginia State Police — https://www.vsp.virginia.gov/
## Courts
- Circuit Court — https://www.vacourts.gov/
## County Attorney / Defender
- Commonwealth's Attorney
- Virginia Public Defender — https://www.vadefenders.org/
## Hunting Regulations
- VA Hunting Regulations — https://www.dwr.virginia.gov/hunting/
## Fishing Regulations
- VA Saltwater Fishing — https://www.mrc.virginia.gov/
- VA Freshwater Fishing — https://www.dwr.virginia.gov/fishing/
## Legal Aid
- Virginia Legal Aid — https://www.vlas.org/
## Corrections
- Local Jail
"""

for folder in missing:
    target
Get-ChildItem -Path "C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\VA" -Directory | Where-Object { .Name -ne "state" } | ForEach-Object {
    C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\KY\Woodford\law_resources.md = Join-Path .FullName "law_resources.md"
    if (-not (Test-Path C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\KY\Woodford\law_resources.md)) {
        Worcester = .Name -replace "_City", "" -replace "_County", ""
@"
# Worcester — Local Law Resources
## Law Enforcement
- Sheriff or Police Chief
- Virginia State Police — https://www.vsp.virginia.gov/
## Courts
- Circuit Court — https://www.vacourts.gov/
## County Attorney / Defender
- Commonwealth's Attorney
- Virginia Public Defender — https://www.vadefenders.org/
## Hunting Regulations
- VA Hunting Regulations — https://www.dwr.virginia.gov/hunting/
## Fishing Regulations
- VA Saltwater Fishing — https://www.mrc.virginia.gov/
- VA Freshwater Fishing — https://www.dwr.virginia.gov/fishing/
## Legal Aid
- Virginia Legal Aid — https://www.vlas.org/
## Corrections
- Local Jail
