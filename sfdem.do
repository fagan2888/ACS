clear 
use M:\IPUMS\usa_00002.dta

/*This program runs analyses on IPUMS ACS data from 2007-onward with the following
questions in mind: 
Prep: 
1. Identify MSAs with large shifts in owner occupied or rental SF homes
2. Look for characteristics of population/housing in MSAs with the greatest shift

Q1: Is change in homeownership rate a different statistic for change in owner-occupied SF? 

Q2: Look at SF renters who moved WITHIN county. 
	- Do their income/hhld size/etc look unusual? 
	- How do they differ from rest of populaton (in terms of financial/ demographics)?
	- How does their new housing unit/ hh structure differ? 

Note: these are household- AND person-level variables	
	- The combo of YEAR, DATANUM, SERIAL, and PERNUM identifies unique persons
	- The combo of YEAR, DATANUM, and SERIAL identifies unique households 
	- Since DATANUM = 1 for all years in this survey, no need to include in either identifier.
	- Use the following code to distinguish between unique persons and unique households
		gen unique_hhid = string(year) + "-" + string(serial)	
		label var unique_hhid "Unique household ID" 
		gen unique_personid = string(year) + "-" + string(serial) + "-" + string(pernum) 
		label var unique_personid = "Unique person ID" 
*/

********
/*Prep*/
********
**********************************************************************
*Identify MSAs with LARGE shifts in owner-occupied or rental SF homes 
**********************************************************************
/*Identify single family homes
gen singlefamhouse = (unitsstr == 3)
label var singlefamhouse "Respondent lives in a single family house" 
label define singlefamhouse 1 "Single family house" 0 "Other"  

*Identify rented housing units
gen renthouse = inlist(ownershpd, 21, 22) 
label var renthouse "Respondent lives in a rented housing unit" 
label define renthouse 1 "Rented housing unit" 0 "Non-rented housing unit" 

*Identify single family rented and owned housing units 
gen sfrental = (singlefamhouse & renthouse)
label var sfrental "Respondent lives in single family rental housing unit" 
label define sfrental 1 "Single family housing unit" 0 "Other" 

gen sfowned = (singlefamhouse  owner-& !renthouse)
label var sfowned "Respondent lives in single family owned housing unit" 
label define sfowned 1 "Single family owned housing unit" 0 "Other" 

*Calculate total number of SF homes, owned and rented, by MSA and year
by metaread year, sort: egen sfowned_total = sum(sfowned)
label var sfowned_total "Totaloccupied single family homes"
by metaread year, sort: egen sfrental_total = sum(sfrental) 
label var sfrental_total "Total renter-occupied single family homes"
by metaread year, sort: egen sf_total = sum(singlefamhouse)
label var sf_total "Total single family homes"

*Organize number of SF family homes (owned, rented, and total) by year and MSA. 
duplicates drop metaread year
keep sfowned_total sfrental_total sf_total year metarea* 	
outsheet using sf_by_msa.csv, comma replace
*The code to create this is found in change_across_msa.py
*Resulting data in sf_by_msa.csv

insheet using "M:\IPUMS\sf_by_year.csv", names clear 
*Calculate shifts in owner-/renter-occupied/total SF across time
forvalues y = 2007(1)2011 {
	gen rental_share_`y' = 100*sfrental_total_`y'/sf_total_`y' 
	gen owner_share_`y' = 100*sfowned_total_`y'/sf_total_`y'
} 
gen pchange_rental_share = 100*(rental_share_2011 - rental_share_2007)/rental_share_2007
gen pchange_owner_share = 100*(owner_share_2011 - owner_share_2007)/owner_share_2007
gen pchange_total_sf = 100*(sf_total_2011 - sf_total_2007)/sf_total_2007
/*Export sheets to excel
export excel using sf_aggregate_ipums, sheet("Overall") sheetreplace firstrow(variables)
forvalues y = 2007(1)2011 { 
export excel msa sfowned_total_`y' sfrental_total_`y' sf_total_`y' using sf_aggregate_ipums, sheet("`y'") sheetreplace firstrow(variables)
}*/


*Place MSAs into quantile categories: what are the MSAs with the greatest shift in SF rentals? 
	*Overall percentile
	egen n = count(pchange_rental_share)
	egen i = rank(pchange_rental_share), track
	gen pctile_pchange_rentshare = 100*(i-1)/(n-1)
	*Deciles
	xtile decile_pchange_rentshare = pchange_rental_share, nq(10)
	*Quintiles 
	xtile qtile_pchange_rentshare = pchange_rental_share, nq(5)
	outsheet using "M:\IPUMS\sf_msa_info.csv", comma replace
	*Attach msa buckets to individual-level data. Code in change_across_msa.py*/


*Place MSAs into geographical categories: do housing/unemployment trends differ by region/ climate
	*Overall percentile
	*by metarea, sort: egen n = count(pchange_rental_share)

*Keep unique hh obs only (i.e. isolate hh level data)
duplicates drop unique_hhid, force







