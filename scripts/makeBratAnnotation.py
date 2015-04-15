import sys
import sys, traceback
import elementtree.ElementTree as ET
import glob
from sys import argv
from os.path import basename
import os

'''
This script is for converting NER output files into Brat annotation format, 
or a format which can be evaluated against Brat annotation files.

This script is meant to be as verbose as necessary so following users can 
understand the process and change as necessary.

v1.1 - all .chem files in directory, chemspot and oscar3 support.

Created by: Sean Holloway 05-05-2015
Tested on: Mac OSX 10.9.5
'''

#Simple yes/no query function
def query_yes_no(question, default="yes"):
    "Recipe 577058"
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def chemspotFormatter(path):
    #Start iteration through .chem files
    fileList = glob.glob(path + "/*.chem")
    print str(len(fileList)) + " chemspot files found for processing"

    for file in fileList:

        print "Currently working on file: " + str(file)

        with open(file) as f:

            #create output file
            bratFormatFile = open(path + '/output/000' + str(fileList.index(f.name) + 1) + 'bratFormat' + '.ann' , 'w')
            #print "Creating output file: " + bratFormatFile.name

            #skip first line as this is a chemspot header
            next(f)

            #line number variable
            i = 1

            for line in f:
                #split by whitespace
                unformatedText = line.split()
                #print "Line split: " + str(unformatedText)

                #create line formatted for Brat, need to increment first span by 1 
                #and second span by 2 to match Brat span numbers

                formatedText = str(i) + " Compound" + " " + str(int(unformatedText[0]) + 1) + " " + str(int(unformatedText[1]) + 2) + " " + unformatedText[2]
                #print "Formatted line: " + str(formatedText)

                bratFormatFile.write(formatedText + '\n')
                i += 1

            bratFormatFile.close()
    f.close()

def oscar3Formatter(path):
    #Get file list
    fileList = glob.glob(path + "/*")
    print str(len(fileList)) + " oscar3 files found for processing"

    #Start and end are the two strings we want to find, and then extract the information between
    start = '<ne'
    end = '</ne>'

    #Iterate through files in file list
    for file in fileList:

        print "Currently working on file: " + str(file)

        #Open file for processing
        with open(file) as f:

            #Create output file
            evalFormatFile = open(path + '/output/000' + str(fileList.index(f.name)) + 'evalFormat' + '.txt' , 'w')

            tree = ET.parse(file)
            print tree
    return 0


def main():
    try:
        #Directory path resolution
        path = os.getcwd()
        print "Your directory path is: " + path

        if query_yes_no("Does this directory contain the unformated files? If not, you will be asked for the directory path"):
            print "Using current directory path."
        else:
            print "Please enter directory path of unformated files. If none present, an output directory will be created there."
            path = raw_input()
            print "New file path: " + path
    except Exception:
        print "Exception getting directory path"
        sys.exit(0)

    try:
        #Query what type of format is coming in
        fileFormat = str(raw_input("Please enter what type the original files are; chemspot, oscar3: "))
    except Exception:
        print "Exception with format type"
        sys.exit(0)

    try:
        #check for output directory, if not found, create it
        if not os.path.isdir(path + '/output'):
            os.makedirs(path + '/output')
            print 'Creating output directory ' + path + '/output'
    except Exception:
        print "Exception creating output directory"
        sys.exit(0)

    try:
        #Run proper format function based upon fileFormat
        if fileFormat == 'chemspot':
            print "Running chemspot to Brat formatter"
            chemspotFormatter(path)
        elif fileFormat == 'oscar3':
            print "Running oscar3 to Brat formatter"
            oscar3Formatter(path)
        else:
            print "Non-viable format type"
            sys.exit(0)
    except Exception:
        print "Exception in file format checker"
        traceback.print_exc()
        sys.exit(0)

if __name__ == "__main__":
    main()
