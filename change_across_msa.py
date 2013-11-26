import csv

""" 
This script rearranges ACS data on single family homes by year. 
These data are located in sf_by_msa.csv. 
The scripts outsheets the rearranged data in sf_by_year.csv.
""" 

def rearrange(csvfile): 
	original = csv.DictReader(open(csvfile, 'r'))
	d = {} 
	for line in original: 
		year = line['year']
		msa = line['metaread']
		d[(year, msa)] = [line['sfowned_total'], line['sfrental_total'], line['sf_total']]
	fieldnames = 


	for line in d: 





	#t = 
	#for line in original: 

rearrange("sf_by_msa.csv")