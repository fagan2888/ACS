import csv
import pandas as pd 
import numpy as np 
from functools import partial 
import matplotlib.pyplot as plt 




# Calculate the weighted avg of a variable within a certain subgroup of a dataframe
def wavg(df, var): 
	weight = df['hhwt']
	data = df[var]
	avg = (data*weight).sum()/ weight.sum()
	df[]



































def weightedAvg(group, var):
#
	data = group[str(var)]
	weight = group['hhwt']
	return weight
	#return (data*weight).sum()/ weight.sum()

# Get weighted average by MSA in a dataframe, accounting for hh-level weights
def weightedAvgByMSA(var, df, hhwt):
	# Group data by msa
	msagrouped = df.groupby('metaread')
	# Compute weighted average for each msa in msagrouped
	msagrouped.apply()
	#avger = partial(weightedAvg, str(var))
	#msagrouped.apply(partial(weightedAvg, str(var)))


col_indices = [10, 0, 4, 49, 2]
datafr = pd.read_csv("M:/IPUMS/hhdata/2007.csv", usecols = col_indices, nrows=30)
datafr = datafr[datafr['related'] == "Head/Householder"]
weightedAvgByMSA('related', datafr, 'hhwt')	

	

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
	# Get column indices of relevant vars 
	col_indices = []
	f = csv.DictReader(open("M:/IPUMS/hhdata/"+str(year)+".csv",'r'))
	header = f.fieldnames
	[col_indices.append(header.index(v)) for v in varnames]
	# Extract relevant vars from file by column index, read into dataframe
	datafr = pd.read_csv("M:/IPUMS/hhdata/"+str(year)+".csv", usecols = col_indices)
	# Keep only hh-level obs
	datafr = datafr[datafr['related'] == "Head/Householder"]
	# Write dataframe to csv file named after year
	datafr.to_csv("M:/IPUMS/hhdata/relevant_"+str(year)+".csv",
					header = 'true')
	# Return dataframe 
	return datafr



'''
Implement functions below
'''
#splitMasterIPUMS("M:/IPUMS/hhlevel_housingstress.csv", range(2007, 2012))

#Specify relevant variables to extract
relevantvars = ['metaread',  # MSA 
				'year', 	 # Year
				'hhwt', 	 # Household weight
				'related',	 # Relationship to hh head
				'hhtype',	 # HH type
				'numprec',   # Num person records following
				'bedrooms',  # Num bedrooms **subtract 1**
				'gq',		 # Group quarter status
				'ownershpd', # Ownership status (tenure)
				'mortgage',  # Mortgage status
				'rent',		 # Rent
				'hhincome',  # Total hh income
				'nfams',	 # Num families in hh 
				'unitsstr',  # Units in structure
				'age',       # Age
				'marst',	 # Marital status
				'raced',     # Detailed race
				'educd',	 # Education
				'empstatd']  # Employment status
#[selectRelevantVars(relevantvars, y) for y in range(2007, 2012)]