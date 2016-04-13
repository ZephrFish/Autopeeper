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
def screener():
    portList = [80,443,5800,8080,9090,10000]
    domains=[]
    if args.url:
        targets = url.args
    else:
        targets = open(infile, 'r').readlines()
    for port in portList:
        for target in targets:
            verbose('[+] hosts running on port %r' % str(port))
            domains.append('https://' + str(target) + ':'+ str(port))
            domains.append('http://' + str(target) + ':' + str(port))
    for domain in domains:
        os.system('cutycapt --url=%r --out=%r --delay=100' % (domain, outdir))

# Verbose Mode
def verbose(v):
    if args.verbose:
        print(v)

def main():
    # Check Dependencies
    initialize()
    screener()
    if args.null:
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
