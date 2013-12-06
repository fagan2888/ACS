import csv

""" 
This code merges and rearranges microdata from IPUMS into formats appropriate for use by sfdem.do
""" 

# This function rearranges rectangular ACS data on single family homes by year, and outsheets in outfile. 
# Original data are located in csvfile. newvars is a list of relevant variables.
def rearrange(csvfile, outputfile, newvars): 
	original = csv.DictReader(open(csvfile, 'r'))
	d = {} 
	# Only look at ACS data from 2007-11
	yearslist = range(2007, 2012, 1)
	# Get list of msas in the data
	msalist = [] 
	# Organize original file by msa and year
	for line in original: 
		if (line['metaread'], line['year']) not in d:
			#print (line['metaread'], line['year']) 
			d[(line['metaread'], line['year'])]	= line
		if line['metaread'] not in msalist:
			msalist.append(line['metaread'])
	fieldnames = ['msa']
	for year in yearslist: 
		fieldnames = fieldnames + [var + str(year) for var in newvars]
	# Look up SF info by msa and year; write to file
	output = csv.DictWriter(open(outputfile, 'w'), lineterminator = '\n', fieldnames = fieldnames)	
	output.writerow(dict(zip(fieldnames, fieldnames)))
	for m in msalist: 
		temp = {'msa': m}
		newinfo = {}
		for year in yearslist:
			line = d[(m, str(year))]
			newinfo = {var+str(year): line[var] for var in newvars}
			temp.update(newinfo)	
		output.writerow(temp)	

csvfile = "M:/IPUMS/hhlevel_housingstress.csv"
outputfile = "M:/IPUMS/rearranged_housing_stress.csv"
newvars = ["num_nonfamhh", "num_hh", "share_nonfamhh", "avg_num_nonrelative", 
		   "avg_hhsize", "avg_occ_per_room", "avg_num_bedrooms"]		
rearrange(csvfile, outputfile, newvars)
	




# This function matches individual-level observations to MSA-level statistics
# varlist is a list of MSA-level variables 
# csvfile is the spreadsheet containing MSA-level observations
# outputfile contains hh-level obs matched with MSA-level stats
def matchMsaInfo(csvfile, varlist, outputfile): 
	msaobs = csv.DictReader(open(csvfile, 'rb'))
	# Generate dictionary of MSAs --> vars
	d = {}
	for line in msaobs: 
		d[line['msa']] = {}
		[(d[line['msa']]).update({v: line[v]}) for v in varlist]
	# Match MSA info to hh-level obs; write to outputfile
	hhinfo = csv.DictReader(open( "M:/IPUMS/usa_00002.csv", 'r'))
	fieldnames = hhinfo.fieldnames + varlist
	output = csv.DictWriter(open(outputfile, 'w'), fieldnames = fieldnames, lineterminator = '\n')
	output.writerow(dict(zip(fieldnames, fieldnames)))
	for line in hhinfo: 
		msainfo = d[line['metaread']]
		line.update(msainfo)
		output.writerow(line)
#matchMsaInfo("M:\IPUMS\sf_msa_info.csv", ["pctile_pchange_rentshare", "decile_pchange_rentshare", "qtile_pchange_rentshare"], "M:/IPUMS/usa_00002_msainfo.csv")

# This function rearranges 