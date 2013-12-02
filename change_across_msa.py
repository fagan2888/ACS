import csv

""" 
This script rearranges ACS data on single family homes by year. 
These data are located in sf_by_msa.csv. 
The script outsheets the rearranged data in sf_by_year.csv.
""" 

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