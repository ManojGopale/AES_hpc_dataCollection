#!/usr/bin/python2
import sys
import os
import re
from optparse import OptionParser

def convert(infilename, opts):
	#check file exists
	#exists
	if (os.path.isfile(infilename) == True):
		pass
	#not exists
	else:
		print "File not exists"
		sys.exit(1)
	#read line by line
	with open(infilename) as f:
		content = f.readlines()
	#foreach
	print opts.out
	#loop flag
	loopflag = 0
	loopcount = 0
	with open(opts.out, "w") as fo:
		for k in content:
			if loopflag ==1 :
				for i in range (0, loopcount):
					fo.write("/*" + str(i)+"*/" + k)	
				loopcount = 0
				loopflag = 0
				continue
			plist = re.findall("\s*//LU\s*(\d+)", k)
			if len(plist) > 0:
				loopcount = int(plist[0])
				loopflag = 1		
				fo.write("//Loop unrolled here: "+ plist[0] +" times")
				fo.write("\r\n")
				continue
			else:
				fo.write(k)	
	#regexpression to check comment

	#determine conversion next line

def main():
    global opts
    usage = "usage: %prog [options] <annotated C file>"
    parser = OptionParser(usage=usage)
    parser.add_option("-q", "--quiet",
        action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")
    parser.add_option("-o", "--out", type="string",
        action="store", dest="out", default="output.c",
        help="output C file (input to compiler)")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    print "* Starting conversion*"
    convert(args[0], opts)
    sys.exit(0)
if __name__ == '__main__':
	main()

