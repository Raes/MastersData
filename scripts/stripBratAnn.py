import glob
import sys
import os

'''
Script for pulling out certain annotations from Brat .ann files and listing them by file
for easily tossing into Excel. Currently output file uses OSX address.

v.1.0 Can retrieve compound, species, location annotations


Sean Holloway, NTNU 2015
'''



def main():
	
    path = str(raw_input("Please enter directory path of Brat annotation files. \n:"))
    print "\nFinding annotation files at: " + path

    fileList = glob.glob(path + "/*.ann")
    print str(len(fileList)) + " annotation files found. \n"

    annType = str(raw_input("Please enter type of annotation to retrieve. (compound, species, location) \n:"))

    if annType not in {'compound', 'species', 'location'}:
    	print "Invalid annotation type, have a nice day"
    	sys.exit(0)

    print "Creating output file on your Desktop (~/Desktop)"

    outPath = os.path.expanduser('~/Desktop')

    annFile = open(outPath + '/annotationsFile.txt' , 'w')

    for file in fileList:

    	annMatches = []

    	with open(file) as f:

    		# Write file name
    		annFile.write(f.name + '\n')

    		for line in f:
    			unformatedText = line.split()

    			if unformatedText[1] == str(annType).title():

    				if len(unformatedText[4:]) > 1:
    					annMatches.append(" ".join(unformatedText[4:]))
    				else:
    					annMatches.append(unformatedText[4])

    		for item in annMatches:

    			annFile.write(item + " ")
    		annFile.write("\n")
    	f.close()

    annFile.close()

    print "Done!"
    sys.exit(0)

if __name__ == "__main__":
    main()