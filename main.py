import Bio
from Bio import Entrez
from Bio import Medline

#list of all keywords that can be used to retrieve info from the medline db:
#https://biopython-tutorial.readthedocs.io/en/latest/notebooks/09%20-%20Accessing%20NCBIs%20Entrez%20databases.html

def fetch_details(id_list):
    try:
        ids = ','.join(id_list)#Combines id's from id_list
        Entrez.email = 'example@something.com'
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
        records = Medline.parse(handle)

        return records
    except:
        pass

#for each author tag (1 per line):
  #1 - Go through the list of pmid's and get info on each
  #2 - Append author_tag
  #3 - Write to file
def pubScraper():
	count = 0 
	print("\n\nNow scraping publications, please wait...\n\n")
	f = open('pubs.txt', 'a+')
	with open('author2citation.txt') as a:
		for line in a:
			investigator_tag = (line.split('\t')[0])
			pmidList = (line.split('\t')[1]).rstrip()
			pmidList = pmidList.split(',')
			print(investigator_tag, pmidList)
			papers = fetch_details(pmidList)
			for paper in papers:
				count+=1
				f.write(paper.get("PMID", "?")+"\t") #PUBMED ID 
				f.write(paper.get("TI", "?")+"\t") #Title
				f.write(str(paper.get("AU", "?"))+"\t") #Author List
				f.write(paper.get("AB", "?")+"\t") #Abstract
				f.write(paper.get("SO", "?")+"\t") #Source
				f.write(paper.get("DP", "?")+"\t") #Date Published
				f.write(str(paper.get("MH", "?"))+"\t") #Mesh Headers
				f.write(investigator_tag+"\n")
	print("Finished")

def authorFormatter():
	f = open('facultyListFormatted.txt', 'a+')
	with open('facultyList.txt') as a:
		#this can be reduced to one or two lines, I've expanded it and placed print statements for clarity.
		for line in a:
			indexKey = (line.split('\t')[0])
			fullName = (line.split('\t')[1])[1:-1] #This is to trim off quotation marks that appear in this particular text file.
			email = (line.split('\t')[2])
			if email.endswith('oakland.edu'): #Splits uncategorized researchers by their affiliation based on email domain
				affiliation = "Oakland University"
			else:
				affiliation = "Beaumont Research Institute"
			lastName = (line.split('\t')[3]) 
			firstName =  (line.split('\t')[4])
			location = (line.split('\t')[6])[1:-1] 
			print(indexKey)
			print(fullName)
			print(email)
			print(lastName)
			print(firstName)
			print(location)
			print(affiliation + "\n")
			f.write(indexKey + "\t")
			f.write(fullName + "\t") #This includes title (MD, PhD, etc) whereas lastName and firstName do not.
			f.write(email + "\t")
			f.write(lastName + "\t")
			f.write(firstName + "\t")
			f.write(location + "\t")
			f.write(affiliation + "\n")
	print("Finished")

if __name__ == '__main__':  
#simple terminal GUI
	print("===================================================")
	print("HIVE Automated Conversion and Data Coalation Suite")
	print("===================================================\n")
	print("Please select a functionality:\n    1 - Publication Scraper \n    2 - Author file formatter")
	inputType = int(input(""))
	if inputType == 1:
		pubScraper()
	if inputType == 2:
		authorFormatter()



