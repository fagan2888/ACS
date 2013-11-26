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

Note: remember that these are household- AND person-level variables	
	- The combo of YEAR, DATANUM, SERIAL, and PERNUM identifies unique persons
	- The combo of YEAR, DATANUM, and SERIAL identifies unique households 
	- Since DATANUM = 1 for all years in this survey, no need to include in either identifier.
	
*/

********
/*Prep*/
********
**********************************************************************
*Identify MSAs with LARGE shifts in owner-occupied or rental SF homes 
**********************************************************************
*Identify single family homes
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

gen sfowned = (singlefamhouse & !renthouse)
label var sfowned "Respondent lives in single family owned housing unit" 
label define sfowned 1 "Single family owned housing unit" 0 "Other" 

*Calculate total number of SF homes, owned and rented, by MSA and year
by metaread year, sort: egen sfowned_total = sum(sfowned)
label var sfowned_total "Total owner-occupied single family homes"
by metaread year, sort: egen sfrental_total = sum(sfrental) 
label var sfrental_total "Total renter-occupied single family homes"
by metaread year, sort: egen sf_total = sum(singlefamhouse)
label var sf_total "Total single family homes"

*Table 1: number of SF family homes (owned, rented, and total) by year and MSA
gen unique_hhid = string(year) + "-" + string(serial)	
label var unique_hhid "Unique household ID" 
gen unique_personid = string(year) + "-" + string(serial) + "-" + string(pernum) 
label var unique_personid = "Unique person ID" 

preserve 

duplicates drop metaread year
keep sfowned_total sfrental_total sf_total year metarea* 	



*Identify financial characteristics 
by metaread year, sort: 
by metaread year, sort: 
