#!/usr/bin/env python

import sys
import urllib2
import subprocess
import re
import time
import os
import hashlib
import random

#=================================================
# MAIN FUNCTION
#=================================================

def main():
    # depenency check
    if not all([os.path.exists('phantomjs'), os.path.exists('/usr/bin/curl')]):
        print '[!] PhantomJS and cURL required.'
        return
    # parse options
    import argparse
    usage = """

PeepingTom - Tim Tomes (@LaNMaSteR53) (www.lanmaster53.com)

Dependencies:
 - PhantomJS
 - cURL

$ python ./%(prog)s <mode> <path>"""
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-l', help='list input mode. path to list file.', dest='list_file', action='store')
    parser.add_argument('-x', help='xml input mode. path to Nessus/Nmap XML file.', dest='xml_file', action='store')
    parser.add_argument('-s', help='single input mode. path to target, remote URL or local path.', dest='target', action='store')
    parser.add_argument('-o', help='output directory', dest='output', action='store')
    parser.add_argument('-t', help='socket timeout in seconds. default is 8 seconds.', dest='timeout', type=int, action='store')
    parser.add_argument('-v', help='verbose mode', dest='verbose', action='store_true', default=False)
    parser.add_argument('-b', help='open results in browser', dest='browser', action='store_true', default=False)
    opts = parser.parse_args()

    # process options
    # input source
    if opts.list_file:
        try:
            targets = open(opts.list_file).read().split()
        except IOError:
            print '[!] Invalid path to list file: \'%s\'' % opts.list_file
            return
    elif opts.xml_file:
        # optimized portion of Peeper (https://github.com/invisiblethreat/peeper) by Scott Walsh (@blacktip)
        import xml.etree.ElementTree as ET
        try: tree = ET.parse(opts.xml_file)
        except IOError:
            print '[!] Invalid path to XML file: \'%s\'' % opts.xml_file
            return
        except ET.ParseError:
            print '[!] Not a valid XML file: \'%s\'' % opts.xml_file
            return
        root = tree.getroot()
        if root.tag.lower() == 'nmaprun':
            # parse nmap file
            targets = parseNmap(root)
        elif root.tag.lower() == 'nessusclientdata_v2':
            # parse nessus file
            targets = parseNessus(root)
        print '[*] Parsed targets:'
        for x in targets: print x
    elif opts.target:
        targets = [opts.target]
    else:
        print '[!] Input mode required.'
        return
    # storage location
    if opts.output:
        directory = opts.output
        if os.path.isdir(directory):
            print '[!] Output directory already exists: \'%s\'' % directory
            return
    else:
        random.seed()
        directory = time.strftime('%y%m%d_%H%M%S', time.localtime()) + '_%04d' % random.randint(1, 10000)
    # connection timeout
    timeout = opts.timeout if opts.timeout else 8

    print '[*] Analyzing %d targets.' % (len(targets))
    print '[*] Storing data in \'%s/\'' % (directory)
    os.mkdir(directory)
    report = 'autopeeper.html'
    outfile = '%s/%s' % (directory, report)

    # logic to gather screenshots and headers for the given targets
    db = {'targets': []}
    cnt = 0
    tot = len(targets) * 2
    previouslen = 0
    try:
        for target in targets:
            # Displays the target name to the right of the progress bar
            if opts.verbose:
                printProgress(cnt, tot, target, previouslen)
            else:
                printProgress(cnt, tot)
            imgname = '%s.png' % re.sub('\W','',target)
            srcname = '%s.txt' % re.sub('\W','',target)
            imgpath = '%s/%s' % (directory, imgname)
            srcpath = '%s/%s' % (directory, srcname)
            getCapture(target, imgpath, timeout)
            cnt += 1
            previouslen = len(target)
            target_data = {}
            target_data['url'] = target
            target_data['imgpath'] = imgname
            target_data['srcpath'] = srcname
            target_data['hash'] = hashlib.md5(open(imgpath).read()).hexdigest() if os.path.exists(imgpath) else 'z'*32
            target_data['headers'] = getHeaders(target, srcpath, timeout)
            db['targets'].append(target_data)
            cnt += 1
        print printProgress(1,1)
    except Exception as e:
        print '[!] %s' % (e.__str__())
    
    # build the report and exit
    buildReport(db, outfile)
    if opts.browser:
        import webbrowser
        path = os.getcwd()
        w = webbrowser.get()
        w.open('file://%s/%s/%s' % (path, directory, report))
    print '[*] Done.'

#=================================================
# SUPPORT FUNCTIONS
#=================================================

def parseNmap(root):
    http_ports = [80,8000,8080,8081,8082,9090]
    https_ports = [443,8443]
    targets = []
    # iterate through all host nodes
    for host in root.iter('host'):
        hostname = host.find('address').get('addr')
        # hostname node doesn't always exist. when it does, overwrite address previously assigned to hostanme
        hostname_node = host.find('hostnames').find('hostname')
        if hostname_node is not None: hostname = hostname_node.get('name')
        # iterate through all port nodes reported for the current host
        for item in host.iter('port'):
            state = item.find('state').get('state')
            if state.lower() == 'open':
                #service_node = item.find('service')
                # service node doesn't always exist when a port is open. assume not http if no service is found
                #if service_node is not None:
                #service = service_node.get('name')
                service = item.find('service').get('name')
                port = item.get('portid')
                #print '%s%s' % (port.ljust(10), service)
                if 'http' in service.lower() or int(port) in (http_ports + https_ports):
                    proto = 'http'
                    if 'https' in service.lower() or int(port) in https_ports:
                        proto = 'https'
                    url = '%s://%s:%s' % (proto, hostname, port)
                    if not url in targets:
                        targets.append(url)
    return targets

def parseNessus(root):
    targets = []
    for host in root.iter('ReportHost'):
        name = host.get('name')
        for item in host.iter('ReportItem'):
            svc = item.get('svc_name')
            plugname = item.get('pluginName')
            if (svc in ['www','http?','https?'] and plugname.lower().startswith('service detection')):
                port = item.get('port')
                output = item.find('plugin_output').text.strip()
                proto = guessProto(output)
                url = '%s://%s:%s' % (proto, name, port)
                if not url in targets:
                    targets.append(url)
    return targets

def guessProto(output):
    # optimized portion of Peeper (https://github.com/invisiblethreat/peeper) by Scott Walsh (@blacktip)
    secure = re.search('TLS|SSL', output)
    if secure:
        return "https"
    return "http"

def getCapture(url, imgpath, timeout):
    cmd = 'phantomjs --ignore-ssl-errors=yes ./capture.js %s %s %d' % (url, imgpath, timeout*1000)
    returncode, response = runCommand(cmd)
    return returncode

def getHeaders(url, srcpath, timeout):
    #cmd = 'curl -sILk %s --connect-timeout %d' % (url, timeout)
    cmd = 'curl -sLkD - %s -o %s --max-time %d' % (url, srcpath, timeout)
    returncode, response = runCommand(cmd)
    return response

def runCommand(cmd):
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = proc.communicate()
    response = ''
    if stdout: response += str(stdout)
    if stderr: response += str(stderr)
    return proc.returncode, response.strip()

def printProgress(cnt, tot, target='', previouslen=0):
    percent = 100 * float(cnt) / float(tot)
    if target and previouslen > len(target): 
        target = target + ' ' * (previouslen - len(target))
    sys.stdout.write('[%-40s] %d%%   %s\r' % ('='*int(float(percent)/100*40), percent, target))
    sys.stdout.flush()
    return ''

def buildReport(db, outfile):
    live_markup = ''
    error_markup = ''
    dead_markup = ''
    # process markup for live targets
    for live in sorted(db['targets'], key=lambda k: k['hash']):
        live_markup += "<tr><td class='img'><a href='{0}' target='_blank'><img src='{0}' onerror=\"this.parentNode.parentNode.innerHTML='No image available.';\" /></a></td><td class='head'><a href='{1}' target='_blank'>{1}</a> (<a href='{2}' target='_blank'>source</a>)<br /><pre>{3}</pre></td></tr>\n".format(live['imgpath'],live['url'],live['srcpath'],live['headers'])
    # add markup to the report
    file = open(outfile, 'w')
    file.write("""
<!doctype html>
<head>
<style>
table, td, th {border: 1px solid black;border-collapse: collapse;padding: 5px;font-size: .9em;font-family: tahoma;}
table {width: 100%%;table-layout: fixed;min-width: 1000px;}
td.img {width: 40%%;}
img {width: 100%%;}
td.head {vertical-align: top;word-wrap: break-word;}
</style>
</head>
<body>
<table>
%s
</table>
</body>
</html>""" % (live_markup))
    file.close()

#=================================================
# START
#=================================================

if __name__ == "__main__": main()
