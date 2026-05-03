import urllib.request
# NC counties with known specific URLs
nc_urls = {
'Alamance':'https://www.alamance-nc.com/','Alexander':'https://alexandercountync.gov/','Alleghany':'https://www.alleghanycounty-nc.gov/',
'Anson':'https://www.co.anson.nc.us/','Ashe':'https://www.ashecountygov.com/','Avery':'https://www.averycountync.gov/',
'Beaufort':'https://www.co.beaufort.nc.us/','Bertie':'https://www.co.bertie.nc.us/','Bladen':'https://www.bladenco.org/',
'Brunswick':'https://www.brunswickcountync.gov/','Buncombe':'https://www.buncombecounty.org/','Burke':'https://www.burkenc.org/',
'Cabarrus':'https://www.cabarruscounty.us/','Caldwell':'https://www.caldwellcountync.org/','Camden':'https://www.camdencountync.gov/',
'Carteret':'https://www.carteretcountync.gov/','Caswell':'https://www.caswellcountync.gov/','Catawba':'https://www.catawbacountync.gov/',
'Chatham':'https://www.chathamcountync.gov/','Cherokee':'https://www.cherokeecounty-nc.gov/','Chowan':'https://www.chowancounty-nc.gov/',
'Clay':'https://www.claycountync.gov/','Cleveland':'https://www.clevelandcounty.com/','Columbus':'https://www.columbusco.org/',
'Craven':'https://www.cravencountync.gov/','Cumberland':'https://www.cumberlandcountync.gov/','Currituck':'https://www.currituckcountync.gov/',
'Dare':'https://www.darenc.com/','Davidson':'https://www.co.davidson.nc.us/','Davie':'https://www.daviecountync.gov/',
'Duplin':'https://www.duplincountync.com/','Durham':'https://www.dconc.gov/','Edgecombe':'https://www.edgecombecountync.gov/',
'Forsyth':'https://www.co.forsyth.nc.us/','Franklin':'https://www.franklincountync.gov/','Gaston':'https://www.gastongov.com/',
'Gates':'https://www.gatescountync.gov/','Graham':'https://www.grahamcounty.org/','Granville':'https://www.granvillecounty.org/',
'Greene':'https://www.greenecountync.gov/','Guilford':'https://www.guilfordcountync.gov/','Halifax':'https://www.halifaxnc.com/',
'Harnett':'https://www.harnett.org/','Haywood':'https://www.haywoodcountync.gov/','Henderson':'https://www.hendersoncountync.gov/',
'Hertford':'https://www.hertfordcountync.gov/','Hoke':'https://www.hokecounty.org/','Hyde':'https://www.hydecountync.gov/',
'Iredell':'https://www.iredellcountync.gov/','Jackson':'https://www.jacksonnc.org/','Johnston':'https://www.johnstonnc.com/',
'Jones':'https://www.jonescountync.gov/','Lee':'https://www.leecountync.gov/','Lenoir':'https://www.lenoircountync.gov/',
'Lincoln':'https://www.lincolncounty.org/','Macon':'https://www.maconnc.org/','Madison':'https://www.madisoncountync.gov/',
'Martin':'https://www.martincountync.gov/','McDowell':'https://www.mcdowellgov.com/','Mecklenburg':'https://www.mecknc.gov/',
'Mitchell':'https://www.mitchellcounty.org/','Montgomery':'https://www.montgomerycountync.gov/','Moore':'https://www.moorecountync.gov/',
'Nash':'https://www.nashcountync.gov/','New_Hanover':'https://www.nhcgov.com/','Northampton':'https://www.northamptonnc.com/',
'Onslow':'https://www.onslowcountync.gov/','Orange':'https://www.orangecountync.gov/','Pamlico':'https://www.pamlicocounty.org/',
'Pasquotank':'https://www.pasquotankcountync.gov/','Pender':'https://www.pendercountync.gov/','Perquimans':'https://www.perquimanscountync.gov/',
'Person':'https://www.personcountync.gov/','Pitt':'https://www.pittcountync.gov/','Polk':'https://www.polknc.org/',
'Randolph':'https://www.randolphcountync.gov/','Richmond':'https://www.richmondnc.com/','Robeson':'https://www.co.robeson.nc.us/',
'Rockingham':'https://www.rockinghamcountync.gov/','Rowan':'https://www.rowancountync.gov/','Rutherford':'https://www.rutherfordcountync.gov/',
'Sampson':'https://www.sampsonnc.com/','Scotland':'https://www.scotlandcounty.org/','Stanly':'https://www.stanlycountync.gov/',
'Stokes':'https://www.co.stokes.nc.us/','Surry':'https://www.co.surry.nc.us/','Swain':'https://www.swaincountync.gov/',
'Transylvania':'https://www.transylvaniacounty.org/','Tyrrell':'https://www.tyrrellcounty.net/','Union':'https://www.unioncountync.gov/',
'Vance':'https://www.vancecounty.org/','Wake':'https://www.wake.gov/','Warren':'https://www.warrencountync.gov/',
'Washington':'https://www.washingtoncountync.gov/','Watauga':'https://www.wataugacounty.org/','Wayne':'https://www.waynegov.com/',
'Wilkes':'https://www.wilkescounty.net/','Wilson':'https://www.wilson-co.com/','Yadkin':'https://www.yadkincountync.gov/',
'Yancey':'https://www.yanceycountync.gov/','State':'https://www.ncosfm.gov/',
}
ok=fail=0; V={}
for n,u in nc_urls.items():
    try:
        req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
        urllib.request.urlopen(req,timeout=8)
        V[n]=u; ok+=1; print(f'OK: {n}')
    except: fail+=1; print(f'FAIL: {n}')
print(f'\n{ok} pass, {fail} fail')
