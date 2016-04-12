# Autopeeper v0.24
# @ZephrFish
# Still a work in progress
#
#
#
#

import argparse
import subprocess
import os
import sys

# Global Variables
infile = ''
outdir = ''

# Autopeeper Logo Echo
print('''
                _                                                 ___   ___  _  _
     /\        | |                                               / _ \ |__ \| || |
    /  \  _   _| |_ ___  _ __   ___  ___ _ __   ___ _ __  __   _| | | |   ) | || |_
   / /\ \| | | | __/ _ \| '_ \ / _ \/ _ \ '_ \ / _ \ '__| \ \ / / | | |  / /|__   _|
  / ____ \ |_| | || (_) | |_) |  __/  __/ |_) |  __/ |     \ V /| |_| | / /_   | |
 /_/    \_\__,_|\__\___/| .__/ \___|\___| .__/ \___|_|      \_/  \___(_)____|  |_|
                        | |             | |
                        |_|             |_|
@ZephrFish v0.24

''')
def whereiscutycapt(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def initialize():
    if whereiscutycapt(cutycapt)==False:
        verbose('[+] Setting up dependencies')
        os.system('sudo apt-get install subversion libqt4-webkit libqt4-dev g++')
        os.system('svn co svn://svn.code.sf.net/p/cutycapt/code/ cutycapt')
        os.system('cd cutycapt/CutyCapt')
        os.system('qmake')
        os.system('make')
        verbose('[!] Initialised...')
    else:
        print('[!] initialized...')

# Single Target Mode
def singleURL():
    url = input("Enter URL>")
    single=[]
    portList = [80,443,5800,8080,9090,10000]
    for port in portList:
        verbose('[+] hosts running on port %r' % str(port))
        verbose('https://' + url + ':'+ str(port))
        verbose('http://' + url + ':' + str(port))
        single.append('https://' + url + ':'+ str(port))
        single.append('http://' + url + ':' + str(port))
        verbose(single)
    for target in single:
        os.system('cutycapt --url=%r --out=%r/test_single.png --delay=100' % (target, outdir))

# File Mode
def file():
    targets = open(infile, 'r').readlines()
    domains=[]
    for domain in targets:
         portList = [80,443,5800,8080,9090,10000]
         for port in portList:
             verbose('Target Port %r' % str(port))
             verbose('https://' + str(domain) + ':'+ str(port))
             verbose('http://' + str(domain) + ':'+ str(port))
             domains.append('https://' + str(domain) + ':'+ str(port))
             domains.append('http://' + str(domain) + ':' + str(port))
             verbose(domains)
    for target in domains:
        os.system('cutycapt --url=%r --out=%r/test_single.png --delay=100' % (target, outdir))

# Verbose Mode
def verbose(v):
    if args.verbose:
        print(v)

def main():
    # Check Dependencies
    initialize()

    # Single URL Mode
    if args.url:
        verbose('[!] Single URL Mode Enabled')
        singleURL()
    # File Mode
    elif args.infile:
        verbose('[!] Batch Mode Enabled')
        file()
    else:
        print('[!] No Flags Given')
        print('[!] Quitting...')
        quit()

# Argument Parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Domain Lister',
        prog="lister.py",
        usage='%(prog)s [options]'
    )
    # Required Parameters
    parser.add_argument("infile", help='targets file to scan & screenshot')
    parser.add_argument("outdir",help='output directory for results')


    # Debug & Verbose Mode
    parser.add_argument('--verbose', action='store_true', help='turn on verbose mode')
    parser.add_argument('--debug', action='store_true', help='turn on debug')
    parser.add_argument('--url', action='store_true', help='Single URL Mode')
    args = parser.parse_args()


main()



