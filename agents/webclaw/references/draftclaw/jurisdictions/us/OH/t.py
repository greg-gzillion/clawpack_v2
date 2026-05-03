import urllib.request
urls = {
'Adams':'https://www.arcainfo.org/','Allen':'https://www.allencountyohio.com/','Ashland':'https://www.ashlandcounty.org/',
'Ashtabula':'https://www.ashtabulacounty.us/','Athens':'https://www.athensohio.org/','Auglaize':'https://www.auglaizecounty.org/',
'Belmont':'https://www.belmontcountyohio.org/','Brown':'https://www.browncountyohio.gov/','Butler':'https://www.butlercountyohio.org/',
'Carroll':'https://www.carrollcountyohio.us/','Champaign':'https://www.co.champaign.oh.us/','Clark':'https://www.clarkcountyohio.gov/',
'Clermont':'https://www.clermontcountyohio.gov/','Clinton':'https://www.clintoncountyohio.com/','Columbiana':'https://www.columbianacounty.org/',
'Coshocton':'https://www.coshoctoncounty.net/','Crawford':'https://www.crawfordcountyohio.gov/','Cuyahoga':'https://www.cuyahogacounty.gov/',
'Darke':'https://www.darkecountyohio.com/','Defiance':'https://www.defiance-county.com/','Delaware':'https://www.co.delaware.oh.us/',
'Erie':'https://www.eriecounty.oh.gov/','Fairfield':'https://www.co.fairfield.oh.us/','Fayette':'https://www.fayette-co-oh.com/',
'Franklin':'https://www.franklincountyohio.gov/','Fulton':'https://www.fultoncountyoh.com/','Gallia':'https://www.galliacounty.org/',
'Geauga':'https://www.co.geauga.oh.us/','Greene':'https://www.greenecountyohio.gov/','Guernsey':'https://www.guernseycounty.org/',
'Hamilton':'https://www.hamiltoncountyohio.gov/','Hancock':'https://www.hancockcountyohio.gov/','Hardin':'https://www.hardincountyohio.org/',
'Harrison':'https://www.harrisoncountyohio.org/','Henry':'https://www.henrycountyohio.com/','Highland':'https://www.highlandcountyohio.com/',
'Hocking':'https://www.hockingcountyohio.gov/','Holmes':'https://www.holmescountyohio.org/','Huron':'https://www.huroncountyohio.gov/',
'Jackson':'https://www.jacksoncountyohio.gov/','Jefferson':'https://www.jeffersoncountyohio.gov/','Knox':'https://www.knoxcountyohio.org/',
'Lake':'https://www.lakecountyohio.gov/','Lawrence':'https://www.lawrencecountyohio.org/','Licking':'https://www.lickingcounty.gov/',
'Logan':'https://www.co.logan.oh.us/','Lorain':'https://www.loraincounty.us/','Lucas':'https://www.co.lucas.oh.us/',
'Madison':'https://www.co.madison.oh.us/','Mahoning':'https://www.mahoningcountyoh.gov/','Marion':'https://www.co.marion.oh.us/',
'Medina':'https://www.medinacountyohio.gov/','Meigs':'https://www.meigscountyohio.com/','Mercer':'https://www.mercercountyohio.org/',
'Miami':'https://www.miamicountyohio.gov/','Monroe':'https://www.monroecountyohio.com/','Montgomery':'https://www.mcohio.org/',
'Morgan':'https://www.morgancountyohio.gov/','Morrow':'https://www.morrowcountyohio.gov/','Muskingum':'https://www.muskingumcounty.org/',
'Noble':'https://www.noblecountyohio.gov/','Ottawa':'https://www.ottawacountyohio.gov/','Paulding':'https://www.pauldingcountyoh.com/',
'Perry':'https://www.perrycountyohio.net/','Pickaway':'https://www.pickawaycountyohio.gov/','Pike':'https://www.pikecountyohio.org/',
'Portage':'https://www.portagecounty-oh.gov/','Preble':'https://www.prebco.org/','Putnam':'https://www.putnamcountyohio.gov/',
'Richland':'https://www.richlandcountyohio.gov/','Ross':'https://www.rosscountyohio.gov/','Sandusky':'https://www.sanduskycountyohio.gov/',
'Scioto':'https://www.sciotocountyohio.gov/','Seneca':'https://www.senecacountyohio.gov/','Shelby':'https://www.shelbycountyohio.com/',
'Stark':'https://www.starkcountyohio.gov/','Summit':'https://www.summitoh.net/','Trumbull':'https://www.co.trumbull.oh.us/',
'Tuscarawas':'https://www.co.tuscarawas.oh.us/','Union':'https://www.unioncountyohio.gov/','Van_Wert':'https://www.vanwertcountyohio.gov/',
'Vinton':'https://www.vintoncountyohio.gov/','Warren':'https://www.co.warren.oh.us/','Washington':'https://www.washingtongov.org/',
'Wayne':'https://www.wayneohio.org/','Williams':'https://www.williamscountyohio.gov/','Wood':'https://www.woodcountyohio.gov/',
'Wyandot':'https://www.wyandotcountyohio.gov/','State':'https://www.com.ohio.gov/',
}
ok=fail=0; V={}
for n,u in urls.items():
    try:
        urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=8)
        V[n]=u; ok+=1; print(f'OK: {n}')
    except: fail+=1
print(f'\n{ok} pass, {fail} fail')
