import csv

""" 
This code merges and rearranges microdata from IPUMS into formats appropriate for use by sfdem.do
""" 

# This function rearranges ACS data on single family homes by year, and outsheets in sf_by_year.csv. 
# Original data are located in sf_by_msa.csv. 
def rearrange(csvfile): 
	original = csv.DictReader(open(csvfile, 'r'))
	d = {} 
	# Only look at ACS data from 2007-11
	yearslist = range(2007, 2012, 1)
	# Get list of msas in the data
	msalist = [] 
	# Organize original file by msa and year
	for line in original: 
		msalist.append(line['metaread'])
		d[(line['metaread'], line['year'])] = line 
	msalist = list(set(msalist))
	# Get all years
	fieldnames = ['msa']
	for year in yearslist: 
		y = str(year)
		fieldnames = fieldnames + ['sfowned_total_'+ y, 'sfrental_total_'+ y, 'sf_total_'+y]
	# Look up SF info by msa and year; write to file
	output = csv.DictWriter(open('sf_by_year.csv', 'w'), lineterminator = '\n', fieldnames = fieldnames)	
	output.writerow(dict(zip(fieldnames, fieldnames)))
	for m in msalist: 
		temp = {'msa': m}
		for year in yearslist:
			y = str(year)
			line = d[(m, str(y))]
			temp.update(dict(zip(['sfowned_total_'+ y, 'sfrental_total_'+ y, 'sf_total_'+y], [line['sfowned_total'], line['sfrental_total'], line['sf_total']])))
		print temp	
		output.writerow(temp)	
#rearrange("sf_by_msa.csv")

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

matchMsaInfo("M:\IPUMS\sf_msa_info.csv", ["pctile_pchange_rentshare", "decile_pchange_rentshare", "qtile_pchange_rentshare"], "M:/IPUMS/usa_00002_msainfo.csv")

