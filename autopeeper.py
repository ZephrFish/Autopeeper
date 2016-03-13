# Autopeeper v1.0
# Automated Web Application Screenshotter
# ZephrFish 2016
from sys import argv
import argparse

# Define basic variables
#usage = """

# Usage Information
parser = argparse.ArgumentParser()
parser.add_argument('-f', help='targets file, file containing target urls', dest='file', action='store')
parser.add_argument('-d', help='debugging mode, turns on debugging', dest='debugging', action='store_true')
parser.add_argument('-v', help='verbose mode', dest='verbose', action='store')
parser.add_argument('-o', help='output directory', dest='output directory', action='store')

opts = parser.parse_args()

# Required arguments for file
script, file = argv

# Start to parse out target urls

if opts.file:
	try:
	     targets = open(opts.file).read().split()
	except IOError:
	     print '[!!] Invalid File, or incorrect path to %r ' % opts.file


# Set Targets as file provided to script
targets = open(file)
num_lines = sum(1 for line in open(file))

# Debugging step, prints out the hosts from file
def debugging():
	print "The output from %r is shown: " % file	
	print targets.read()
	print "There are a total of %r targets in the file provided " % num_lines



# Run Main Code
# Uncomment line below to run debugging
#debugging()
