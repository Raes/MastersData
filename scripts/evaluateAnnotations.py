from __future__ import division
from fractions import *
import os
import glob
import re

'''
This script is for comparing two directories of files. Each file pair will look for annotation matches
and compute precision/recall/f-score for each pair. It will then compute precision/recall/f-score for total.

This script is meant to be as verbose as necessary so that it can be expanded upon by other students later.

v1.0 - compounds only

Created by: Sean Holloway 05-05-2015
Tested on: Mac OSX 10.9.5, Python 2.7.5
'''

'''
Annotation Exceptions: water
'''

#Allows sorting of more complex file names using found integers
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]    

#Gets two directory paths from user and checks if they are directories and that they have same number of files
def getPaths():

	while True:

		try:
			dir1 = str(raw_input("Please enter directory path for first directory which contains manual annotations in Brat format\n:"))
			pass
		except IOError, e:
			print "I/O error when checking first directory"

		fileList1 = sorted(glob.glob(dir1 + "/*.*"), key=natural_sort_key)
		#print "glob dir1 " + str(len(fileList1))
		#print str(fileList1)

		try:
			dir2 = str(raw_input("Please enter directory path for the second directory which contains NER results, preformatted\n:"))
			pass
		except IOError, e:
			print "I/O error when checking first directory"
			raise e

		fileList2 = sorted(glob.glob(dir2 + "/*.*"), key=natural_sort_key)
		#print "glob dir2 " + str(len(fileList2))
		#print str(fileList2)

		evalTypeList = ["compound", "location", "species"]

		try:
			evalType = str(raw_input("Please enter evaluation type; Compound, Location, Species. Single answers only: "))
			pass
			if evalType.lower() in evalTypeList:
				break
			else:
				print "That type was not in the accepted type list, please try again."
				continue
		except IOError, e:
			print "I/O Error getting type"

		if not len(fileList1) == len(fileList2):
			print str(len(fileList1)) + " files in fileList1"
			print str(len(fileList2)) + " files in fileList2"
			print "Those directories do not have the same number of files, invalid input for this script"
			continue
		else:
			break

	return fileList1, fileList2, evalType

def evalSet(file1, file2, evalType):

	split_file1 = []
	split_file2 = []
	true_pos = 0
	false_pos = 0
	gs_count= 0
	global total_true_pos
	global total_false_pos
	global total_false_neg

	
	with open(file1) as f1:

		for line in f1:
			split_line = line.split()[1:]
			if str(split_line[0].lower()) == str(evalType):
				gs_count += 1
				lc_split_line = [x.lower() for x in split_line]
				split_file1.append(lc_split_line)

	f1.close()

	with open(file2) as f2:

		for line in f2:
			split_line = line.split()[1:]
			lc_split_line = [x.lower() for x in split_line]
			split_file2.append(lc_split_line)

	f2.close()

	print "Gold Standard Split File \n" + str(split_file1) + '\n'
	print "System Annotated Split File \n" + str(split_file2) + '\n'

	for line1 in split_file2:
		temp_pos = true_pos
		for line2 in split_file1:
			if line1 == line2:
				true_pos += 1
				break
			else:
				continue
		if (temp_pos == true_pos):
			false_pos += 1

	false_neg = gs_count - true_pos

	total_true_pos += true_pos
	total_false_pos += false_pos
	total_false_neg += false_neg

	try:
		precision = Fraction(true_pos , (true_pos + false_pos))
	except ZeroDivisionError, e:
		print "Precision divide by 0, setting precision to 1"
		precision = 1.0

	try:
		recall = Fraction(true_pos , abs(true_pos + false_neg))
	except ZeroDivisionError, e:
		print "Recall divide by 0, setting recall to 1"
		recall = 1.0

	try:
		fscore = abs(2 * ((precision * recall) / (precision + recall)))
	except ZeroDivisionError, e:
		print "F-score divide by 0, setting fscore to 1"
		fscore = 1.0

	print "Gold Standard count:" + str(gs_count) + " True Positives:" + str(true_pos) + " False Positives:" + str(false_pos) + " False Negatives:" + str(false_neg)
	print "Precision:" + str(precision) + " recall:" + str(recall) + " fscore:" + str(fscore)

	print '\n'
	return precision,recall,fscore

#Get and assign file lists, type to evaluate
fileList1, fileList2, evalType = getPaths()
total_true_pos = 0
total_false_pos = 0
total_false_neg = 0

print "fileList1: " + str(fileList1) + '\n'
print "fileList2: " + str(fileList2) + '\n'
print "evalType: " + str(evalType)


#Create output file
path = os.getcwd()
results = open(path + '/evalResults.txt', 'w')
print "Results file at: " + path + '/evalResults.txt\n'

#Iterate through each set of files
for x in range(1, len(fileList1) + 1):
	print "Evaluating file set " + str(x)
	p, r, f = evalSet(fileList1[x - 1], fileList2[x - 1], evalType.lower())
	results.write("Evaluating test file: " + str(fileList2[x-1]) + " against gold standard file" + str(fileList1[x-1]) + '\n')
	results.write("Precision:" + str(p) + " Recall:" + str(r) + " F-score:" + str(f) + '\n')
	results.write('\n')

results.write("Total true_pos:" + str(total_true_pos) + " Total false_pos:" + str(total_false_pos) + " Total false_neg:" + str(total_false_neg) + '\n')

avg_precision = Fraction(total_true_pos , (total_true_pos + total_false_pos))
avg_recall = Fraction(total_true_pos , abs(total_true_pos + total_false_neg))
avg_fscore = abs(2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall)))

results.write("Average Precision:" + str(avg_precision) + " Average Recall:" + str(avg_recall) + " Average fscore:" + str(avg_fscore))

results.close()


