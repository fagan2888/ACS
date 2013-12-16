/*
Date: 12/4/2013 
Author: Shruthi Venkatesh

This program explores various measures of housing stress using ACS microdata
We want to understand variation of the following across msa and time: 

1. % of total hh in each msa that are non-family (i.e. roommates etc) 
2. Number of non-relatives in each hh  
3. Average size of household
4. Average number of occupants/ room 
5. Number of bedrooms
*/

/*Unblock the following lines to import the dataset*/ 
*use "M:/IPUMS/usa_00002.dta", clear
*preserve

/*The following lines split the master IPUMS file by year
Records for each year are stored in a separate file
forvalues y = 2007(1)2011 {
	outsheet using "M:/IPUMS/hhdata/`y'.csv" if year == `y', comma replace
}*/

***************************************
/*Calculate meaures of housing stress*/
***************************************
*NOTE: hhwt is a frequency weight
*Identify unique households
gen unique_hhid = string(year) + "-" + string(serial)
label var unique_hhid "Unique household ID" 

*Identify unique year-msa groups
egen year_metaread_group = group(year metaread), missing 
 

*1. Share of non-family households 
	gen nonfamhh = (hhtype > 3)*(relate == 1)
	label var nonfamhh "Non-family household"
	label def nonfamhh 1 "A non-family household" 0 "A family household" 

	
	*Get weighted totals
	gen num_nonfamhh = 9999
	gen num_hh = 9999
	
	
	label var num_nonfamhh "Number of non-family households by year and msa"	
	label var num_hh "Number of households by year and msa" 
	
	forvalues i = 1(1)1490 {
	
		di `i'
		quietly summarize nonfamhh [fweight = hhwt] if year_metaread_group == `i', detail 
		replace num_nonfamhh = r(sum) if year_metaread_group == `i'  
		
		quietly summarize num_hh [fweight = hhwt] if year_metaread_group = `i'
	} 
	*by metaread year, sort: egen num_nonfamhh = total(nonfamhh) 
	
	
	by metaread year, sort: egen num_hh = total(relate==1) 
	
	
	by metaread year, sort: gen share_nonfamhh = num_nonfamhh/num_hh
	label var share_nonfamhh "Share of non-family housholds by year and msa" 	
	
*2. Number of non-relatives in each hh 
	gen nonrelative = (relate > 10)	
	by unique_hhid, sort: egen num_nonrelative = total(nonrelative)
	label var num_nonrelative "Number of non-relatives in the household" 

	by metaread year, sort: egen avg_num_nonrelative = mean(num_nonrelative)
	label var avg_num_nonrelative "Average number of non-relatives in hh by year and msa"	
	
*3. Average household size
	by metaread year, sort: egen avg_hhsize = mean(numprec)
	label var avg_hhsize "Average houshold size by year and msa" 		
		
*4. Average number of occupants per room 
	gen bedrooms2 = bedrooms-1 
	label var bedrooms2 "Raw number of bedrooms" 
	
	by unique_hhid, sort: gen occ_per_room = numprec/bedrooms2 if bedrooms2 >= 0
	label var occ_per_room "Occupants per bedroom" 
	
	by metaread year, sort: egen avg_occ_per_room = mean(occ_per_room)
	label var avg_occ_per_room "Average occupants per bedroom in each hh by year and msa" 
	
*5. Average number of bedrooms in each household
	by metaread year, sort: egen avg_num_bedrooms = mean(bedrooms2)
	label var avg_num_bedrooms "Average number of bedrooms by year and msa" 
	
	/*Uncomment the following lines to outsheet the heads only for msa-level arrangement*/
 	*drop if relate != 1
	*outsheet using "M:/IPUMS/hhlevel_housingstress.csv", comma names replace
*Organize data by msa and year: see python code in change_across_msa.py
*Reshaped data in rearranged_housing_stress.csv
	/*Uncomment the following code to create an excel file with separate tabs for each year
	insheet using rearranged_housing_stress.csv, clear
	export excel using "M:/IPUMS/aggregate_housingstress", sheet("Overall") sheetreplace firstrow(variables)
	forvalues y = 2007(1)2011 { 
		export excel msa num_nonfamhh`y' num_hh`y' share_nonfamhh`y' avg_num_nonrelative`y' avg_hhsize`y' avg_occ_per_room`y' avg_num_bedrooms`y' using "M:/IPUMS/aggregate_housingstress", sheet(`y') sheetreplace firstrow(variables)
		}*/

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
