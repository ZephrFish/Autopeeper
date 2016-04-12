# Autopeeper v0.22
# ZephrFish


url = input('URL>')

# Verbose Mode
def verbose(v):
    print(v)

# Single URL Mode
def single():
    if 'https' in url:
        verbose(url + str(':443'))
    elif 'http' in url:
        verbose(url + str(":80"))
    else:
        verbose('https://' + url + str(':443'))
        verbose('http://' + url + str(':80'))

# Iterate through ports
def ports():
    portList = [80,443,5800,8080,9090,10000]
    for port in portList:
        if port == str(443):
            print('https://' + url + str(':443'))
        else:
            print('http://' + url + ':' + str(port))

# Screenshot Function
#def screenshot():
    # Marker

# Where all the magic happens
#def main():
# web only
#    single()
# Single Mode
#    single()
# File Mode

# all

# vnc

if __name__ == "__main__":
    ports()
