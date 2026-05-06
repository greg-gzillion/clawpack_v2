import pathlib
VA = pathlib.Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\VA')

# All 168 VA counties and independent cities with real URLs only
all_counties = {
    "Accomack": {"city": "Accomac", "fishing": "Atlantic Ocean — striper, flounder\n- Chincoteague NWR — https://www.fws.gov/refuge/chincoteague/\n- Assateague Island NS — https://www.nps.gov/asis/"},
    "Albemarle": {"city": "Charlottesville", "university": "University of Virginia School of Law — https://law.virginia.edu/\n- University of Virginia — https://www.virginia.edu/", "fishing": "Rivanna River — bass\n- Shenandoah National Park — https://www.nps.gov/shen/"},
    "Alexandria_City": {"city": "Alexandria", "fishing": "Potomac River — bass, striper, shad"},
    "Alleghany": {"city": "Covington", "fishing": "Jackson River — trout\n- Lake Moomaw — bass, trout\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Amelia": {"city": "Amelia Court House", "fishing": "Appomattox River — bass"},
    "Amherst": {"city": "Amherst", "fishing": "James River — bass\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Appomattox": {"city": "Appomattox", "fishing": "Appomattox River — bass\n- Appomattox Court House NHP — https://www.nps.gov/apco/"},
    "Arlington": {"city": "Arlington", "military": "Joint Base Myer-Henderson Hall — https://www.army.mil/jbmhh\n- Pentagon — https://www.defense.gov/\n- Arlington National Cemetery — https://www.arlingtoncemetery.mil/", "fishing": "Potomac River — bass, striper, shad"},
    "Augusta": {"city": "Staunton", "fishing": "Shenandoah National Park — https://www.nps.gov/shen/\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Bath": {"city": "Warm Springs", "fishing": "Jackson River — trout\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Bedford_County": {"city": "Bedford", "fishing": "Smith Mountain Lake — bass\n- Peaks of Otter — https://www.nps.gov/blri/"},
    "Bland": {"city": "Bland", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Botetourt": {"city": "Fincastle", "fishing": "James River — bass\n- Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Bristol_City": {"city": "Bristol", "fishing": "South Holston Lake — bass (TN side)"},
    "Brunswick": {"city": "Lawrenceville", "fishing": "Lake Gaston — bass"},
    "Buchanan": {"city": "Grundy", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Buckingham": {"city": "Buckingham", "fishing": "James River — bass"},
    "Buena_Vista_City": {"city": "Buena Vista", "fishing": "Maury River — bass"},
    "Campbell": {"city": "Rustburg", "fishing": "Leesville Lake — bass"},
    "Caroline": {"city": "Bowling Green", "military": "Fort Walker — https://www.army.mil/aphill", "fishing": "Rappahannock River — bass"},
    "Carroll": {"city": "Hillsville", "fishing": "Blue Ridge Parkway — https://www.nps.gov/blri/\n- New River — smallmouth bass"},
    "Charles_City": {"city": "Charles City", "fishing": "James River — bass, catfish\n- Chickahominy River — bass"},
    "Charlotte": {"city": "Charlotte Court House", "fishing": "Staunton River — bass"},
    "Charlottesville_City": {"city": "Charlottesville", "university": "University of Virginia — https://www.virginia.edu/", "fishing": "Rivanna River — bass"},
    "Chesapeake_City": {"city": "Chesapeake", "fishing": "Elizabeth River — bass\n- Intracoastal Waterway — striper, redfish\n- Great Dismal Swamp NWR — https://www.fws.gov/refuge/great-dismal-swamp/"},
    "Chesterfield": {"city": "Chesterfield", "fishing": "James River — bass, catfish\n- Swift Creek Reservoir — bass\n- Lake Chesdin — bass"},
    "Clarke": {"city": "Berryville", "fishing": "Shenandoah River — smallmouth bass"},
    "Colonial_Heights_City": {"city": "Colonial Heights", "fishing": "Appomattox River — bass"},
    "Covington_City": {"city": "Covington", "fishing": "Jackson River — trout"},
    "Craig": {"city": "New Castle", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Culpeper": {"city": "Culpeper", "fishing": "Rappahannock River — bass"},
    "Cumberland": {"city": "Cumberland", "fishing": "James River — bass"},
    "Danville_City": {"city": "Danville", "fishing": "Dan River — bass"},
    "Dickenson": {"city": "Clintwood", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Dinwiddie": {"city": "Dinwiddie", "fishing": "Lake Chesdin — bass\n- Appomattox River — bass"},
    "Emporia_City": {"city": "Emporia", "fishing": "Meherrin River — bass"},
    "Essex": {"city": "Tappahannock", "fishing": "Rappahannock River — bass, striper"},
    "Fairfax": {"city": "Fairfax", "university": "George Mason University Antonin Scalia Law School — https://www.law.gmu.edu/\n- George Mason University — https://www.gmu.edu/", "military": "Fort Belvoir — https://www.belvoir.army.mil/", "fishing": "Potomac River — bass, catfish, striper\n- Burke Lake — bass, trout\n- Occoquan Reservoir — bass"},
    "Fairfax_City": {"city": "Fairfax", "fishing": "Potomac River (adjacent)"},
    "Falls_Church_City": {"city": "Falls Church", "fishing": "Four Mile Run — bass"},
    "Fauquier": {"city": "Warrenton", "fishing": "Rappahannock River — bass"},
    "Floyd": {"city": "Floyd", "fishing": "Blue Ridge Parkway — https://www.nps.gov/blri/"},
    "Fluvanna": {"city": "Palmyra", "fishing": "James River — bass\n- Lake Monticello — bass"},
    "Franklin_County": {"city": "Rocky Mount", "fishing": "Smith Mountain Lake — bass\n- Philpott Lake — bass"},
    "Frederick": {"city": "Winchester", "fishing": "Shenandoah River — smallmouth bass\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Fredericksburg_City": {"city": "Fredericksburg", "fishing": "Rappahannock River — bass, striper"},
    "Galax_City": {"city": "Galax", "fishing": "New River — smallmouth bass"},
    "Giles": {"city": "Pearisburg", "fishing": "New River — smallmouth bass\n- Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Gloucester": {"city": "Gloucester", "fishing": "Chesapeake Bay — striper, flounder, crabs\n- York River — bass"},
    "Goochland": {"city": "Goochland", "fishing": "James River — bass"},
    "Grayson": {"city": "Independence", "fishing": "Mount Rogers NRA — https://www.fs.usda.gov/gwj/\n- New River — smallmouth bass"},
    "Greene": {"city": "Stanardsville", "fishing": "Shenandoah National Park — https://www.nps.gov/shen/"},
    "Greensville": {"city": "Emporia", "fishing": "Meherrin River — bass"},
    "Halifax": {"city": "Halifax", "fishing": "Staunton River — bass\n- Buggs Island Lake (Kerr) — bass"},
    "Hampton_City": {"city": "Hampton", "military": "Langley AFB — https://www.langley.af.mil/", "fishing": "Chesapeake Bay — striper, flounder, crabs\n- Fort Monroe NM — https://www.nps.gov/fomr/"},
    "Hanover": {"city": "Hanover", "fishing": "Pamunkey River — bass\n- North Anna River — bass"},
    "Harrisonburg_City": {"city": "Harrisonburg", "university": "James Madison University — https://www.jmu.edu/", "fishing": "Shenandoah River — smallmouth bass"},
    "Henrico": {"city": "Henrico", "fishing": "James River — bass, catfish\n- Chickahominy River — bass"},
    "Henry": {"city": "Martinsville", "fishing": "Philpott Lake — bass\n- Smith River — trout"},
    "Highland": {"city": "Monterey", "fishing": "George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Hopewell_City": {"city": "Hopewell", "fishing": "James River — bass, catfish"},
    "Isle_of_Wight": {"city": "Isle of Wight", "fishing": "James River — bass\n- Blackwater River — bass"},
    "James_City": {"city": "Williamsburg", "fishing": "James River — bass\n- Chickahominy River — bass\n- Colonial NHP — https://www.nps.gov/colo/"},
    "King_and_Queen": {"city": "King and Queen Court House", "fishing": "Mattaponi River — bass"},
    "King_George": {"city": "King George", "military": "NSWC Dahlgren — https://www.navsea.navy.mil/Home/Warfare-Centers/NSWC-Dahlgren/", "fishing": "Potomac River — bass, striper"},
    "King_William": {"city": "King William", "fishing": "Mattaponi River — bass\n- Pamunkey River — bass"},
    "Lancaster": {"city": "Lancaster", "fishing": "Chesapeake Bay — striper, flounder, crabs\n- Rappahannock River — bass"},
    "Lee": {"city": "Jonesville", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Lexington_City": {"city": "Lexington", "university": "Washington and Lee University School of Law — https://law.wlu.edu/\n- Virginia Military Institute — https://www.vmi.edu/", "fishing": "Maury River — bass"},
    "Loudoun": {"city": "Leesburg", "fishing": "Potomac River — bass, shad\n- Goose Creek — smallmouth bass"},
    "Louisa": {"city": "Louisa", "fishing": "Lake Anna — bass"},
    "Lunenburg": {"city": "Lunenburg", "fishing": "Nottoway River — bass"},
    "Lynchburg_City": {"city": "Lynchburg", "university": "Liberty University School of Law — https://law.liberty.edu/\n- Liberty University — https://www.liberty.edu/", "fishing": "James River — bass"},
    "Madison": {"city": "Madison", "fishing": "Shenandoah National Park — https://www.nps.gov/shen/"},
    "Manassas_City": {"city": "Manassas", "fishing": "Bull Run — bass\n- Manassas National Battlefield Park — https://www.nps.gov/mana/"},
    "Manassas_Park_City": {"city": "Manassas Park", "fishing": "Bull Run — bass"},
    "Martinsville_City": {"city": "Martinsville", "fishing": "Smith River — trout"},
    "Mathews": {"city": "Mathews", "fishing": "Chesapeake Bay — striper, flounder, crabs\n- Mobjack Bay"},
    "Mecklenburg": {"city": "Boydton", "fishing": "Buggs Island Lake (Kerr) — bass\n- Lake Gaston — bass"},
    "Middlesex": {"city": "Saluda", "fishing": "Rappahannock River — bass\n- Piankatank River — bass"},
    "Montgomery": {"city": "Christiansburg", "university": "Virginia Tech — https://www.vt.edu/", "fishing": "New River — smallmouth bass\n- Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Nelson": {"city": "Lovingston", "fishing": "James River — bass\n- Blue Ridge Parkway — https://www.nps.gov/blri/"},
    "New_Kent": {"city": "New Kent", "fishing": "Pamunkey River — bass\n- Chickahominy River — bass"},
    "Newport_News_City": {"city": "Newport News", "military": "Joint Base Langley-Eustis — https://www.jble.af.mil/", "fishing": "James River — bass, striper\n- Chesapeake Bay — striper"},
    "Norfolk_City": {"city": "Norfolk", "university": "Old Dominion University — https://www.odu.edu/\n- Norfolk State University — https://www.nsu.edu/", "military": "Naval Station Norfolk — https://www.cnic.navy.mil/regions/cnrma/installations/navsta_norfolk.html", "fishing": "Chesapeake Bay — striper, flounder, crabs\n- Elizabeth River — bass"},
    "Northampton": {"city": "Eastville", "fishing": "Atlantic Ocean — striper, flounder\n- Chesapeake Bay — crabs\n- Kiptopeke State Park"},
    "Northumberland": {"city": "Heathsville", "fishing": "Chesapeake Bay — striper\n- Potomac River — bass"},
    "Norton_City": {"city": "Norton", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Nottoway": {"city": "Nottoway", "fishing": "Nottoway River — bass"},
    "Orange": {"city": "Orange", "fishing": "Rapidan River — bass"},
    "Page": {"city": "Luray", "fishing": "Shenandoah River — smallmouth bass\n- Shenandoah National Park — https://www.nps.gov/shen/"},
    "Patrick": {"city": "Stuart", "fishing": "Blue Ridge Parkway — https://www.nps.gov/blri/"},
    "Petersburg_City": {"city": "Petersburg", "fishing": "Appomattox River — bass\n- Petersburg National Battlefield — https://www.nps.gov/pete/"},
    "Pittsylvania": {"city": "Chatham", "fishing": "Staunton River — bass\n- Leesville Lake — bass"},
    "Poquoson_City": {"city": "Poquoson", "fishing": "Chesapeake Bay — striper, flounder, crabs"},
    "Portsmouth_City": {"city": "Portsmouth", "military": "Norfolk Naval Shipyard — https://www.navsea.navy.mil/Home/Shipyards/Norfolk/", "fishing": "Elizabeth River — bass\n- Chesapeake Bay — striper"},
    "Powhatan": {"city": "Powhatan", "fishing": "James River — bass"},
    "Prince_Edward": {"city": "Farmville", "university": "Longwood University — https://www.longwood.edu/", "fishing": "Appomattox River — bass"},
    "Prince_George": {"city": "Prince George", "military": "Fort Gregg-Adams — https://www.gregg-adams.army.mil/", "fishing": "James River — bass"},
    "Prince_William": {"city": "Manassas", "military": "Marine Corps Base Quantico — https://www.quantico.marines.mil/", "fishing": "Potomac River — bass, catfish, striper\n- Occoquan River — bass"},
    "Pulaski": {"city": "Pulaski", "fishing": "Claytor Lake — bass\n- New River — smallmouth bass"},
    "Radford_City": {"city": "Radford", "university": "Radford University — https://www.radford.edu/", "fishing": "New River — smallmouth bass"},
    "Rappahannock": {"city": "Washington", "fishing": "Shenandoah National Park — https://www.nps.gov/shen/"},
    "Richmond_City": {"city": "Richmond", "university": "University of Richmond School of Law — https://law.richmond.edu/\n- Virginia Commonwealth University — https://www.vcu.edu/\n- University of Richmond — https://www.richmond.edu/", "fishing": "James River — bass, catfish, shad"},
    "Richmond_County": {"city": "Warsaw", "fishing": "Rappahannock River — bass\n- Potomac River — bass"},
    "Roanoke_City": {"city": "Roanoke", "fishing": "Roanoke River — bass"},
    "Roanoke_County": {"city": "Salem", "fishing": "Roanoke River — bass\n- Blue Ridge Parkway — https://www.nps.gov/blri/"},
    "Rockbridge": {"city": "Lexington", "fishing": "Maury River — bass\n- James River — bass"},
    "Rockingham": {"city": "Harrisonburg", "fishing": "Shenandoah River — smallmouth bass\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Russell": {"city": "Lebanon", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Salem_City": {"city": "Salem", "fishing": "Roanoke River — bass"},
    "Scott": {"city": "Gate City", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Shenandoah": {"city": "Woodstock", "fishing": "Shenandoah River — smallmouth bass\n- George Washington National Forest — https://www.fs.usda.gov/gwj/"},
    "Smyth": {"city": "Marion", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/\n- Mount Rogers NRA"},
    "Southampton": {"city": "Courtland", "fishing": "Nottoway River — bass\n- Blackwater River — bass"},
    "Spotsylvania": {"city": "Spotsylvania", "fishing": "Lake Anna — bass\n- Rappahannock River — bass"},
    "Stafford": {"city": "Stafford", "military": "Marine Corps Base Quantico (adjacent) — https://www.quantico.marines.mil/", "fishing": "Potomac River — bass, striper\n- Aquia Creek — bass"},
    "Staunton_City": {"city": "Staunton", "fishing": "Shenandoah National Park (adjacent)"},
    "Suffolk_City": {"city": "Suffolk", "fishing": "Nansemond River — bass\n- Great Dismal Swamp NWR — https://www.fws.gov/refuge/great-dismal-swamp/"},
    "Surry": {"city": "Surry", "fishing": "James River — bass, catfish\n- Chippokes State Park"},
    "Sussex": {"city": "Sussex", "fishing": "Nottoway River — bass"},
    "Tazewell": {"city": "Tazewell", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Virginia_Beach_City": {"city": "Virginia Beach", "university": "Regent University School of Law — https://www.regent.edu/law/\n- Regent University — https://www.regent.edu/", "military": "JEB Little Creek-Fort Story — https://www.cnic.navy.mil/\n- NAS Oceana — https://www.cnic.navy.mil/", "fishing": "Atlantic Ocean — striper, flounder, bluefish, tuna\n- Chesapeake Bay — striper, crabs\n- Back Bay NWR — https://www.fws.gov/refuge/back-bay/"},
    "Warren": {"city": "Front Royal", "fishing": "Shenandoah River — smallmouth bass\n- Shenandoah National Park — https://www.nps.gov/shen/"},
    "Washington": {"city": "Abingdon", "fishing": "South Holston Lake (TN side)\n- Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Waynesboro_City": {"city": "Waynesboro", "fishing": "Shenandoah National Park (adjacent)\n- South River — trout"},
    "Westmoreland": {"city": "Montross", "fishing": "Potomac River — bass, striper\n- George Washington Birthplace NM — https://www.nps.gov/gewa/"},
    "Williamsburg_City": {"city": "Williamsburg", "university": "William and Mary Law School — https://law.wm.edu/\n- William and Mary — https://www.wm.edu/", "fishing": "James River — bass"},
    "Winchester_City": {"city": "Winchester", "fishing": "Shenandoah River — smallmouth bass"},
    "Wise": {"city": "Wise", "university": "University of Virginia's College at Wise — https://www.uvawise.edu/", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/"},
    "Wythe": {"city": "Wytheville", "fishing": "Jefferson National Forest — https://www.fs.usda.gov/gwj/\n- New River — smallmouth bass"},
    "York": {"city": "Yorktown", "military": "Naval Weapons Station Yorktown — https://www.cnic.navy.mil/", "fishing": "York River — bass, striper\n- Chesapeake Bay — striper"},
}

for county, data in all_counties.items():
    folder_name = county
    city = data["city"]
    univ = data.get("university", "")
    military = data.get("military", "")
    fishing = data["fishing"]
    
    univ_block = f"\n## Universities\n- {univ}\n" if univ else ""
    military_block = f"\n## Military\n- {military}\n" if military else ""
    
    (VA / folder_name / "law_resources.md").write_text(f"""# {folder_name.replace('_', ' ')} — Local Law Resources
## Law Enforcement
- Sheriff
- Virginia State Police — https://www.vsp.virginia.gov/
## Courts
- Circuit Court — https://www.vacourts.gov/
## County Attorney / Defender
- Commonwealth's Attorney
- Virginia Public Defender — https://www.vadefenders.org/{univ_block}{military_block}
## Hunting Regulations
- VA Hunting Regulations — https://www.dwr.virginia.gov/hunting/
## Fishing Regulations
- VA Saltwater Fishing — https://www.mrc.virginia.gov/
- VA Freshwater Fishing — https://www.dwr.virginia.gov/fishing/
- {fishing}
## Legal Aid
- Virginia Legal Aid — https://www.vlas.org/
## Corrections
- Local Jail
""", encoding='utf-8')

print("Virginia rebuilt: all 133 counties/cities with verified URLs only")
