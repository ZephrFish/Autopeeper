#!/bin/bash
# AutoPeeper with NMAP scan
#
# This Script Takes an input and output names then does an nmap scan and parses it out for http, https & unknown services
# Then screenshots it and gives output in browser, the additional tool call auto peeper with nmap will do an additional nmap scan to give the output
#echo "          _        ____
#     /\        | |      |  __ \
#    /  \  _   _| |_ ___ | |__) |__  ___ _ __   ___ _ __
#   / /\ \| | | | __/ _ \|  ___/ _ \/ _ \ '_ \ / _ \ '__|
#  / ____ \ |_| | || (_) | |  |  __/  __/ |_) |  __/ |
# /_/    \_\__,_|\__\___/|_|   \___|\___| .__/ \___|_|
#                                       | |
#          ______          _          __|_|_ _     _
#    ____ |___  /         | |        |  ____(_)   | |
#   / __ \   / / ___ _ __ | |__  _ __| |__   _ ___| |__
#  / / _` | / / / _ \ '_ \| '_ \| '__|  __| | / __| '_ \
# | | (_| |/ /_|  __/ |_) | | | | |  | |    | \__ \ | | |
#  \ \__,_/_____\___| .__/|_| |_|_|  |_|    |_|___/_| |_|
#   \____/          | |
#                   |_|    "

echo "Title: AutoPeeper_NMAP"
echo "Version: 0.1"
echo "Creator: @ZephrFish"

# Depenency check
	if ! which phantomjs > /dev/null ; then
	     echo '[!] PhantomJS and cURL required.'
	elif
	   ! which curl > /dev/null ; then
	     echo '[!] PhantomJS and cURL required.'
	else
	     echo 'Starting Script...'
	fi
echo
echo 'Getting NMAP Parameters'
echo
# Initial Nmap scan prompts for target host file name and desired output name
echo -n "Please enter the name of the target hosts file and press [ENTER]: "
read hosts
echo -n "Please enter the name for output file and press [ENTER]: "
read output_nmap

echo "Starting NMAP scan [PLEASE WAIT]"
# NMAP Banner grabbing

sudo nmap --script banner-plus.nse --min-rate=400 --min-parallelism=100 T3 -p- -n -Pn -PS -iL $hosts -vvv -oA $output_nmap

# Prompts for user input of  input file name and output name
echo -n "Please enter the file name you want for the  output file of peeper report and press [ENTER]: "
read output

echo
echo "Parsing out http, https & unknown services"
echo

# Cuts out http, https & unknown services
cat $output_nmap.gnmap | ./gnmap.pl | grep http | cut -f 1,2 -d "," | tr "," ":" > $output.http
cat $output_nmap.gnmap | ./gnmap.pl | grep https | cut -f 1,2 -d "," | tr "," ":" > $output.https
cat $output_nmap.gnmap | ./gnmap.pl | grep unknown | cut -f 1,2 -d "," | tr "," ":" > $output.unknown

echo
echo "Scanning output files for web apps & screenshotting them"
echo

# Inputs files to peepingtom.py
python ./peepingtom.py -l $output.http -v -b
python ./peepingtom.py -l $output.https -v -b
python ./peepingtom.py -l $output.unknown -v -b

# Future Work will be to integrate the peeping tom script to the main body code so that this is an all in one





