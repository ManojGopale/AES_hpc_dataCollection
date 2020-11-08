#!/usr/bin/python2.7
import datetime;
import multiprocessing
import subprocess
import shutil
import os
import re
import sys
import random
import copy
import time
from optparse import OptionParser

## Removing contents of dirPath folder for new run
def removeDir(dirPath):
    try: 
        shutil.rmtree(dirPath)
        print"\nSuccessfull Removed folder\n%s\n" %(dirPath)
    except OSError as e:
        ## python2.7 syntax
        print "rmtree Error: %s - %s." % (e.filename, e.strerror)

## Create directory tree for dirPath
def createDir(dirPath):
    try:
        #M os.makedirs() Creates sub directory paths even if they do not exist
        os.makedirs(dirPath)
        print "Successfully Created new folder\n%s\n" %(dirPath)
    except OSError as e:
        ## python2.7 syntax
        print "MakeDir Error: %s - %s." % (e.filename, e.strerror)


parser = OptionParser()
parser.add_option('-f','--fileName', 
                  action = 'store', type='string', dest='fileName', default = 'normal')

(options, args) = parser.parse_args()

fcurr = options.fileName + "/"

## Number of power traces to generate
##num = 10000
num = 500

##mainDir -> where main.c is located
mainDir = "/manojwork/work/complete_cross/"

## runDir -> where all the main[0-255].c will be saved for further use
runDir = "/xdisk/manojgopale/AES/dataCollection/runDir/" + fcurr
createDir(runDir)

fin = open(mainDir + 'main.c','r') ## open /home/complete/cross/main.c
lines_old = fin.readlines() ## Populate lines_old with lines of main.c
fin.close() ## Close the file
curr_max = 0
last_line = 0
first_line = 0
check = re.compile(r'm5_checkpoint\(0,0\);')
repeat = re.compile(r'[\t\s]+POM_ENC\((\d+)\);[\r\n]')
key = re.compile(r'([\t\s]+key\[0\] = )\d+(;[\r\n])')
go_unroll = re.compile(r'(./unroll_loop.py )main\d*.c')
key_line = 0
new_keyline = ''
warm_up = 0

## removes the key_runs directory and its substructure
#Mshutil.rmtree(runDir + 'key_runs',ignore_errors = True)
#Mos.makedirs(runDir + 'key_runs') ## Creates 'key_runs' directory where main[0-255].c is stored
mainFilesDir = runDir + "mainFiles/"
removeDir(mainFilesDir)
createDir(mainFilesDir)

enc_list = []
## num = =10000
## Creates a list of num lines with each line having 16 random hexa numbers as input to the POM_ENC
for i in range(0, num):
    byte_array = []
    for byte in range(16):
        byte_array.append(hex(random.SystemRandom().randint(0, 2**8-1)))
    input_str = ','.join(byte_array)
    enc_list.append('\tPOM_ENC('+input_str+');\n')
##Creates a list with 
## '\tPOM_ENC(0x37,0x0,0x9c,0xd,0x9c,0x22,0x92,0xe4,0x53,0x20,0x2d,0x8,0x4a,0x0,0x80,0xcc);\n


warm_list = []
for i in range(0, warm_up):
    byte_array = []
    for byte in range(16):
        byte_array.append(hex(random.SystemRandom().randint(0, 2**8-1)))
    input_str = ','.join(byte_array)
    warm_list.append('\tPOM_ENC('+input_str+');\n')

    
    
#for k in range(0,256):
def main_one(k):
    print "Generating " + str(k)
    curr_max = 0
    last_line = 0
    first_line = 0
    lines = copy.deepcopy(lines_old) ## List of lines in main.c
    for line in lines:        
        ## repeat = re.compile(r'[\t\s]+POM_ENC\((\d+)\);[\r\n]')
        ## looking for POM_ENC in main.c file
        match_repeat = repeat.search(line)
        if match_repeat != None: ## if matched
            num_literal = int(match_repeat.group(1)) ## Get the number inside the paranthesis of POM_ENC()
            if first_line == 0:
                    first_line = lines.index(line) ## Get the index or line number of the match
            if num_literal > curr_max:
                curr_max = num_literal;
            last_line = lines.index(line);
        ## key = re.compile(r'([\t\s]+key\[0\] = )\d+(;[\r\n])')
        ## key[0] = 50 pattern in main.c
        match_key = key.search(line)
        if match_key != None: ## If matched, go in this loop
            key_line = lines.index(line)
            new_keyline = match_key.group(1) + str(k) + match_key.group(2)

#        print match_repeat
#        print match_key
#    print lines[check_line]
    new_enc_list = []
    new_enc_list.extend(enc_list) ##Add the 10,000 lines of POM_ENC() to the file   
    
    # Update lines in reverse order
    lines[last_line+1:last_line+1] = new_enc_list
#    lines[check_line+1:check_line+1] = new_warm_list    
    lines[key_line] = new_keyline
    del lines[first_line:last_line+1]
    return lines ##M lines contain the full changes that have to be made in the main.c



##M line_in comes from main_one() which makes POM_ENC, and key[0] changes to file
def main_two(k, line_in):
#    print "Generating " + str(k)
    check_line = 0
    lines = copy.deepcopy(line_in)
    for line in lines:        
        match_checkpoint = check.search(line) ##M matches m5_checkpoint(0,0) line
        if match_checkpoint:
            check_line = lines.index(line)
#
    new_warm_list = []
    new_warm_list.extend(warm_list)
    new_warm_list.append(lines[check_line])
#    warm_list.append(lines[check_line])
#    print new_warm_list
    
    
    lines[check_line+1:check_line+1] = new_warm_list    
    del lines[check_line]
    fout = open(mainFilesDir + 'main'+str(k)+'.c','w')
    fout.writelines([l.replace('\r','') for l in lines])
    fout.close()
    print 'Finishing ' + str(k)
    

#jobs = []
#for k in range(256):
#    p = multiprocessing.Process(target=main_one, args=(k,))
#    jobs.append(p)
#    p.start()

#for j in jobs:
#    j.join()

for k in range(256):
    main_two(k,main_one(k))
