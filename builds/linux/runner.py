import sys
import os
args = sys.argv[1:]
out = ""
for x in args:
	out += x + ""
os.system("sudo build/scanz_env/bin/python3 build/scanz.py " + out)
