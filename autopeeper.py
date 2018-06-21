# Autopeeper v0.01
# @ZephrFish
# Still a work in progress
# Define Libraties and Modules to import
import argparse
import subprocess
import os
import sys

# Global Variables
infile = ''
outdir = ''


# Look for cutycapt binary on system
def whereiscutycapt(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True
    
# If not installed, install cutycapt and set it up
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

# Single & File Mode
def file():
  if args.url:
    targets = args.url
  elif args.infile:
    targets = open(args.infile, 'r').readlines()
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
        cmd = 'cutycapt --url={0} --out={1}/{0}.png --delay=100'.format(target, args.outdir)
        os.system(cmd)

# Verbose Mode
def verbose(v):
    if args.verbose:
        print(v)

# Main function body
def main():
    # Check Dependencies
    initialize()

    # Single URL Mode
    if args.url:
        verbose('[!] Single URL Mode Enabled')
        #singleURL() Doesn't exists
        file()
    # File Mode
    elif args.infile:
        verbose('[!] Batch Mode Enabled')
        file()
    else:
        print(args.help)
        quit()

# Argument Parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Domain Lister',
        prog="lister.py",
        usage='%(prog)s [options]'
    )
    # Parameters
    need = parser.add_mutually_exclusive_group()
    need.add_argument('-f', '--file', dest='infile', help='targets file to scan & screenshot')
    need.add_argument('-u', '--url', dest='url', action='store_true', help='Single URL Mode')
    parser.add_argument('-o', '--outdir', dest='outdir', help='output directory for results')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='turn on verbose mode')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='turn on debug')
    args = parser.parse_args()


main()



