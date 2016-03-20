# Autopeeper v0.21
# Working Copy
# Automated Web Application Screenshotter
# ZephrFish 2016
import sys
import os
import subprocess
import argparse
from argparse import ArgumentParser

# File & Output Path
file = None
outdir = None

# Autopeeper Logo Echo
print('''
                _                                                 ___   ___  __ 
     /\        | |                                               / _ \ |__ \/_ |
    /  \  _   _| |_ ___  _ __   ___  ___ _ __   ___ _ __  __   _| | | |   ) || |
   / /\ \| | | | __/ _ \| '_ \ / _ \/ _ \ '_ \ / _ \ '__| \ \ / / | | |  / / | |
  / ____ \ |_| | || (_) | |_) |  __/  __/ |_) |  __/ |     \ V /| |_| | / /_ | |
 /_/    \_\__,_|\__\___/| .__/ \___|\___| .__/ \___|_|      \_/  \___(_)____||_|
                        | |             | |                                     
          ______        |_|          ___|_| _     _                             
    ____ |___  /         | |        |  ____(_)   | |                            
   / __ \   / / ___ _ __ | |__  _ __| |__   _ ___| |__                          
  / / _` | / / / _ \ '_ \| '_ \| '__|  __| | / __| '_ \                         
 | | (_| |/ /_|  __/ |_) | | | | |  | |    | \__ \ | | |                        
  \ \__,_/_____\___| .__/|_| |_|_|  |_|    |_|___/_| |_|                        
   \____/          | |                                                          
                   |_|
    This is Still a work in progress - a learning project
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
			
			

def scanning():
	# Scanning Function

def capture():
	# Screenshotting Function

def checking():
	# Check output exists
	

# Main method, to check input parameters
if __name__ == "__main__":
   
        parser = ArgumentParser(description="Tool for Screenshotting Web Applications Automatically")

        # Requried Options
        parser.add_argument("file", help="File to check version of")
        parser.add_argument("outdir", help="Directory of local git repository")

        # Optional Optiosn
        parser.add_argument("-v", "--verbose", action="store_true",help="verbose mode")
        parser.add_argument("-d", "--debugging", action="store_true", help='debugging mode, turns on debugging', dest='debugging')
	parser.add_argument("-s", "--single", action="store_true",help="single url mode")
        args = parser.parse_args()
		
		# Check file exists
		# if os.path.isfile(args.file)==False:
		#	parser.print_help()
		#	print "[!] Targets File does not exist [!]"
		#	sys.exit(-1)
		
		# check that the directory exists
		#if os.path.isdir(args.outdir)==False:
		#	parser.print_help()
		#	print "[!] Output directory does not exist [!]"
		#	sys.exit(-1)
