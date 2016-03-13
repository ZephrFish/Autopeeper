# Autopeeper v0.2
# Automated Web Application Screenshotter
# ZephrFish 2016
import sys
from sys import argv
import os
import subprocess
import argparse

# Define basic variables
#usage = """

# Check if user has supplied flags
if len(sys.argv) != 2:
  print """ Usage: python autopeeper.py [-h] [-f FILE] [-d] [-v VERBOSE] [-o OUTPUT DIRECTORY]
		
	optional arguments: 
		-h, --help show this help message and exit 
		-f FILE targets file, file containing target urls 
		-d debugging mode, turns on debugging 
		-v VERBOSE verbose mode 
		-o OUTPUT DIRECTORY output directory
		"""
  print
  sys.exit()

# Usage Information
parser = argparse.ArgumentParser()
parser.add_argument('-f', help='targets file, file containing target urls', dest='file', action='store')
parser.add_argument('-d', help='debugging mode, turns on debugging', dest='debugging', action='store_true')
parser.add_argument('-v', help='verbose mode', dest='verbose', action='store')
parser.add_argument('-o', help='output directory', dest='output directory', action='store')

opts = parser.parse_args()

script, options, file = argv

# Start to parse out target urls

if opts.file:
	try:
	     targets = open(opts.file).read().split()
	except IOError:
	     print '[!] Invalid File, or incorrect path to %r ' % opts.file


# Scanning Function, web, rpc, vnc and more
def scanning():
	web = [80,443,8080,8000,9000,8081,8082,9090,8000]
	rpcd = [3389]
	vnc = [5900]
	others = []



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
