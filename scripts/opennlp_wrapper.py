'''
' Wrapper for OpenNLP NER system evaluation.
' Model used: en-ner-location.bin
' 
'
'''

import subprocess
import os
import glob
import re

#Allows sorting of more complex file names using found integers
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]    

def main():

	inpath = os.path.expanduser('~/Desktop')

	opennlp_path = inpath + '/loc_NER_eval/OpenNLP/apache-opennlp-1.5.3/bin/opennlp'
	model_path = inpath + '/loc_NER_eval/OpenNLP/apache-opennlp-1.5.3/bin/en-ner-location.bin'
	abs_path =  os.path.expanduser('~/') + '/MastersData/NER_Sys_Eval/100_abs'
	toolName = 'TokenNameFinder'
	inputDir = sorted(glob.glob(abs_path + "/*.*"), key=natural_sort_key)

	print "Processing " + str(len(inputDir)) + " files..."

	outputDir = os.makedirs(inpath + '/opennlp_wrapper_output')

	###=====### Recursive command calls
	for idx,file in enumerate(inputDir):

		outputDoc = open(inpath + '/opennlp_wrapper_output/output_' + str(idx) + '.txt', 'w')

		with open(file) as f:

			subp_string = opennlp_path + " " + toolName + " " + model_path + " " + '<' + " " + f.name

			output = subprocess.check_output(subp_string, shell=True)

			for line in output:
				if line.find('<START:location>') != 1:
					outputDoc.write(line)


		outputDoc.close()

	
	###=====### Single command calls (test)
	# output = subprocess.check_output('/Users/holloway/Desktop/loc_NER_eval/OpenNLP/apache-opennlp-1.5.3/bin/opennlp TokenNameFinder /Users/holloway/Desktop/loc_NER_eval/OpenNLP/apache-opennlp-1.5.3/bin/en-ner-location.bin < /Users/holloway/MastersData/NER_Sys_Eval/100_abs/00001#10.1038#nrmicro1749.txt', shell=True)
	# outputDoc = open('/Users/holloway/Desktop/opennlp_wrapper_output.txt', 'w')

	# for line in output:
	# 	outputDoc.write(line)

	# outputDoc.close()


if __name__ == "__main__":
    main()