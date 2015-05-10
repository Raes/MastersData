import xml.etree.ElementTree as ET
import glob
import os

'''
This script is for parsing CoreNLP XML files and retrieving <NER>LOCATION</NER> tags for evaluation purposes,
using ElementTree.

Sean Holloway, NTNU 2015
OSX 10.9.5
Python 2.7.5
'''
def parseFile(filePath):

	foundHits = []
	charOffsetCheck = -1

	tree = ET.parse(filePath)
	root = tree.getroot()

	#ET does not keep parent pointers, so we need to work on parent -> children 
	for token in root.iter('token'):
		for child in token.findall('NER'):
			if child.text == 'LOCATION':

				NERtokenID = 0
				NERword = 0
				NERCOB = 0
				NERCOE = 0

				for NERtag in token.iter():
					if NERtag.tag == 'token':
						NERtokenID = NERtag.get('id')
					elif NERtag.tag == 'word':
						NERword = NERtag.text
					elif NERtag.tag == 'CharacterOffsetBegin':
						NERCOB = NERtag.text
					elif NERtag.tag == 'CharacterOffsetEnd':
						NERCOE = NERtag.text

				if (int(charOffsetCheck) + 1) == int(NERCOB):
					print "Found possible tag connection"
					catHit = (foundHits.pop()).split()
					catHit[3] = NERCOE
					catHit.append(NERword)
					catHitJ = ' '.join(catHit)
					foundHits.append(catHitJ)

				else:
					foundHits.append(str(NERtokenID) + " Location " + str(NERCOB) + " " + str(NERCOE) + " " + str(NERword))

				charOffsetCheck = NERCOE

	return foundHits

def main():
	outPath = os.path.expanduser('~/Desktop')
	path = raw_input("Please enter path to directory containing CoreNLP .xml output files\n:")
	fileList = glob.glob(path + "/*.xml")

	print(str(len(fileList)) + " files found for processing.\n")

	if not os.path.isdir(outPath + '/output'):
			print "Creating output directory: " + outPath + "/output"
			os.makedirs(outPath + '/output')

	for idx,file in enumerate(fileList):
		print "Currently processing file: " + str(file)
		
		print "Creating output file"
		bratFormatFile = open(outPath + '/output/000' + str(idx+1) + 'bratFormat' + '.ann' , 'w')

		hits = parseFile(str(file))

		for item in hits:
			bratFormatFile.write(item + '\n')

		bratFormatFile.close()

		print "\n"

	print "Done!"

if __name__ == "__main__":
    main()