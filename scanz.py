#Radiant python network scanner

print("""



   SSSSSSSSSSSSSSS              CCCCCCCCCCCCC                    AAA                    NNNNNNNN        NNNNNNNN     ZZZZZZZZZZZZZZZZZZZ
 SS:::::::::::::::S          CCC::::::::::::C                   A:::A                   N:::::::N       N::::::N     Z:::::::::::::::::Z
S:::::SSSSSS::::::S        CC:::::::::::::::C                  A:::::A                  N::::::::N      N::::::N     Z:::::::::::::::::Z
S:::::S     SSSSSSS       C:::::CCCCCCCC::::C                 A:::::::A                 N:::::::::N     N::::::N     Z:::ZZZZZZZZ:::::Z
S:::::S                  C:::::C       CCCCCC                A:::::::::A                N::::::::::N    N::::::N     ZZZZZ     Z:::::Z
S:::::S                 C:::::C                             A:::::A:::::A               N:::::::::::N   N::::::N             Z:::::Z
 S::::SSSS              C:::::C                            A:::::A A:::::A              N:::::::N::::N  N::::::N            Z:::::Z
  SS::::::SSSSS         C:::::C                           A:::::A   A:::::A             N::::::N N::::N N::::::N           Z:::::Z
    SSS::::::::SS       C:::::C                          A:::::A     A:::::A            N::::::N  N::::N:::::::N          Z:::::Z
       SSSSSS::::S      C:::::C                         A:::::AAAAAAAAA:::::A           N::::::N   N:::::::::::N         Z:::::Z
            S:::::S     C:::::C                        A:::::::::::::::::::::A          N::::::N    N::::::::::N        Z:::::Z
            S:::::S      C:::::C       CCCCCC         A:::::AAAAAAAAAAAAA:::::A         N::::::N     N:::::::::N     ZZZ:::::Z     ZZZZZ
SSSSSSS     S:::::S       C:::::CCCCCCCC::::C        A:::::A             A:::::A        N::::::N      N::::::::N     Z::::::ZZZZZZZZ:::Z
S::::::SSSSSS:::::S        CC:::::::::::::::C       A:::::A               A:::::A       N::::::N       N:::::::N     Z:::::::::::::::::Z
S:::::::::::::::SS           CCC::::::::::::C      A:::::A                 A:::::A      N::::::N        N::::::N     Z:::::::::::::::::Z
 SSSSSSSSSSSSSSS                CCCCCCCCCCCCC     AAAAAAA                   AAAAAAA     NNNNNNNN         NNNNNNN     ZZZZZZZZZZZZZZZZZZZ


""")

#imports

import argparse
import sys
from netifaces import interfaces, ifaddresses
import threading
from scapy.layers.l2 import arping
import time
import os
from itertools import product

#function declaration

def getIpFromInterface(iface):
    #check if interface exists
    if iface in interfaces():
        #check if can get an ip from the interface
        try:
            return ifaddresses(iface)[2][0]["addr"]
        except:
            return "err2"
    else:
        return "err1"

def arpinger(ipArg):
    #scans the ip, if there is an error, it means that the host isnt active, so it doesnt add it to the activeHosts list
    try:
        var = arping(ipArg, timeout=args.timeout, verbose=0)[0][0]
        activeHosts.append(ipArg)
    except IndexError:
        pass

def displayPercentage():
    while True:
        if (len(threading.enumerate()) - 2 == 0):
            print("[+] Done")
            break
        print("[+] Scanned " + str(len(threading.enumerate()) - 2)  + " hosts out of " + str(256 ** int(args.subnetting)))
        time.sleep(5)

#argument parsing
parser = argparse.ArgumentParser(description='')
parser.add_argument("--subnetting", metavar="level", type=int, help="how many octet's scan from the base ip, defaults to 1", default=1)
parser.add_argument("--timeout", metavar="seconds", type=int, help="scan timeout, defaults to one second", default=1)
parser.add_argument("--output", metavar="file_name", type=str, help="the file name output, doesnt save if isnt specified", default=None)
parser.add_argument("interface", metavar="interface_name", type=str, help="specify wich interface to get the ip from")
#display help and exit script if no arguments are parsed
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(2)
elif os.geteuid() != 0:
    print("[-] Error: You need to run the script as root")
args = parser.parse_args()

#ip template generation
ip = getIpFromInterface(args.interface)
#error checking on function
if ip == "err1":
        print("ERROR[-] The interface selected doesnt exists!")
        sys.exit(2)
elif ip == "err2":
        print("ERROR[-] The interface selected isnt valid!")
        sys.exit(2)
#generate ip template knowing when does an octet ends counting the dots
ipTemplate = ""
dotCounter = 0
dotCount = 4 - args.subnetting
#validate subnet argument
if dotCount >= 4:
    ipTemplate = ""
else:
    for x in ip:
        if x == ".":
            dotCounter += 1
        ipTemplate += x
        if dotCounter == dotCount:
            break


#scanning
activeHosts = [] #place where the scanner stores the active hosts
if args.subnetting == 1:
    for x in range(256):
        ip = str(ipTemplate + str(x))
        thr = threading.Thread(target=arpinger, args=(ip,))
        thr.start()
elif args.subnetting == 2:
    for x, y in product([*range(256)], repeat=2):
        ip = str(ipTemplate + str(x) + "." + str(y))
        thr = threading.Thread(target=arpinger, args=(ip,))
        thr.start()
elif args.subnetting == 2:
    for x, y, z in product([*range(256)], repeat=3):
        ip = str(ipTemplate + str(x) + "." + str(y) + "." + str(z))
        thr = threading.Thread(target=arpinger, args=(ip,))
        thr.start()
elif args.subnetting == 2:
    for x, y, z, a in product([*range(256)], repeat=4):
        ip = str(ipTemplate + str(x) + "." + str(y) + "." + str(z) + "." + str(a))
        thr = threading.Thread(target=arpinger, args=(ip,))
        thr.start()

while len(threading.enumerate()) > 1:
    continue

output = ""
for x in activeHosts:
    output += x + "\n"

print(output)

if args.output != None:
    toWrite = open(args.output, "w")
    toWrite.write(output)
    toWrite.close()
