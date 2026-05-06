import pathlib
IA = pathlib.Path(r'C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\lawclaw\jurisdictions\us\IA')

cities = {
    "Story": {"Ames": {"city": "https://www.cityofames.org/", "police": "Ames PD — 515 Clark Ave — (515) 239-5133", "court": "Iowa Second Judicial District — 515 Clark Ave — (515) 239-5140", "court_url": "https://www.iowacourts.gov/"}},
    "Polk": {
        "Ankeny": {"city": "https://www.ankenyiowa.gov/", "police": "Ankeny PD — 211 SW Walnut St — (515) 965-6440", "court": "Polk County Courthouse — 400 E 2nd St, Des Moines — (515) 286-3550", "court_url": "https://www.iowacourts.gov/"},
        "Des_Moines_City": {"city": "https://www.dsm.city/", "police": "Des Moines PD — 25 E 1st St — (515) 283-4824", "court": "Des Moines Municipal Court — 24 E 1st St — (515) 283-4899", "court_url": "https://www.dsm.city/courts"},
        "Urbandale": {"city": "https://www.urbandale.org/", "police": "Urbandale PD — 3740 86th St — (515) 278-3911", "court": "Polk County Courthouse — 400 E 2nd St, Des Moines — (515) 286-3550", "court_url": "https://www.iowacourts.gov/"},
        "West_Des_Moines": {"city": "https://www.westdesmoines.org/", "police": "West Des Moines PD — 700 3rd St — (515) 222-3600", "court": "Polk County Courthouse — 110 6th Ave, Des Moines — (515) 286-3765", "court_url": "https://www.iowacourts.gov/"},
    },
    "Scott": {
        "Bettendorf": {"city": "https://www.bettendorf.org/", "police": "Bettendorf PD — 1609 State St — (563) 344-4015", "court": "Scott County Courthouse — 400 W 4th St, Davenport — (563) 326-8625", "court_url": "https://www.iowacourts.gov/"},
        "Davenport": {"city": "https://www.davenportiowa.com/", "police": "Davenport PD — (563) 326-7979", "court": "Scott County Courthouse — 400 W 4th St — (563) 326-8611", "court_url": "https://www.iowacourts.gov/"},
    },
    "Black_Hawk": {
        "Cedar_Falls": {"city": "https://www.cedarfalls.com/", "police": "Cedar Falls PD — 220 Clay St — (319) 268-5148 — M-F 8-5", "court": "Black Hawk County Courthouse — 316 E 5th St, Waterloo — (319) 833-6200", "court_url": "https://www.iowacourts.gov/"},
        "Waterloo": {"city": "https://www.waterloo-ia.org/", "police": "Waterloo PD — (319) 291-4340", "court": "Black Hawk County Clerk — 316 E 5th St — (319) 833-6200", "court_url": "https://www.iowacourts.gov/"},
    },
    "Linn": {
        "Cedar_Rapids": {"city": "https://www.cedar-rapids.org/", "police": "Cedar Rapids PD — (319) 286-5491", "court": "Linn County Courthouse — 931 2nd St SE — (319) 398-3545", "court_url": "https://www.iowacourts.gov/"},
        "Marion": {"city": "https://www.cityofmarion.org/", "police": "Marion PD — (319) 377-1511", "court": "Linn County Clerk — 319 1st Ave SE, Cedar Rapids — (319) 892-5100", "court_url": "https://www.iowacourts.gov/"},
    },
    "Clinton": {"Clinton_City": {"city": "https://www.clintoncounty-ia.gov/", "police": "Clinton PD — 241 7th Ave N — (563) 242-9211", "court": "Clinton Municipal Court — 612 N 2nd St — (563) 242-9211", "court_url": "https://www.clintonmunicourt.org/"}},
    "Pottawattamie": {"Council_Bluffs": {"city": "https://www.councilbluffs-ia.gov/", "police": "Council Bluffs PD — 227 S 6th St — (712) 328-5737", "court": "Pottawattamie County Court — 227 S 6th St — (712) 328-5617", "court_url": "https://www.iowacourts.gov/"}},
    "Dubuque": {"Dubuque_City": {"city": "https://www.cityofdubuque.org/", "police": "Dubuque PD — 770 Iowa St — (563) 589-4410", "court": "Dubuque County Clerk — 720 Central Ave — (563) 589-4418", "court_url": "https://www.iowacourts.gov/"}},
    "Warren": {"Indianola": {"city": "https://www.cityofindianola.com/", "police": "Indianola PD — 110 N 1st St — (515) 961-9400 — M-F 8-5", "court": "Warren County Courthouse — (515) 961-9410", "court_url": "https://www.iowacourts.gov/"}},
    "Johnson": {"Iowa_City": {"city": "https://www.icgov.org/", "police": "Iowa City PD — (319) 356-2621", "court": "Johnson County District Court — 417 S Clinton St — (319) 356-4931", "court_url": "https://www.iowacourts.gov/"}},
    "Marshall": {"Marshalltown": {"city": "https://www.marshalltown-ia.gov/", "police": "Marshalltown PD — 909 S 2nd St — (641) 754-5725", "court": "Marshall County Clerk — 1 E Main St — (641) 754-6380", "court_url": "https://www.iowacourts.gov/"}},
    "Cerro_Gordo": {"Mason_City": {"city": "https://www.masoncity.net/", "police": "Mason City PD — 78 S Georgia Ave — (641) 421-3636", "court": "Cerro Gordo County Clerk — 220 N Washington Ave — (641) 421-3056", "court_url": "https://www.iowacourts.gov/"}},
    "Woodbury": {"Sioux_City": {"city": "https://www.siouxcity.org/", "police": "Sioux City PD — 405 6th St — (712) 279-6300 — M-F 7:45-4:30", "court": "Woodbury County Clerk — 700 7th St — (712) 279-6623", "court_url": "https://www.iowacourts.gov/"}},
    "Dallas": {"Waukee": {"city": "https://www.waukee.org/", "police": "Waukee PD — 1300 SE LA Grant Pkwy — (515) 987-1073", "court": "Dallas County Clerk — 801 Court St, Adel — (515) 993-5805", "court_url": "https://www.iowacourts.gov/"}},
}

count = 0
for county, city_dict in cities.items():
    for city_name, data in city_dict.items():
        city_dir = IA / county / city_name
        if not city_dir.exists():
            continue
        court_url_line = f"- **Court Website**: {data['court_url']}" if data.get('court_url') else ""
        (city_dir / 'law_resources.md').write_text(f"""# {city_name.replace('_', ' ')} — Local Law Resources
## City Website
- {data['city']}
## Law Enforcement
- {data['police']}
- Iowa State Patrol — https://www.dps.iowa.gov/
## Courts
- {data['court']}
{court_url_line}
## Building Permits
- {city_name.replace('_', ' ')} Building Department — {data['city']}
## Hunting Regulations
- IA Hunting Regulations — https://www.iowadnr.gov/Hunting/Hunting-Regulations
## Fishing Regulations
- IA Fishing Regulations — https://www.iowadnr.gov/Fishing/Fishing-Regulations
## Legal Aid
- Iowa Legal Aid — https://www.iowalegalaid.org/
## Corrections
- {county.replace('_', ' ')} County Jail
""", encoding='utf-8')
        (city_dir / 'municipal_court.md').write_text(f"""# {city_name.replace('_', ' ')} Municipal Court
## Court Information
- {data['court']}
{court_url_line}
## City Website
- {data['city']}
""", encoding='utf-8')
        count += 1

print(f"Iowa cities updated: {count}")
