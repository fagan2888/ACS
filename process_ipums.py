from __future__ import division
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
	# 9999999 is the code for "N/A"
	selected_df = selected_df[selected_df[var] < 9999999]
	# Select column containing hh weights 
	weight = selected_df['hhwt']
	# Select column containing var of interest
	data = selected_df[var]
	# Compute weighted avg
	avg = (data*weight).sum()/ weight.sum()
	return avg

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

# Given a dataframe and an empty dictionary of MSAs, compute the freq weight for each MSA
def sumWeights(infodict, df, key): 
	for m in infodict.keys(): 
		selected = df[df['metaread'] == m]
		weights = selected['hhwt']
		infodict[m].update(dict(zip(['fweight_' + key], [weights.sum()])))
	return infodict

def meanRent(infodict, df, key): 
	for m in infodict.keys():
		selected = df[df['metaread'] == m]
		no_errors_only = selected[selected['rent'] < 9999999] 
		weights = no_errors_only['hhwt']
		data = no_errors_only['rent']
		avg = (weights*data).sum()/ weights.sum()
		infodict[m].update(dict(zip(['avgrent_'+ key], [avg])))
	return infodict




'''
Implement functions below
'''
'''
Section I. The following script: 
a. Extracts relevant variables from master IPUMS file
b. Aggregates by household
c. Computes averages of desired variables by MSA, sf/mf and renter/owner types.

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

# Dummies to be aggregated (weighted average of dummies = share of population matching that characteristic)
# Think expected value
dummies = ['living_with_other', 'living_alone', 'living_with_fam',
			  'owned', 'rented', 'married', 'mortgage_status', 'white', 'black',
				'nohs', 'hsgrad', 'college', 'postcoll', 'employed', 'not_in_lf', 'sf', 
				'mf']

# Cts vars to be aggregated (weighted average of cts values = mean value)
cts = ['numprec', 'bedrooms', 'rent', 'hhincome', 
		 'nfams', 'age']

yearlist = range(2009, 2012)
#yearlist = range(2008, 2012)
for year in yearlist: 
# Get four dataframes, each containing hh-level obs for sf/mf and rental/owner types
	print "Placing hh-level obs in separate sf/ mf owner/renter buckets for " + str(year)
	sf_rental = selectTenureHhtype(year, 'rented', 'sf')
	mf_rental = selectTenureHhtype(year, 'rented', 'mf')
	sf_owned = selectTenureHhtype(year, 'owned', 'sf')
	mf_owned = selectTenureHhtype(year, 'owned', 'mf')
	full = sf_owned.append(sf_rental, mf_rental, mf_owned)
	

# For each of the four of the data frames, compute weighted average of each variable by MSA
	# First get all the MSAs present in the dataframe and initialize an empty dictionary with msas as keys
	print "Getting MSAs present in all buckets for " + str(year)
	msas = full.groupby('metaread')
	msadict = {x: {} for x in msas.groups}
	
	# For each variable, compute the weighted average by msa and store in a dict with msas as keys
	print "Computing statistics of key vars in each bucket for " + str(year)
	varlist = dummies + cts				
	print "	For sfrental"
	stats_sfrental = getCtsDict(msadict, sf_rental, varlist) 
	print "	For sfowned"
	stats_sfowned = getCtsDict(msadict, sf_owned, varlist)
	print "	For mfrental"
	stats_mfrental = getCtsDict(msadict, mf_rental, varlist)
	print "	For mfowned"
	stats_mfowned = getCtsDict(msadict, mf_owned, varlist)
	fieldnames = ['msa'] + [str(year)]	+ ["avg_" + str(v) for v in varlist]
	info = stats_sfowned

	bname = 'sf_owned'
	print "Compiling stats in " + bname + " bucket into a single dict for " + str(year)
	output = []
	for k in info: 
		msa = dict(zip(['msa'], [k]))
		msa.update(info[k])
		output.append(msa)
	# Write to a csv file	
	print "Writing info about " + bname + " bucket in " + str(year) + " to a csv file"
	fname = "M:/IPUMS/hhdata/" + bname + str(year) + ".csv"
	f_out = csv.DictWriter(open(fname, "wb"), fieldnames = fieldnames)
	f_out.writerow(dict(zip(fieldnames, fieldnames)))
	for l in output: 
		f_out.writerow(l) 
'''

'''
Section II: 
a. Retrieve frequency weights for each sf/mf and owner/renter bucket by MSA for each year
b. Combine with appropriate spreadsheet 
'''


yearlist = range(2007, 2012) 
for y in yearlist: 
	# Extract each bucket into a dataframe
	sf_rental = selectTenureHhtype(y, 'rented', 'sf')
	mf_rental = selectTenureHhtype(y, 'rented', 'mf')
	#sf_owned = selectTenureHhtype(y, 'owned', 'sf')
	#mf_owned = selectTenureHhtype(y, 'owned', 'mf')
	print "Extracted buckets for year " + str(y)

	# Get list of MSAs
	full = sf_rental.append(mf_rental)
	msas = full.groupby('metaread')
	msadict = {x: {} for x in msas.groups}
	print "Compiled empty dict of MSAs in " + str(y)

	# For each bucket (dataframe), get freq weight for all MSAs
	sfrdict = sumWeights(msadict, sf_rental, 'sfr')
	mfrdict = sumWeights(msadict, mf_rental, 'mfr')
#	sfodict = sumWeights(msadict, sf_owned, 'sfo')
#	mfodict = sumWeights(msadict, mf_owned, 'mfo')
	sfrdict.update(mfrdict)
	print "Calculated freq weight sums by MSA for " + str(y)
	#print sfrdict

	# Attach freq weights by msa to appropriate yearly spreadsheet 
#	namestubs = {'sf_rental': 'sfr', 'mf_rental': 'mfr', 'sf_owned': 'sfo', 'mf_owned': 'mfo'}
	namestubs = {'sf_rental': 'sfr', 'mf_rental': 'mfr'}
	fnames = dict(zip(namestubs.keys(), ["M:/IPUMS/hhdata/"+n+str(y)+"_rentavg.csv" for n in namestubs.keys()]))
	new = dict(zip(namestubs.keys(), ["M:/IPUMS/hhdata/"+n+str(y)+"_fwt_rentavg.csv" for n in namestubs.keys()]))
	for f in namestubs.keys(): 
		print "Writing info for " + f + " in " + str(y)
		orig = csv.DictReader(open(fnames[f], 'rb'))
		h = orig.fieldnames + ['fweight_' + namestubs[f]]
		out = csv.DictWriter(open(new[f], 'wb'), fieldnames = h)
		out.writerow(dict(zip(h,h)))
		key = 'fweight_' + namestubs[f]
		for l in orig: 
			msa = l['msa']
			allfreqs = sfrdict[msa]
			info = dict(zip(['fweight_' + namestubs[f]], [allfreqs[key]]))
			l.update(info)
			out.writerow(l)

'''
Section III. Fix rent variable to account for error code
'''
#yearlist = [2007]
yearlist = range(2007, 2012) 
for y in yearlist: 
	# Extract each bucket into a dataframe
	sf_rental = selectTenureHhtype(y, 'rented', 'sf')
	mf_rental = selectTenureHhtype(y, 'rented', 'mf')
	#sf_owned = selectTenureHhtype(y, 'owned', 'sf')
	#mf_owned = selectTenureHhtype(y, 'owned', 'mf')
	print "Extracted buckets for year " + str(y)

	# Get list of MSAs
	full = sf_rental.append(mf_rental)
	msas = full.groupby('metaread')
	msadict = {x: {} for x in msas.groups}
	print "Compiled empty dict of MSAs in " + str(y)

	# For each bucket, calculate mean rent for all MSAs
	sfrdict = meanRent(msadict, sf_rental, 'sfr')
	mfrdict = meanRent(msadict, mf_rental, 'mfr')
	sfrdict.update(mfrdict)
	print "Calculated mean rent for all buckets in " + str(y)

	# Attach freq weights by msa to appropriate yearly spreadsheet 
	namestubs = {'sf_rental': 'sfr', 'mf_rental': 'mfr'}
	fnames = dict(zip(namestubs.keys(), ["M:/IPUMS/hhdata/"+n+str(y)+".csv" for n in namestubs.keys()]))
	new = dict(zip(namestubs.keys(), ["M:/IPUMS/hhdata/"+n+str(y)+"_rentavg.csv" for n in namestubs.keys()]))
	for f in namestubs.keys(): 
		print "Writing info for " + f + " in " + str(y)
		orig = csv.DictReader(open(fnames[f], 'rb'))
		h = orig.fieldnames + ['avgrent_' + namestubs[f]]
		out = csv.DictWriter(open(new[f], 'wb'), fieldnames = h)
		out.writerow(dict(zip(h,h)))
		key = 'avgrent_' + namestubs[f]
		for l in orig: 
			msa = l['msa']
			allfreqs = sfrdict[msa]
			info = dict(zip(['avgrent_' + namestubs[f]], [allfreqs[key]]))
			l.update(info)
			out.writerow(l)






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

