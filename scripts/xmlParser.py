import xml.etree.ElementTree as ET
import glob

'''
This script is for parsing CoreNLP XML files and retrieving <NER>LOCATION</NER> tags for evaluation purposes,
using ElementTree.

Sean Holloway, NTNU 2015
OSX 10.9.5
Python 2.7.5
'''
def parseFile(filePath):

	tree = ET.parse(filePath)
	root = tree.getroot()

	#ET does not keep parent pointers, so we need to work on parent -> children 
	for token in root.iter('token'):
		for child in token.findall('NER'):
			if child.text == 'LOCATION':
				print "Found NER tag location: \n" 
				for NERtag in token.iter():
					print NERtag.tag, NERtag.text
			print "\n"
	print "\n"




	return 0


def main():
	path = raw_input("Please enter path to directory containing CoreNLP .xml output files\n:")
	fileList = glob.glob(path + "/*.xml")

	print(str(len(fileList)) + " files found for processing.\n")

	for file in fileList:
		print "Currently processing file: " + str(file)
		parseFile(str(file))

	print("Done!")

if __name__ == "__main__":
    main()