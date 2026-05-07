import pathlib
MI = pathlib.Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\MI')

cities = {
"Lenawee": {"Adrian": {"city": "https://www.adriancity.com/", "police": "Adrian PD — 155 E Maumee St — (517) 264-4808", "court": "2A District Court — 425 N Main St — (517) 264-4675", "court_url": "https://www.lenawee.org/2a-district-court"}},
"Allegan": {
"Allegan": {"city": "https://www.allegancounty.org/", "police": "Allegan County Sheriff — (269) 673-0500", "court": "57th District Court — 113 Chestnut St — (269) 673-0400", "court_url": "https://www.allegancounty.org/57th-district-court"},
"Holland": {"city": "https://www.hollandmi.gov/", "police": "Holland PD — 100 E Eighth St — (616) 355-1000", "court": "63rd District Court — 201 S River Ave — (616) 355-1550", "court_url": "https://www.oakgov.com/63rd-district-court"},
},
"Alpena": {"Alpena": {"city": "https://alpenacounty.org/", "police": "Alpena PD — 501 W Chisholm St — (989) 354-1800", "court": "88th District Court — 720 W Chisholm St — (989) 354-9573", "court_url": "https://alpenacounty.org/26/circuit-court"}},
"Mecosta": {"Big_Rapids": {"city": "https://cityofbr.org/", "police": "Big Rapids DPS — 435 N Michigan Ave — (231) 527-0005", "court": "77th District Court — 400 Elm St — (231) 592-0799", "court_url": "https://www.co.mecosta.mi.us/77th-district-court"}},
"Wexford": {"Cadillac": {"city": "https://www.cadillac-mi.net/", "police": "Cadillac PD — 200 N Lake St — (231) 775-3491", "court": "13A District Court — 200 N Mitchell St — (231) 775-5003", "court_url": "https://13adistrictcourt.org/"}},
"Branch": {"Coldwater": {"city": "https://www.cityofcoldwater.com/", "police": "Coldwater PD — 57 Division St — (517) 278-4525", "court": "3A District Court — 31 Division St — (517) 279-4308", "court_url": "https://www.branchcountymi.gov/3a-district-court"}},
"Otsego": {"Gaylord": {"city": "https://www.cityofgaylord.com/", "police": "Gaylord PD — 305 East Main St — (989) 732-1777", "court": "87A District Court — 800 Livingston Blvd — (989) 731-7500", "court_url": "https://www.otsegocountymi.gov/district_court"}},
"Montcalm": {"Greenville": {"city": "https://www.greenvillemi.org/", "police": "Greenville DPS — 411 S Lafayette St — (616) 754-5645", "court": "64B District Court — Stanton — (989) 831-7450", "court_url": "https://www.montcalm.us/64b-district-court"}},
"Houghton": {"Hancock": {"city": "https://www.cityofhancock.com/", "police": "Hancock PD — 125 Quincy St — (906) 482-2720", "court": "93rd District Court — 206 W Montezuma Ave — (906) 482-1414", "court_url": "https://www.houghtoncountymi.gov/courts"}},
"Barry": {"Hastings": {"city": "https://www.hastingsmi.org/", "police": "Hastings PD — 206 West State St — (269) 948-2111", "court": "56B District Court — 206 W Court St Ste 202 — (269) 945-1404", "court_url": "https://www.barrycounty.org/district_court"}},
"Hillsdale": {"Hillsdale": {"city": "https://www.hillsdalecity.com/", "police": "Hillsdale PD — 97 North Broad St — (517) 437-6460", "court": "14th District Court — 29 North Howell St — (517) 437-7758", "court_url": "https://www.hillsdalecountymi.gov/district_court"}},
"Dickinson": {"Iron_Mountain": {"city": "https://www.ironmountain.org/", "police": "Iron Mountain PD — 111 East Fleshiem St — (906) 774-6262", "court": "95A District Court — 705 S Stephenson St — (906) 774-2266", "court_url": "https://www.dickinsoncountymi.gov/courts"}},
"Gogebic": {"Ironwood": {"city": "https://www.ironwoodcity.com/", "police": "Ironwood DPS — 123 West McLeod Ave — (906) 932-0333", "court": "97th District Court — 213 South Marquette St — (906) 932-0333", "court_url": "https://www.co.gogebic.mi.us/97th-district-court"}},
"Mason": {"Ludington": {"city": "https://www.ludington.com/", "police": "Ludington PD — 304 E Ludington Ave — (231) 843-4130", "court": "79th District Court — 304 E Ludington Ave — (231) 843-4130", "court_url": "https://www.masoncounty.net/79th-district-court"}},
"Manistee": {"Manistee": {"city": "https://www.manisteemi.gov/", "police": "Manistee PD — 70 Maple St — (231) 723-5010", "court": "85th District Court — 415 Third St — (231) 723-5010", "court_url": "https://www.manisteecounty.org/district-court"}},
"Menominee": {"Menominee": {"city": "https://www.menominee.org/", "police": "Menominee PD — 2509 10th St — (906) 863-5568", "court": "95A District Court — 839 10th Ave — (906) 863-8981", "court_url": "https://www.menomineecounty.org/courts"}},
"Isabella": {"Mount_Pleasant": {"city": "https://www.mt-pleasant.org/", "police": "Mount Pleasant PD — 804 E High St — (989) 779-5100", "court": "76th District Court — 300 N Main St — (989) 772-0911", "court_url": "https://www.isabellacounty.org/courts"}},
"Shiawassee": {"Owosso": {"city": "https://www.cityofowosso.org/", "police": "Owosso PD — 202 S Water St — (989) 725-0580", "court": "66th District Court — Corunna — (989) 743-2395", "court_url": "https://www.shiawasseecounty.org/66th-district-court"}},
"Emmet": {"Petoskey": {"city": "https://www.petoskey.gov/", "police": "Petoskey PD — 101 E Lake St — (231) 347-2600", "court": "90th District Court — 200 Division St #G12 — (231) 348-1750", "court_url": "https://www.emmetcounty.org/90th-district-court"}},
"Van_Buren": {"South_Haven": {"city": "https://www.southhaven.org/", "police": "South Haven PD — 400 Phoenix St — (269) 637-5222", "court": "7th District Court — 1007 E Wells St — (269) 637-5258", "court_url": "https://www.vanburencounty.org/district-court"}},
"St._Joseph": {
"Sturgis": {"city": "https://www.sturgismi.gov/", "police": "Sturgis PD — 122 N Nottawa St — (269) 651-3231", "court": "3B District Court — Centreville — (269) 445-1930", "court_url": "https://www.stjosephcountymi.gov/3b-district-court"},
"Three_Rivers": {"city": "https://www.threeriversmi.org/", "police": "Three Rivers PD — 121 W Michigan Ave — (269) 273-1000", "court": "3B District Court — Centreville — (269) 445-1930", "court_url": "https://www.stjosephcountymi.gov/3b-district-court"},
},
}

count = 0
for county, city_dict in cities.items():
for city_name, data in city_dict.items():
city_dir = MI / county / city_name
if not city_dir.exists():
continue
court_url_line = f"- Court Website: {data['court_url']}" if data.get('court_url') else ""
(city_dir / 'law_resources.md').write_text(f"""# {city_name.replace('_', ' ')} — Local Law Resources

City Website
{data['city']}

Law Enforcement
{data['police']}

Michigan State Police — https://www.michigan.gov/msp

Courts
{data['court']}
{court_url_line}

Building Permits
{city_name.replace('_', ' ')} Building Department — {data['city']}

Hunting Regulations
MI Hunting Regulations — https://www.michigan.gov/dnr/hunting

Fishing Regulations
MI Fishing Regulations — https://www.michigan.gov/dnr/fishing

Legal Aid
Michigan Legal Aid — https://www.michiganlegalaid.org/

Corrections
{county.replace('', ' ')} County Jail
""", encoding='utf-8')
(city_dir / 'district_court.md').write_text(f"""# {city_name.replace('', ' ')} District Court

Court Information
{data['court']}
{court_url_line}

City Website
{data['city']}
""", encoding='utf-8')
count += 1

print(f"Michigan batch 3: {count}")
