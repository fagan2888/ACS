from __future__ import division
import csv
import pandas as pd
import numpy as np
import subprocess 

# Will use for filling blank dataframes
randn = np.random.randn

# Get the number of relative and non-relative members in each household 
def relatives(group): 
	(serialid, hhinfo) = group
	output = pd.DataFrame(index = hhinfo.index.values)
	nrels = ['Partner, friend, visitor', 'Other non-relatives', 'Institutional inmates']
	criterion_nrel = hhinfo['relate'].map(lambda x: x in nrels)
	criterion_rel = hhinfo['relate'].map(lambda x: x not in nrels)
	nrel_df = hhinfo[criterion_nrel]
	rel_df = hhinfo[criterion_rel]
	output['nonrel_share'] = nrel_df['relate'].count()/ hhinfo['relate'].count()
	output['rel_share'] = rel_df['relate'].count()/ hhinfo['relate'].count()
	output['num_nonrel'] = nrel_df['relate'].count()
	output['num_rel'] = rel_df['relate'].count()
	return output

# Get the number of adults aged > 18 who is not the household head, or the head's spouse/ cohabiting partner 
def addlAdult(group):
	(serialid, hhinfo) = group
	output = pd.DataFrame(index = hhinfo.index.values)
	age18_criterion = hhinfo['age'].map(lambda x: x >= 18) # Identify people who are 18 or older
	age24_criterion = hhinfo['age'].map(lambda x: x > 24) # Identify people who are 24 or older
	schoolage_criterion = hhinfo['age'].map(lambda x: 18 <= x <= 24) # Identify people who are between 18-24 
	spouse_criterion = hhinfo['related'].map(lambda x: x not in ['Spouse', 'Head/Householder', 'Unmarried partner']) # Identify people who are not the household head, nor the unmarried partner or spouse of head
	educ_criterion = hhinfo['schltype'].map(lambda x: x not in ['Public school', 'Private school (1960,1990-2000,ACS,PRCS)'])
	adults1 = hhinfo[schoolage_criterion & spouse_criterion & educ_criterion] # People aged 18-24 who are not the head, or the spouses/partners of the head, and are not in school
	adults2 = hhinfo[age24_criterion & spouse_criterion] 	# People who are older than 24 and not the head, nor the spouses/partners of the head
	adults_sharing = (adults1.append(adults2)).drop_duplicates(cols = 'pernum') # All adults older than 18 who are not the head, or spouses/partners of the head, exluding students aged 18-14
	adults_sharing2 = hhinfo[age18_criterion & spouse_criterion] 	# An alternate definition of adults sharing, just to test for fun
	output['adults_sharing'] = adults_sharing['pernum'].count()
	output['adults_sharing2'] = adults_sharing2['pernum'].count()
	return output

# Get the weighted count of a variable in a dataframe
def wcount(df, var, weight): 
	data = df[var]
	wt = df[weight]
	count = (data*weight).sum()
	return count

# Get the weighted average of a variable in a dataframe
def wavg(df, var, weight): 
	# Special allowance for rented types: when calculating average rent, ignore "N/A" values
	data = df[df[var] != "No rent reported"] 
 	wt = df[weight]
	avg = (data*weight).sum()/ weight.sum()
	return avg

# Run a stata do file with any parameters 
def dostata(dofile, *params): 
	cmd = ["C:/Program Files (x86)/Stata12/StataSE-64", "do", dofile]
	[cmd.append(p) for p in params]
	subprocess.call(cmd, shell = 'true')

# Compute national averages for varlist
def computeNatlAvg(df, varlist):
	weight = df['hhwt']
	outputkeys = [x for x in varlist if x not in ['hhwt', 'metaread', 'year']]
	output = {}
	#print "Computing national average"
	for v in outputkeys: 
		avg = (df[v]*weight).sum()/weight.sum()
		output.update({v: avg})
	return output

# Compute MSA level avgs for varlist
def computeMsaAvg(df, varlist): 
	output = [] 
	grouped = df.groupby('metaread')
	for group in grouped: 
		m, data = group 
		info = computeNatlAvg(data, varlist)
		info.update({'msa': m})
		output.append(info)
	return output

'''Implement functions below''' 

# Select the variables of interest 
varnames =  ['metaread',  # MSA 
				'year', 	 # Year 
				'hhwt', 	 # Household weight
				'relate',	 # Relationship to hh head
				'hhtype',	 # HH type
				'numprec',   # Num person records following
				'bedrooms',  # Num bedrooms
				'gq',		 # Group quarter status
				'ownershpd', # Ownership status (tenure)
				'mortgage',  # Mortgage status
				'rent',		 # Rent
				'hhincome',  # Total hh income
				'nfams',	 # Num families in hh 
				'unitsstr',  # Units in structure
				'age',       # Age
				'marst',     # Marital status
				'raced',     # Detailed race
				'educd',	 # Education
				'empstatd',  # Employment status
				'serial', 	 # Household ID
				'nsubfam',   # Number of subfamilies
				'nfams',     # Number of families
				'ncouples',  # Number of couples
				'multgend',  # Number of generations living together
				'famsize',   # Size of family
				'subfam', 	 # Subfam
				'famunit', 	 # Family unit
				'schltype',	 # School enrollement/type 	
				'related',   # Relationship to hh head w/ detail	
				'pernum',	 # Unique person id within family unit
				'sfrelate']  # Relationship within subfamily 
print varnames

# Read in variables of interest from csv to dataframe with correct column labels
years = [2007] 
for y in years: 
	print str(y)
	fname = 'M:/IPUMS/hhdata/'+str(y)+'.csv'
	f = csv.DictReader(open(fname, 'r'))
	header = f.fieldnames 
	cindices = [header.index(v) for v in varnames]
	df = pd.read_csv(fname, usecols = cindices)

	# Group dataframe by MSA 
	msagr = df.groupby('metaread')

		# Count number of total households within each MSA
			# Get number of SFR, MFR, SFO, MFO 
	
		# Count number of hh with additional adult
			# Get number of SFR, MFR, SFO, MFO 

		# Count number of households with additional adult and a subfamily 
			# Get number of SFR, MFR, SFO, MFO 

		# Count the number of households with additional adult aged >= 35
			# Get number of SFR, MFR, SFO, MFO 

 


	''' 

	# Group dataframe by household
	dfgr = df.groupby('serial')

	# Append each household's sharing info to the household's group 
	collect_dicts = []
	oname = "M:/IPUMS/hhdata/hhsharing/" + str(y) + 'relevant.csv'
	h = varnames + ['rel_share','adults_sharing', 'adults_sharing2','nonrel_share', 'num_nonrel', 'num_rel']
	o = csv.DictWriter(open(oname, 'wb'), fieldnames = h)
	o.writerow(dict(zip(h, h)))
	for group in dfgr:
		(serialid, hhinfo) = group
		attached = (pd.concat([relatives(group), addlAdult(group)], axis = 1)).drop_duplicates()

		# Keep only the hh-head observation. Note that institutional inmates and other non-relatives who make up a single-member family are dropped
		head = hhinfo[hhinfo['relate'] == 'Head/Householder']
		if head['serial'].count() > 0:
			head2 = pd.concat([attached, head], axis = 1)
			head_dict = head2.to_dict(outtype = 'dict')

			# Convert the info from dataframe format to a dict, and write to csv
			o.writerow({k: (head_dict[k])[x] for k in head_dict for x in head_dict[k]})
			#collect_dicts.append({k: (head_dict[k])[x] for k in head_dict for x in head_dict[k]})
	'''
'''
# Clean up yearly datasets (recode vars, etc) with stata code 
dofile = r"M:\IPUMS\hhsharing_panel.do"
cmd = ["stata", "do", dofile]
dostata(dofile)
'''
'''
#years = [2011]
years = range(2007,2012)
for y in years: 
	# Read each cleaned file into a dataframe 
	fname = "M:/IPUMS/hhdata/hhsharing/" + str(y) + "full.csv"
	f = csv.DictReader(open(fname, 'rb'))
	header = f.fieldnames 
	varlist = ['hhwt', 'metaread', 'year', 'sharedhh', 'num_addl']
	colindices = [header.index(v) for v in varlist]
	df = pd.read_csv(fname, usecols = colindices)
	print "Read " + str(y) + " into dataframe"

	# Compute national and msa level averages of variables in varlist 
	print "Computing national and msa level averages for " + str(y)
	natlavg = computeNatlAvg(df, varlist)
	msa_avg = computeMsaAvg(df, varlist)

	# Write the national and msa level averages into a csv file. 
	print "Writing national and msa level averages for " + str(y)
	dfnatlavg = pd.DataFrame([natlavg])
 	dfnatlavg.to_csv("M:/IPUMS/hhdata/hhsharing_national" + str(y) + ".csv", header = 'true')

 	df_msa_avg = pd.DataFrame(msa_avg)
 	df_msa_avg.to_csv("M:/IPUMS/hhdata/hhsharing/hhsharing_" + str(y) + ".csv", header = 'true') 
'''

