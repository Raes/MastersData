from __future__ import division
from fractions import *

'''
This script is for calculating Precision, Recall and F-measure. It will ask you for three integers and then
output PRF.

v1.0 - single set only

Created by: Sean Holloway 21-05-2015
'''

def main():
	gs_count = int(raw_input("Please enter gold standard count\n:"))
	true_pos = int(raw_input("Please enter true positive count\n:"))
	false_pos = int(raw_input("Please enter false positive count\n:"))

	false_neg = gs_count - true_pos

	try:
		precision = Fraction(true_pos , (true_pos + false_pos))
	except ZeroDivisionError, e:
		print "Precision divide by 0, setting precision to 1.0"
		print('\n')
		precision = 1.0

	try:
		recall = Fraction(true_pos , abs(true_pos + false_neg))
	except ZeroDivisionError, e:
		print "Recall divide by 0, setting recall to 1.0"
		print('\n')
		recall = 1.0

	try:
		fscore = abs(2 * ((precision * recall) / (precision + recall)))
	except ZeroDivisionError, e:
		print "F-score divide by 0, setting fscore to 1.0"
		print('\n')
		fscore = 1.0

	print ('-------')
	print "Precision:" + str(precision) + " recall:" + str(recall) + " fscore:" + str(fscore)
	print ('-------')

if __name__ == "__main__":
    main()