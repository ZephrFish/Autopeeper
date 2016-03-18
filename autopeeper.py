# Autopeeper v0.21
# Working Copy
# Automated Web Application Screenshotter
# ZephrFish 2016
import sys
import os
import subprocess
import argparse
import commands
from argparse
import ArgumentParser

# File & Output Path
file = None
outdir = None

# Autopeeper Logo Echo
print('''
                _                                                 ___   ___  
     /\        | |                                               / _ \ |__ \ 
    /  \  _   _| |_ ___  _ __   ___  ___ _ __   ___ _ __  __   _| | | |   ) |
   / /\ \| | | | __/ _ \| '_ \ / _ \/ _ \ '_ \ / _ \ '__| \ \ / / | | |  / / 
  / ____ \ |_| | || (_) | |_) |  __/  __/ |_) |  __/ |     \ V /| |_| | / /_ 
 /_/    \_\__,_|\__\___/| .__/ \___|\___| .__/ \___|_|      \_/  \___(_)____|
                        | |             | |                                  
  ______          _     |_|  ______ _   |_|                                  
 |___  /         | |        |  ____(_)   | |                                 
    / / ___ _ __ | |__  _ __| |__   _ ___| |__                               
   / / / _ \ '_ \| '_ \| '__|  __| | / __| '_ \                              
  / /_|  __/ |_) | | | | |  | |    | \__ \ | | |                             
 /_____\___| .__/|_| |_|_|  |_|    |_|___/_| |_|                             
           | |                                                               
           |_|                                                               
''')

# Defining Functions

# Debugging Function
def debugging():
		if args.debugging: 
			print('[+] Debugging [Enabled] Disabled');
			targets = open(file);
		num_lines = sum(1 for line in open(file));
        print "The output from %r is shown: " % file;
        print targets.read();
        print "There are a total of %r targets in the file provided " % num_lines;
		else:
			return print('[-] Debugging Enabled [Disabled]');

def verbose():
		if args.verbose:
			
			
			
# Main method, to check input parameters
if __name__ == "__main__":
   
        parser = ArgumentParser(description="Tool for Screenshotting Web Applications Automatically")

        
        parser.add_argument("file", help="File to check version of")
        parser.add_argument("outdir", help="Directory of local git repository")

        
        parser.add_argument("-v", "--verbose", action="store_true",help="verbose mode")
        parser.add_argument("-d", "--debugging", action="store_true", help='debugging mode, turns on debugging', dest='debugging')

        
        args = parser.parse_args()
		
		
		if os.path.isfile(args.file)==False:
			parser.print_help()
			print "[!] Targets File does not exist [!]"
			sys.exit(-1)
		
		# check that the directory exists
		#if os.path.isdir(args.outdir)==False:
		#	parser.print_help()
		#	print "[!] Output directory does not exist [!]"
		#	sys.exit(-1)
