*clear 
*use M:\IPUMS\usa_00002.dta

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
by metaread year, sort: egen sfrental_total = sum(sfrental) 
by metaread year, sort: egen sf_total = sum(singlefamhouse)


*Identify financial characteristics 
by metaread year, sort: 
by metaread year, sort: 
