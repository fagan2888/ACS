/* This program supplements the python code in M:/IPUMS/hhdata/process_ipums.py */ 


* Format selected categorical variables into dummies 
forvalues y = 2007(1)2011 {
	insheet using M:/IPUMS/hhdata/relevant_`y'.csv, names clear 
	
	drop v1
	drop related

	* hhtype
	gen living_with_other = inlist(hhtype, "Female householder, no husband present", "Female householder, not living alone", "Male householder, no wife present", "Male householder, not living alone") 
	gen living_alone = inlist(hhtype, " Male householder, living alone", "Female householder, living alone") 
	gen living_with_fam = (hhtype == "Married-couple family household")
	
	* Ownership status	
	gen owned = inlist(ownershpd, "Owned free and clear", "Owned with mortgage or loan") 
	gen rented = inlist(ownershpd, "No cash rent", "With cash rent") 
	
	* Mortgage
	gen mortgage_status = !inlist(mortgage, "No, owned free and clear")

	* Marital status
	gen married = inlist(marst, "Married, spouse absent", "Married, spouse present")
	
	* Race
	gen white = (raced == "White") 
	gen black = (raced == "Black/Negro")
	gen orace = (!white & !black)
	
	* Education
	encode(educd), gen(educd2) 
	gen nohs = inlist(educd2, 14, 13, 10, 9, 8, 7, 6, 2)  
	gen hsgrad = inlist(educd2, 11) 
	gen college = inlist(educd2, 1, 4, 16) 
	gen postcoll = inlist(educd2, 5, 12, 15) 
	drop educd2
	
	* Employment status
	gen employed = !inlist(empstatd, "Unemployed", "N/A", "Not in Labor Force") 
	gen not_in_lf = (empstatd == "Not in Labor Force")
	
	* Not a discrete variable; recode units in structure for convenience
	gen sf = (unitsstr == "1-family house, detached")
	gen mf = !sf 
	
	* Destring continuous-valued string variables
	*Number of people in the household
	replace numprec = "1" if numprec == "1 person record"
	destring numprec, replace
	*Number of bedrooms
	replace bedrooms = "4" if bedrooms == "4 (4+ in 1960)" 
	replace bedrooms = "5" if bedrooms == "5+ (1970-2000, ACS, PRCS)"
	replace bedrooms = "0" if bedrooms == "No bedrooms"
	destring bedrooms, replace
	*Age
	replace age = "90" if age == "90 (90+ in 1980 and 1990)"
	destring age, replace
	*Number of families
	replace nfams = "1" if nfams == "1 family or N/A" 
	replace nfams = "2" if nfams == "2 families" 
	destring nfams, replace
	*Rent: replace range values with the midpoint of that range
	replace rent = "999999999999" if rent == "N/A"
	replace rent = "60" if rent == "Less than $60 (Puerto Rico)"
	replace rent = "1000" if rent == "$1,000+"
	replace rent = "10" if rent == "$1-19" 
	replace rent = "39" if rent == "$1-79" 
	replace rent = "110" if rent == "$100-119 (1960 1%)"
	replace rent = "200" if rent == "$200+ (1960 1%)"
	replace rent = "449" if rent == "$400-499  ($400+ Puerto Rico)"
	replace rent = "69" if rent == "$60-79" 
	replace rent = "89" if rent == "$80-99 (1960 1%)"
	destring rent, replace
	
	* Outsheet
	outsheet using M:/IPUMS/hhdata/hhrelevant_`y'.csv, comma replace
	}	
