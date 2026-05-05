import pathlib

BASE = pathlib.Path(r"C:\Users\greg\dev\clawpack_v2\agents\webclaw\references\mediclaw\jurisdictions\us\MI\state\medi_resources")
BASE.mkdir(parents=True, exist_ok=True)

(BASE / "medi_state.md").write_text("""# Michigan Medical Resources — State Overview

## Medical Schools (Allopathic — MD)
- University of Michigan Medical School — Ann Arbor — https://www.medicine.umich.edu/medschool/
- Wayne State University School of Medicine — Detroit — https://www.med.wayne.edu/
- Michigan State University — College of Human Medicine — East Lansing/Grand Rapids/Flint — https://www.chm.msu.edu/
- Western Michigan University — Homer Stryker M.D. School of Medicine — Kalamazoo — https://www.med.wmich.edu/
- Oakland University — William Beaumont School of Medicine — Rochester — https://www.oakland.edu/medicine/
- Central Michigan University — College of Medicine — Mount Pleasant — https://www.cmich.edu/colleges/med

## Medical Schools (Osteopathic — DO)
- Michigan State University — College of Osteopathic Medicine — East Lansing/Detroit/Macomb — https://www.com.msu.edu/

## Physician Assistant Programs
- University of Detroit Mercy — PA Program — https://www.udmercy.edu/pa
- Wayne State University — PA Program — https://www.pa.wayne.edu/
- Western Michigan University — PA Program — Kalamazoo — https://www.wmich.edu/pa
- Grand Valley State University — PA Program — Grand Rapids — https://www.gvsu.edu/pa/
- Central Michigan University — PA Program — Mount Pleasant — https://www.cmich.edu/pa
- Eastern Michigan University — PA Program — Ypsilanti — https://www.emich.edu/pa/
- University of Michigan-Flint — PA Program (developing)

## Nursing Schools — Baccalaureate & Higher
- University of Michigan — School of Nursing — Ann Arbor — https://www.nursing.umich.edu/
- Wayne State University — College of Nursing — Detroit — https://www.nursing.wayne.edu/
- Michigan State University — College of Nursing — East Lansing — https://www.nursing.msu.edu/
- University of Detroit Mercy — College of Health Professions — Nursing — https://www.udmercy.edu/nursing
- Oakland University — School of Nursing — Rochester — https://www.oakland.edu/nursing/
- Grand Valley State University — Kirkhof College of Nursing — Grand Rapids — https://www.gvsu.edu/nursing/
- Western Michigan University — Bronson School of Nursing — Kalamazoo — https://www.wmich.edu/nursing/
- Eastern Michigan University — School of Nursing — Ypsilanti — https://www.emich.edu/nursing/
- Central Michigan University — School of Nursing — Mount Pleasant — https://www.cmich.edu/nursing
- Northern Michigan University — School of Nursing — Marquette — https://www.nmu.edu/nursing/
- Ferris State University — School of Nursing — Big Rapids — https://www.ferris.edu/nursing
- Saginaw Valley State University — Nursing — https://www.svsu.edu/nursing/
- University of Michigan-Flint — School of Nursing — https://www.umflint.edu/nursing/
- Lake Superior State University — Nursing — Sault Ste. Marie — https://www.lssu.edu/nursing/
- Calvin University — Nursing — Grand Rapids — https://www.calvin.edu/nursing
- Hope College — Nursing — Holland — https://www.hope.edu/nursing/
- Madonna University — Nursing — Livonia — https://www.madonna.edu/nursing
- Davenport University — Nursing — Grand Rapids — https://www.davenport.edu/nursing
- Finlandia University — Nursing (closed 2023)
- Andrews University — Nursing — Berrien Springs — https://www.andrews.edu/nursing/
- Spring Arbor University — Nursing — https://www.arbor.edu/nursing/
- Concordia University Ann Arbor — Nursing — https://www.cuaa.edu/nursing

## Nursing Schools — ADN Programs
- Alpena Community College — Nursing (ADN) — https://www.alpenacc.edu/nursing
- Bay College — Nursing (ADN) — Escanaba — https://www.baycollege.edu/nursing
- Delta College — Nursing (ADN) — University Center — https://www.delta.edu/nursing
- Glen Oaks Community College — Nursing (ADN) — Centreville — https://www.glenoaks.edu/nursing
- Gogebic Community College — Nursing (ADN) — Ironwood — https://www.gogebic.edu/nursing
- Grand Rapids Community College — Nursing (ADN) — https://www.grcc.edu/nursing
- Henry Ford College — Nursing (ADN) — Dearborn — https://www.hfcc.edu/nursing
- Jackson College — Nursing (ADN) — https://www.jccmi.edu/nursing
- Kellogg Community College — Nursing (ADN) — Battle Creek — https://www.kellogg.edu/nursing
- Kirtland Community College — Nursing (ADN) — Grayling — https://www.kirtland.edu/nursing
- Lake Michigan College — Nursing (ADN) — Benton Harbor — https://www.lakemichigancollege.edu/nursing
- Lansing Community College — Nursing (ADN) — https://www.lcc.edu/nursing
- Macomb Community College — Nursing (ADN) — Warren — https://www.macomb.edu/nursing
- Mid Michigan College — Nursing (ADN) — Harrison — https://www.midmich.edu/nursing
- Monroe County Community College — Nursing (ADN) — https://www.monroeccc.edu/nursing
- Montcalm Community College — Nursing (ADN) — Sidney — https://www.montcalm.edu/nursing
- Mott Community College — Nursing (ADN) — Flint — https://www.mcc.edu/nursing
- Muskegon Community College — Nursing (ADN) — https://www.muskegoncc.edu/nursing
- North Central Michigan College — Nursing (ADN) — Petoskey — https://www.ncmich.edu/nursing
- Northwestern Michigan College — Nursing (ADN) — Traverse City — https://www.nmc.edu/nursing
- Oakland Community College — Nursing (ADN) — https://www.oaklandcc.edu/nursing
- Schoolcraft College — Nursing (ADN) — Livonia — https://www.schoolcraft.edu/nursing
- Southwestern Michigan College — Nursing (ADN) — Dowagiac — https://www.swmich.edu/nursing
- St. Clair County Community College — Nursing (ADN) — Port Huron — https://www.sc4.edu/nursing
- Washtenaw Community College — Nursing (ADN) — Ann Arbor — https://www.wccnet.edu/nursing
- Wayne County Community College — Nursing (ADN) — Detroit — https://www.wcccd.edu/nursing
- West Shore Community College — Nursing (ADN) — Scottville — https://www.westshore.edu/nursing

## Pharmacy Schools
- University of Michigan — College of Pharmacy — Ann Arbor — https://www.pharmacy.umich.edu/
- Wayne State University — Eugene Applebaum College of Pharmacy — Detroit — https://www.pharmacy.wayne.edu/
- Ferris State University — College of Pharmacy — Big Rapids/Grand Rapids — https://www.ferris.edu/pharmacy

## Dental Schools
- University of Michigan — School of Dentistry — Ann Arbor — https://www.dent.umich.edu/
- University of Detroit Mercy — School of Dentistry — https://www.udmercy.edu/dental

## Optometry School
- Ferris State University — Michigan College of Optometry — Big Rapids — https://www.ferris.edu/mco

## Public Health Schools
- University of Michigan — School of Public Health — Ann Arbor — https://www.sph.umich.edu/
- Wayne State University — School of Public Health (developing)
- Michigan State University — Master of Public Health — https://www.publichealth.msu.edu/
- University of Michigan-Flint — Public Health — https://www.umflint.edu/publichealth/

## Physical Therapy Programs
- University of Michigan — PT — Flint/Ann Arbor — https://www.umflint.edu/pt/
- Wayne State University — PT — https://www.pt.wayne.edu/
- Oakland University — PT — https://www.oakland.edu/pt/
- Central Michigan University — PT — https://www.cmich.edu/pt
- Grand Valley State University — PT — https://www.gvsu.edu/pt/
- Andrews University — PT — https://www.andrews.edu/pt/

## Occupational Therapy Programs
- University of Michigan — OT (developing)
- Wayne State University — OT — https://www.ot.wayne.edu/
- Eastern Michigan University — OT — https://www.emich.edu/ot/
- Western Michigan University — OT — https://www.wmich.edu/ot
- Grand Valley State University — OT — https://www.gvsu.edu/ot/
- Saginaw Valley State University — OT — https://www.svsu.edu/ot/

## Other Health Professions
- University of Michigan — Communication Sciences — https://www.marsalinfamilycenter.umich.edu/
- Michigan State University — Communication Sciences — https://www.comdis.msu.edu/
- Wayne State University — Communication Sciences — https://www.clas.wayne.edu/csd
- Central Michigan University — Speech-Language Pathology — https://www.cmich.edu/slp
- Western Michigan University — Speech-Language Pathology — https://www.wmich.edu/speech
- Eastern Michigan University — Speech-Language Pathology — https://www.emich.edu/csd/
- Northern Michigan University — Speech-Language Pathology — https://www.nmu.edu/csd/
- Grand Valley State University — Clinical Lab Science — https://www.gvsu.edu/cls/

## Major Hospital Systems
- Corewell Health (Beaumont + Spectrum) — 22 hospitals — https://www.corewellhealth.org/
- Trinity Health Michigan — 8 hospitals — https://www.trinityhealthmichigan.org/
- Henry Ford Health — 6 hospitals — Detroit — https://www.henryford.com/
- University of Michigan Health — Ann Arbor — https://www.uofmhealth.org/
- McLaren Health Care — 15 hospitals — https://www.mclaren.org/
- Ascension Michigan — 16 hospitals — https://www.ascension.org/michigan
- Bronson Healthcare — Kalamazoo — https://www.bronsonhealth.com/
- MidMichigan Health (U-M Health) — https://www.midmichigan.org/
- Munson Healthcare — Traverse City — https://www.munsonhealthcare.org/
- Sparrow Health System (U-M Health) — Lansing — https://www.sparrow.org/
- Children's Hospital of Michigan (DMC) — Detroit — https://www.childrensdmc.org/
- CS Mott Children's Hospital (U-M) — Ann Arbor — https://www.mottchildren.org/
- DMC Children's Hospital — Detroit — https://www.childrensdmc.org/
- Mary Free Bed Rehabilitation — Grand Rapids — https://www.maryfreebed.com/
- Pine Rest Christian Mental Health — Grand Rapids — https://www.pinerest.org/

## State Health Agencies
- Michigan Department of Health and Human Services — https://www.michigan.gov/mdhhs
- Michigan Board of Medicine — https://www.michigan.gov/lara/bureau-of-professional-licensing
- Michigan Medicaid — https://www.michigan.gov/medicaid
- Michigan Department of Health and Human Services — Behavioral Health — https://www.michigan.gov/mdhhs

## State Psychiatric Hospitals
- Walter P. Reuther Psychiatric Hospital — Westland — https://www.michigan.gov/mdhhs
- Kalamazoo Psychiatric Hospital — https://www.michigan.gov/mdhhs
- Hawthorn Center — Northville — children — https://www.michigan.gov/mdhhs
- Center for Forensic Psychiatry — Saline — https://www.michigan.gov/mdhhs
- Caro Center — Caro — https://www.michigan.gov/mdhhs

## Federal & VA
- VA Ann Arbor Healthcare System — https://www.va.gov/ann-arbor-health-care/
- John D. Dingell VA Medical Center — Detroit — https://www.va.gov/detroit-health-care/
- Battle Creek VA Medical Center — https://www.va.gov/battle-creek-health-care/
- Aleda E. Lutz VA Medical Center — Saginaw — https://www.va.gov/saginaw-health-care/
- Oscar G. Johnson VA Medical Center — Iron Mountain — https://www.va.gov/iron-mountain-health-care/

## Military Medical Facilities
- Selfridge Air National Guard Base — 127th Medical Group — https://www.127wg.ang.af.mil/
- Camp Grayling — Medical Clinic — https://www.mi.ng.mil/
- Michigan National Guard Medical Detachment — Lansing — https://www.mi.ng.mil/
- US Coast Guard Sector Detroit — Medical — https://www.atlanticarea.uscg.mil/
- US Coast Guard Air Station Traverse City — Medical — https://www.atlanticarea.uscg.mil/
""", encoding="utf-8")

# === DETROIT ===
d = BASE / "Detroit"
d.mkdir(parents=True, exist_ok=True)
(d / "medi_state.md").write_text("""# Detroit / Southeast Michigan Medical Resources

## Medical Schools (MD)
- Wayne State University School of Medicine — 540 E Canfield St, Detroit, MI 48201 — (313) 577-1000 — https://www.med.wayne.edu/
- Oakland University — William Beaumont School of Medicine — Rochester — https://www.oakland.edu/medicine/

## Medical School (DO)
- Michigan State University — College of Osteopathic Medicine — Detroit campus — https://www.com.msu.edu/

## PA Programs
- University of Detroit Mercy — PA Program — https://www.udmercy.edu/pa
- Wayne State University — PA Program — https://www.pa.wayne.edu/

## Nursing Schools
- Wayne State University — College of Nursing — https://www.nursing.wayne.edu/
- University of Detroit Mercy — Nursing — https://www.udmercy.edu/nursing
- Oakland University — School of Nursing — https://www.oakland.edu/nursing/
- University of Michigan-Flint — School of Nursing — https://www.umflint.edu/nursing/
- Madonna University — Nursing — Livonia — https://www.madonna.edu/nursing
- Eastern Michigan University — School of Nursing — Ypsilanti — https://www.emich.edu/nursing/
- Henry Ford College — Nursing (ADN) — Dearborn — https://www.hfcc.edu/nursing
- Macomb Community College — Nursing (ADN) — https://www.macomb.edu/nursing
- Oakland Community College — Nursing (ADN) — https://www.oaklandcc.edu/nursing
- Schoolcraft College — Nursing (ADN) — Livonia — https://www.schoolcraft.edu/nursing
- Wayne County Community College — Nursing (ADN) — https://www.wcccd.edu/nursing
- Washtenaw Community College — Nursing (ADN) — Ann Arbor — https://www.wccnet.edu/nursing

## Pharmacy School
- Wayne State University — Eugene Applebaum College of Pharmacy — https://www.pharmacy.wayne.edu/

## Dental School
- University of Detroit Mercy — School of Dentistry — https://www.udmercy.edu/dental

## Public Health
- Wayne State University — School of Public Health (developing)
- University of Michigan-Flint — Public Health — https://www.umflint.edu/publichealth/

## PT & OT
- Wayne State University — PT + OT — https://www.pt.wayne.edu/
- Oakland University — PT — https://www.oakland.edu/pt/
- Eastern Michigan University — OT — https://www.emich.edu/ot/

## Other Health Professions
- Wayne State University — Communication Sciences — https://www.clas.wayne.edu/csd

## Major Hospitals
- Henry Ford Hospital — 2799 W Grand Blvd, Detroit, MI 48202 — (313) 916-2600 — Level I Trauma — https://www.henryford.com/
- Detroit Receiving Hospital (DMC) — 4201 St Antoine, Detroit, MI 48201 — (313) 745-3000 — Level I Trauma — https://www.dmc.org/
- Children's Hospital of Michigan (DMC) — 3901 Beaubien Blvd, Detroit, MI 48201 — (313) 745-5437 — Level I Pediatric — https://www.childrensdmc.org/
- Harper University Hospital (DMC) — 3990 John R, Detroit, MI 48201 — (313) 745-8000 — https://www.dmc.org/
- Sinai-Grace Hospital (DMC) — 6071 W Outer Dr, Detroit, MI 48235 — (313) 966-3300 — https://www.dmc.org/
- Hutzel Women's Hospital (DMC) — 3990 John R, Detroit, MI 48201 — (313) 745-7555 — https://www.dmc.org/
- Rehabilitation Institute of Michigan (DMC) — https://www.rimrehab.org/
- Corewell Health William Beaumont University Hospital — Royal Oak — 3601 W 13 Mile Rd, Royal Oak, MI 48073 — (248) 898-5000 — Level I Trauma — https://www.corewellhealth.org/
- Corewell Health Beaumont Troy Hospital — 44201 Dequindre Rd, Troy, MI 48085 — (248) 964-5000 — https://www.corewellhealth.org/
- Corewell Health Beaumont Grosse Pointe — https://www.corewellhealth.org/
- Corewell Health Beaumont Dearborn — https://www.corewellhealth.org/
- Ascension Providence Hospital — Southfield/Novi — https://www.ascension.org/
- Ascension St. John Hospital — 22101 Moross Rd, Detroit, MI 48236 — (313) 343-4000 — https://www.ascension.org/
- Ascension Macomb-Oakland Hospital — Warren — https://www.ascension.org/
- Trinity Health Ann Arbor — St. Joseph Mercy — 5301 McAuley Dr, Ypsilanti, MI 48197 — (734) 712-3456 — https://www.trinityhealthmichigan.org/
- Trinity Health Livonia — St. Mary Mercy — https://www.trinityhealthmichigan.org/
- Trinity Health Oakland — Pontiac — https://www.trinityhealthmichigan.org/
- John D. Dingell VA Medical Center — 4646 John R, Detroit, MI 48201 — (313) 576-1000 — https://www.va.gov/detroit-health-care/
- University of Michigan Health — Ann Arbor — C.S. Mott Children's — https://www.uofmhealth.org/
- DMC Huron Valley-Sinai Hospital — Commerce — https://www.dmc.org/
- Henry Ford Macomb Hospital — Clinton Township — https://www.henryford.com/
- Henry Ford West Bloomfield Hospital — https://www.henryford.com/
- Henry Ford Wyandotte Hospital — https://www.henryford.com/
- McLaren Macomb — Mount Clemens — https://www.mclaren.org/
- McLaren Oakland — Pontiac — https://www.mclaren.org/

## Emergency (24/7 Level I Trauma)
- Henry Ford Hospital ER — (313) 916-2600
- Detroit Receiving Hospital ER — (313) 745-3000
- Children's Hospital of Michigan ER — (313) 745-5437
- Corewell Beaumont Royal Oak ER — (248) 898-5000
- Ascension St. John ER — (313) 343-4000
""", encoding="utf-8")

(d / "medi_resources.md").write_text("""# Detroit Medical Resources — Quick Reference

## 24/7 Emergency Rooms
- Henry Ford Hospital ER (Level I Trauma) — 2799 W Grand Blvd — (313) 916-2600 — https://www.henryford.com/
- Detroit Receiving Hospital ER (Level I) — 4201 St Antoine — (313) 745-3000 — https://www.dmc.org/
- Children's Hospital of Michigan ER (Level I Pediatric) — 3901 Beaubien Blvd — (313) 745-5437 — https://www.childrensdmc.org/
- Corewell Beaumont Royal Oak ER (Level I) — 3601 W 13 Mile Rd — (248) 898-5000 — https://www.corewellhealth.org/
- Ascension St. John ER — 22101 Moross Rd — (313) 343-4000 — https://www.ascension.org/
- Trinity Health Ann Arbor ER — 5301 McAuley Dr, Ypsilanti — (734) 712-3456 — https://www.trinityhealthmichigan.org/
- John D. Dingell VA ER — 4646 John R — (313) 576-1000 — https://www.va.gov/detroit-health-care/

## 24/7 Pharmacies
- CVS, Walgreens — everywhere — multiple 24hr locations

## Urgent Care
- Henry Ford Urgent Care — https://www.henryford.com/
- Corewell Health Urgent Care — https://www.corewellhealth.org/
- Ascension Urgent Care — https://www.ascension.org/
- Beaumont Urgent Care — https://www.corewellhealth.org/

## FQHCs
- Community Health and Social Services (CHASS) — https://www.chasscenter.org/
- Covenant Community Care — https://www.covenantcommunitycare.org/
- Western Wayne Family Health Centers — https://www.wwfhc.org/
- Oakland Integrated Healthcare Network — https://www.oihn.org/

## Pharmacies
- CVS, Walgreens, Kroger Pharmacy, Meijer Pharmacy — everywhere

## Mental Health
- Detroit Wayne Integrated Health Network — (800) 241-4949 — https://www.dwihn.org/
- Michigan Crisis Line — (988)
- Pine Rest (regional) — https://www.pinerest.org/

## Veterans & Military
- John D. Dingell VA — (313) 576-1000 — https://www.va.gov/detroit-health-care/
- Selfridge ANG Medical — https://www.127wg.ang.af.mil/
- USCG Sector Detroit — https://www.atlanticarea.uscg.mil/

## Public Health
- Detroit Health Department — https://www.detroitmi.gov/health
- Michigan DHHS — https://www.michigan.gov/mdhhs

## Insurance
- Michigan Medicaid — https://www.michigan.gov/medicaid
- Healthy Michigan Plan — https://www.michigan.gov/healthymiplan
""", encoding="utf-8")

print("Michigan state overview + Detroit created. Continuing with remaining cities...")
