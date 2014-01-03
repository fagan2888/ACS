import csv
import pandas as pd 
import matplotlib.pyplot as plt 


# Split master IPUMS file into separate files by year
def splitMasterIPUMS(original_csv, years): 
	f = csv.DictReader(open(original_csv, 'r'))
	# Initialize an empty dict with bins for each year
	d = {str(y) : [] for y in years}
	# Place each line from original_csv in correct year bin
	[(d[str(line['year'])]).append(line) for line in f]
	# Write all records in each year bin into a separate csv file
	for y in d.keys(): 
		print "Writing records for " + y
		yearfile = csv.DictWriter(open("M:/IPUMS/hhdata/"+y+".csv", 'w'), fieldnames = f.fieldnames)
		yearfile.writerow(dict(zip(f.fieldnames, f.fieldnames)))
		[yearfile.writerow(line) for line in d[y]]

# Select relevant vars from each yearly dataset, write to file
def selectRelevantVars(varnames, year): 
	# Get col indices of relevant vars 
	col_indices = []
	f = csv.DictReader(open("M:/IPUMS/hhdata/"+str(year)+".csv",'r'))
	header = f.fieldnames
	[col_indices.append(header.index(v)) for v in varnames]
	# Extract relevant vars from file by col index, read into dataframe
	datafr = pd.read_csv("M:/IPUMS/hhdata/"+str(year)+".csv", usecols = col_indices)
	# Keep only hh-level obs
	datafr = datafr[datafr['related'] == "Head/Householder"]
	# Write dataframe to csv file named after year
	datafr.to_csv("M:/IPUMS/hhdata/relevant_"+str(year)+".csv", header = 'true')
	# Return dataframe with selected variables
	return datafr

# Calculate the hh-weighted avg of a var in hhs within a select msa 
def wavg(selected_df, var): 
	# Special allowance for rented types: when calculating average rent, ignore "N/A" values
	# 999999999999 is the code for "N/A"
	selected_df = selected_df[selected_df[var] != 999999999999]
	# Select column containing hh weights 
	weight = selected_df['hhwt']
	# Select column containing var of interest
	data = selected_df[var]
	# Compute weighted avg
	avg = (data*weight).sum()/ weight.sum()
	return avg

# Calculate the hh-weighted avg for a categorical var within a select msa
def wavg_catvar(selected_df, catvar, trueval): 
	weight = selected_df['hhwt']
	#data  = selected_df[catvar]
	#avg = (data*weight)
	allweight = selected_df['hhwt']
#	trueweight = selected_df['hhwt']
	truedata = selected_df[selected_df[catvar] == trueval]
	alldata = selected_df[catvar]
	avg = truedata.sum()


# Calculate hh-weighted avg of a continuous-valued var in a dataframe by msa, return values in a dict by msa
# infodict is an empty dict of dicts with msas in dataframe df as keys
def getCtsDict(infodict, df, varlist):
	# Compute weighted avg of var for each msa in the dict, place in dict 
	for m in infodict.keys(): 
		for v in varlist: 
			selected_df = df[df['metaread'] == m]
			infodict[m].update(dict(zip(["avg_" + str(v)], [wavg(selected_df, v)])))
	# Return dict with msas and weighted hh avg
	return infodict	

#def getDiscreteDict(infodict, df, catvar, true_val):
	#for m in infodict.keys(): 
	#	selected_df = df[df['meteared']] == m]
	#	infodict[m].update(dict(zip(["avg_" + str(var)], [wavg_catvar(selected_df, catvar)])))


# Take a year and list of vars, get dict hh-weighted avgs by msa
def weightedAvgByMSA(year, varlist_of_interest, varlist_of_necessity): 
	# Get hh-level dataframe with all the vars you'll need 
	df = selectRelevantVars(list(set(varlist_of_necessity + varlist_of_interest)), year)
	# Initialize empty dict of msas present in dataframe
	grouped = df.groupby('metaread')
	info = {x: {} for x in grouped.groups}	
	# For each var of interest, get weighted average by msa present in data
	for v in varlist_of_interest: 
		info.update(getValuesDict(df, v, info))
	# Return dict with weighted avgs sorted by the msas present in year
	return info

# Given a year, and hh level obs with dummies, get 4 dataframes of observations. 
def selectTenureHhtype(year, renter_status, house_type): 
	# Read the year's relevant vars/hh-level csv into a df. 
	df = pd.read_csv("M:/IPUMS/hhdata/hhrelevant_"+str(year)+".csv")
	# Create/return df that meets specified ownership_status and hhtype
	famtype = df[df[house_type] == 1]
	famtype_ownership = famtype[famtype[renter_status] == 1]
	# Return dataframe
	return famtype_ownership 




'''
Implement functions below
'''
#Specify relevant variables to extract
relevantvars = ['metaread',  # MSA 
				'year', 		 # Year
				'hhwt', 	    # Household weight
				'related',	 # Relationship to hh head
				'hhtype',	 # HH type
				'numprec',   # Num person records following
				'bedrooms',  # Num bedrooms
				'gq',		 	 # Group quarter status
				'ownershpd', # Ownership status (tenure)
				'mortgage',  # Mortgage status
				'rent',		 # Rent
				'hhincome',  # Total hh income
				'nfams',	 	 # Num families in hh 
				'unitsstr',  # Units in structure
				'age',       # Age
				'marst',		 # Marital status
				'raced',     # Detailed race
				'educd',	 	 # Education
				'empstatd']  # Employment status

# Write relevant vars at hh-level obs from master year files to a seperate file by year
#[selectRelevantVars(relevantvars, y) for y in range(2006, 2012)]

# Dummies to be aggregated (weighted average of dummies = share of population)
dummies = ['living_with_other', 'living_alone', 'living_with_fam',
			  'owned', 'rented', 'married', 'mortgage_status', 'white', 'black',
				'nohs', 'hsgrad', 'college', 'postcoll', 'employed', 'not_in_lf', 'sf', 
				'mf']

# Cts vars to be aggregated (weighted average of cts values = mean value)
cts = ['numprec', 'bedrooms', 'rent', 'hhincome', 
		 'nfams', 'age']

# Get four dataframes, each containing hh-level obs for sf/mf and rental/owner types
sf_rental = selectTenureHhtype(2007, 'rented', 'sf')
mf_rental = selectTenureHhtype(2007, 'rented', 'mf')
sf_owned = selectTenureHhtype(2007, 'owned', 'sf')
mf_owned = selectTenureHhtype(2007, 'owned', 'mf')
	
# For each of the four of the data frames, compute weighted average of each variable by MSA
dfs = [sf_rental, mf_rental, sf_owned, mf_owned]
dfnames = [1: 'sf_rental', 2: 'mf_rental', 3: 'sf_owned', 4: 'mf_owned'] 
for df in dfs: 
	# First get all the MSAs present in the dataframe and initialize an empty dictionary with msas as keys
	msas = df.groupby('metaread')
	msadict = {x: {} for x in msa.groups}
	
	# For each variable, compute the weighted average by msa and store in a dict with msas as keys
	varlist = dummies + cts					
	info = getCtsDict(msadict, df, varlist) 

	# Compile the statistics matched to msa in an output dictionary 
	fieldnames = ['msa'] + [str(year)]	+ ["avg_" + str(v) for v in varlist] 
	for k in info: 
		



	bname = dfnames[dfs.index(df)]
	f_out = csv.DictWriter(open('M:/IPUMS/hhdata/'+str(year)+'agg_'+bname+'_'+str(year)+'.csv'), fieldnames = fieldnames, dialect = excel)
	f_out.writerow(dict(zip(fieldnames, fieldnames)))
























'''
# For each year, generate 4 "buckets" (dataframes) of hh-level obs by ownership status/hhtype 
for  y in range(2007,2012): 
	print "Getting ownership status/ hhtype buckets for year " + str(y)
	
	sf_rental = selectTenureHhtype(y, 'rented', 'sf')
	sf_owner = selectTenureHhtype(y, 'owned', 'sf')
	mf_rental = selectTenureHhtype(y, 'rented', 'mf')
	mf_owner =  selectTenureHhtype(y, 'owned', 'mf')

	print "Getting msas for each bucket in " + str(y)	
	# For each bucket, get an empty dict of msas present (to later aggregate relevant vars by msa)
	sfr_grouped = sf_rental.groupby('metaread')
	sfr_msas = {x: {} for x in sfr_grouped.groups}

	sfo_grouped = sf_owner.groupby('metaread')
	sfo_msas = {x: {} for x in sfo_grouped.groups}

	mfr_grouped = mf_rental.groupby('metaread')
	mfr_msas = {x: {} for x in mfr_grouped.groups}

	mfo_grouped = mf_owner.groupby('metaread')
	mfo_msas = {x: {} for x in mfo_grouped.groups}

	print "Aggregating vars for each bucket in " + str(y)
	# For each bucket, aggregate vars by the msas present
	for v in relevantvars:
		if v in cts:  
			print getCtsDict(sfr_msas, sf_rental, v)
			sfr_msas = sfr_msas.update(getCtsDict(sfr_msas, sf_rental, v))
			sfo_msas = sfo_msas.update(getCtsDict(sfo_msas, sf_owner, v))
			mfr_msas = mfr_msas.update(getCtsDict(mfr_msas, mf_rental, v))
			mfo_msas = mfo_msas.update(getCtsDict(mfo_msas, mf_owner, v))
		#if v in cts: 
		#	break 
		#	sfr_msas = sfr_msas.update(getCtsDict(sfr_msas, sf_rental, v))
		#	sfo_msas = sfo_msas.update(getCtsDict(sfo_msas, sf_owner, v))
		#	mfr_msas = mfr_msas.update(getCtsDict(mfr_msas, mf_rental, v))
		#	mfo_msas = mfo_msas.update(getCtsDict(mfo_msas, mf_owner, v))

	# Get list of all msas present across ALL buckets this given year.
	all_msas = list(set(sfr_msas.keys() + sfo_msas.keys() + mfr_msas.keys() + mfo_msas.keys()))

	print "Combining info for all vars across all buckets by msa for " + str(y)
	# Combine info across buckets for each msa
	all_info = {x: {} for x in all_msas}
	for m in all_msas: 
		master_info = all_info[m]
		if m in sfr_msas: 
			sfr_info = sfr_msas[m]
			for k in sfr_info.keys(): 
				master_info[k + "_sfr"] = sfr_info[k]
		if m in sfo_msas: 
			sfo_info = sfo_msas[m]
			for k in sfo_info.keys(): 
				master_info[k + "_sfo"] = sfo_info[k]				
		if m in mfr_msas: 
			mfr_info = mfr_msas[m]
			for k in mfr_info.keys(): 
				master_info[k + "_mfr"] = mfr_info[k]
		if m in mfo_msas: 
			mfo_info = mfo_msas[m]
			for k in mfo_info.keys(): 
				master_info[k + "_mfo"] = mfo_info[k]

	print "Writing info to output file for " + str(y)
	# Now write to csv file T_______T 
	fieldnames = ['msa'] + [n + "_sfr" for n in relevantvars] + [n + "_sfo" for n in relevantvars] + [n + "_mfr" for n in relevantvars] + [n + "_mfo" for n in relevantvars]
	output = csv.DictWriter(open("M:/IPUMS/yearly_buckets/buckets_" + str(y) + ".csv", 'w'), fieldnames = fieldnames)
	output.writerow(dict(zip(fieldnames, fieldnames)))
	for x in all_info: 
		msainfo = {'msa': x}
		otherinfo = all_info[x]
		msainfo.update(otherinfo)
		output.writerow(msainfo)

# Run some more calculations in Stata 
# UGH T___________T

'''


'''
Scratch code 
'''

#splitMasterIPUMS("M:/IPUMS/hhlevel_housingstress.csv", range(2007, 2012))
#[selectRelevantVars(relevantvars, y) for y in range(2007, 2012)]
#col_indices = [10, 0, 4, 49, 2]
#datafr = pd.read_csv("M:/IPUMS/hhdata/2007.csv", usecols = col_indices, nrows=30)
#datafr = datafr[datafr['related'] == "Head/Householder"]
#weightedAvgByMSA('related', datafr, 'hhwt')	
#getValuesDict(datafr, ['year'])
#weightedAvgByMSA(2008, ['year', 'serial'], ['year', 'hhwt', 'related', 'metaread'])	