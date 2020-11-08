#!/usr/bin/python
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

parser = OptionParser()
parser.add_option('-t','--type', 
                  action = 'store', type='string', dest='run_type', default = 'normal')
parser.add_option('-c','--config', 
                  action = 'store', type='string', dest='config', default = 'default_cache')
parser.add_option('-r', '--runs',
                  action = 'store', type='int', dest='runs', default = 1)
parser.add_option('--cpuCount',
                  action = 'store', type='int', dest='cpuCount', default = 28)

(options, args) = parser.parse_args()

##M
runDir = "/xdisk/manojgopale/AES/dataCollection/runDir/"
qresultDir = "/xdisk/manojgopale/AES/dataCollection/q_result/"

##mainDir
mainDir = "/manojwork/work/complete_cross/"

##seconfigFolder -> Needs to be in /xdisk/ since we are writing to files in it
seconfigDir = runDir + "/seconfigFolder/"

## dir where go file is located
goDir = "/manojwork/work/"

num = 0
#if len(sys.argv) <= 1:
#    num = 1000
#else:
#    num = int(sys.argv[1])

## Changed num=10000 to 1000 for trace detection.
#num = 10000
num = 1000
fin = open(mainDir + 'main.c','r')
lines_old = fin.readlines()
fin.close()
curr_max = 0
last_line = 0
first_line = 0

##M Use --config to set the config
#config = ['normal']
#config = ['normal', 'default_cache', 'cache_associate8', '64kcache','64k_associate8' ,'l2default']
#config = ['64kcache']
#config = ['64k_associate8']
#config = ['l2default']
#config = ['default_cache']
#config = ['l24m_default', 'l24m_l1associate8', 'l2_l1associate8']
#config = ['dram_l2default']
#config = ['l24m_l1associate8'] #4.4
#config = ['dram_l2_l1associate8','dram_l24m_default','dram_l24m_l1associate8']

repeat = re.compile(r'\tPOM_ENC\((\d+)\);\r\n')
key = re.compile(r'(\tkey\[0\] = )\d+(;\r\n)')

#M Commented put because we no longer use unroll_loop.py in go files
#Mgo_unroll = re.compile(r'(./unroll_loop.py )main\d*.c')
key_line = 0
new_keyline = ''

##M Since we are not creating main[].c in this loop.
#Mshutil.rmtree(runDir + 'key_runs',ignore_errors = True)
#Mos.makedirs(runDir + 'key_runs')

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


## REading go files
fgo = open(goDir + 'go','r')
go_text = fgo.readlines();
fgo.close()

enc_list = []
for i in range(0, num):
    byte_array = []
    for byte in range(16):
        byte_array.append(hex(random.SystemRandom().randint(0, 2**8-1)))
    input_str = ','.join(byte_array)
    enc_list.append('\tPOM_ENC('+input_str+');\r\n')

    
out1 = re.compile(r'^\$gem5_se \w*')
out2 = re.compile(r'^\$gem5_se_all \w*')
out3 = re.compile(r'^\$gem5_se_no_trace \w*')
#Mif options.run_type == 'normal':
#M    compile_folder = '/xdisk/manojgopale/AES/dataCollection/compiled/' #M xdisk path
#M    createDir(compile_folder)
#Mif options.run_type == 'masked':
#M    compile_folder = '/xdisk/manojgopale/AES/dataCollection/compiled_masked/'
#M    createDir(compile_folder)

def process_one(k, fcurr):
    print "\nk=%s\tfcurr=%s\n" %(k, fcurr)

    runDir = "/xdisk/manojgopale/AES/dataCollection/runDir/"
    interDir = runDir + fcurr + "interOutput/"
    
    ##full.sh and its subfiles are kept in fullScriptDir folder in runDir
    fullDir = runDir + fcurr + "fullScriptDir/"
    
    ## go_curr files for each run
    goOutDir = runDir + fcurr + "goFiles/"
    
    # Compiled a[].outs are stored here
    compile_folder = runDir + fcurr + "/compiled/"

    for l in go_text:
        #Mmatch_go = go_unroll.search(l)
        match_out1 = out1.search(l)
        match_out2 = out2.search(l)
        match_out3 = out3.search(l)
        #Mif go_unroll.search(l) != None:
            #Mcurr_unroll = goDir + match_go.group(1) + runDir + '/key_runs/main'+str(k) +'.c\n'
            #Mgo_index = go_text.index(l)
            #Mgo_text[go_index] = curr_unroll
        if match_out1 != None:
            out1_index = go_text.index(l)
            #M This is for dynamic timing
            #curr_out1 = match_out1.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=timing  --restore-with-cpu=TimingSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out -r 1 --checkpoint-dir ' + interDir  +str(k) +'\n'
            curr_out1 = match_out1.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=atomic  --restore-with-cpu=AtomicSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out -r 1 --checkpoint-dir ' + interDir  +str(k) +'\n'
            go_text[out1_index] = curr_out1
        if match_out2 != None:
            #curr_out2 = match_out2.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=timing  --restore-with-cpu=TimingSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out -r 1 --checkpoint-dir ' + runDir  +str(k) +'\n'                
            curr_out2 = match_out2.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=atomic  --restore-with-cpu=AtomicSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out -r 1 --checkpoint-dir ' + interDir  +str(k) +'\n'                
            out2_index = go_text.index(l)
            go_text[out2_index] = curr_out2
        if match_out3 != None:
            #curr_out3 = match_out3.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=timing --restore-with-cpu=TimingSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out --checkpoint-dir ' + interDir  +str(k) +'\n'
            curr_out3 = match_out3.group(0) + '--outdir '+ interDir +str(k) +' /manojwork/gem5/configs/example/se.py $CACHE_OPTIONS -n 1 --cpu-type=atomic --restore-with-cpu=AtomicSimpleCPU -c '+compile_folder+'/a'+str(k)+'.out --checkpoint-dir ' + interDir  +str(k) +'\n'
            out3_index = go_text.index(l)
            go_text[out3_index] = curr_out3   
            
            
    go_curr = open(goOutDir + 'go_curr'+str(k),'w')
    go_curr.writelines(go_text)
    go_curr.close()
    
    subprocess.call(['chmod','+x',goOutDir + 'go_curr'+str(k)])    
#    null_out = open(os.devnull,'w')
#    subprocess.call('./go_curr'+str(k),stdout = null_out, stderr = null_out)    
#    shutil.copy('./' + str(k)+ '/my_trace_all.csv','./q_result/'+str(k)+'.csv')
#    os.remove('go_curr'+str(k))
#    shutil.rmtree(str(k))
#    print str(k) + ' size ' + str(os.stat('./'+str(k)+'/my_trace_all.csv').st_size)
#    print str(k) + ' ends'

key_all = 256
job_count = options.cpuCount

#aws_file = open('/home/bozhiliu/aws.sh','r')
#awsline = aws_file.readline()
#aws_address = awsline.split()[3]
##M Create directory before opening file

#final.write("ssh -i ~/ece_par.pem " + aws_address + " ./q_all.sh\n")
#final.write('sshpass -p "fpxdsp730113" scp -rp bozhiliu@filexfer.hpc.arizona.edu:/home/u26/bozhiliu/compiled/*.out ./compiled/\n')

##Create runDir + full_<config>.sh for each config with the 3 full.sh paths to execute
fullConfig = open(runDir + "full_" + str(options.config) + ".sh", 'w')
fullConfig.write("#!/bin/bash\n")
for iterations in range(options.runs):
    time.sleep(random.randint(3,5))
    new_folder = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    for con in [str(options.config)]:
        if options.run_type == 'normal':
            os.mkdir(qresultDir+ new_folder+con) ##Change to /xdisk
            fcurr = new_folder+con+"/"
        if options.run_type == 'masked':
            os.mkdir(qresultDir + '/masked/'+new_folder+con)
            fcurr = 'masked/'+new_folder+con+"/"

        ## Create directory tree for the new run
        ## intermediate directory to store results after gem5.opt simulations before copying back to q_result
        interDir = runDir + fcurr + "interOutput/"
        
        ##full.sh and its subfiles are kept in fullScriptDir folder in runDir
        fullDir = runDir + fcurr + "fullScriptDir/"
        
        ## go_curr files for each run
        goOutDir = runDir + fcurr + "goFiles/"

        ## resultDir
        resultDir = qresultDir + fcurr

        # Compiled a[].outs are stored here
        compile_folder = runDir + fcurr + "/compiled/"
        #McrossCompile_folder = runDir + fcurr + "/crossCompiled/"

        #M Create directory tree for each of these before opening files to write
        createDir(interDir)
        createDir(fullDir)
        createDir(goOutDir)
        createDir(resultDir)
        createDir(compile_folder)
        #McreateDir(crossCompile_folder)

        ## Add full.sh to the fullConfig 
        fullConfig.write(". " + fullDir + "/full.sh\n")

        ##M multiprocessing the creation of go_curr[0-255]
        for batch in range(4):    
            jobs = []
            for kk in range(256):
                pp = multiprocessing.Process(target=process_one, args=(kk,fcurr))
                jobs.append(pp)
                pp.start()    
                
            for jj in jobs:
                jj.join()
        
        final = open(fullDir + 'full.sh','w')
        final.write("echo \"Starting full.sh\" \n")
        final.write("day=$(date | cut -d ' ' -f 3)\n")
        final.write("echo \"$(date)\" \n")
        final.write("wait\n")
        final.write("sleep 5m\n")
        final.write("day=$(date | cut -d ' ' -f 3)\n")
        final.write("echo \"$(date)\" \n")

        for j in range(job_count):
            f = open(fullDir + 'full'+str(j)+'_'+str(iterations)+'_'+ con+'.sh','w')
            for k in range(key_all/job_count):
                js = str(j*(key_all/job_count) + k % (key_all/job_count))        
                f.write('current_date_time="`date +%Y/%m/%d--%H:%M:%S`";\n')
                f.write('echo $current_date_time ' + js + '\n')
                f.write(goOutDir + '/go_curr'+js+' > /dev/null 2>&1\n')
                f.write('wait $!\n')
                f.write('mv ' + interDir + js + '/my_trace_all.csv ' + resultDir +'/dram' + js + '.txt\n')
                f.write('mv ' + interDir + js + '/CPU.bin ' + resultDir +'/CPU' + js + '.bin\n')
                f.write('mv ' + interDir + js + '/Icache.bin ' + resultDir +'/Icache' + js + '.bin\n')
                f.write('mv ' + interDir + js + '/Dcache.bin ' + resultDir +'/Dcache' + js + '.bin\n')
                f.write('mv ' + interDir + js + '/L2cache.bin ' + resultDir +'/L2cache' + js + '.bin\n')
                f.write('mv ' + interDir + js + '/Time.bin ' + resultDir +'/Time' + js + '.bin\n')
                f.write('mv ' + interDir + js + '/Count.txt ' + resultDir +'/Count' + js + '.txt\n')

            #f.write('python extract_key.py '+' ' + js + '\n')
                f.write('rm -rf ' + interDir + js + '\n')
                f.write('rm -rf ' + resultDir +'/' + js + '.csv\n')
                subprocess.call(['chmod','+x',fullDir + 'full'+str(j)+'_'+str(iterations)+'_'+ con+'.sh'])     
            f.close()

        for j in range(key_all % job_count):
            f = open(fullDir + 'full'+str(j)+'_'+ str(iterations)+'_'+con+'.sh','a')
            js = str(key_all - 1 - j)
            f.write('current_date_time="`date +%Y/%m/%d--%H:%M:%S`";');
            f.write('echo $current_date_time ' + js + '\n')
            f.write(goOutDir + '/go_curr'+js+' > /dev/null 2>&1\n')
            f.write('wait $!\n')
            
            f.write('mv ' + interDir + js + '/my_trace_all.csv ' + resultDir +'/dram' + js + '.txt\n')
            f.write('mv ' + interDir + js + '/CPU.bin ' + resultDir +'/CPU' + js + '.bin\n')
            f.write('mv ' + interDir + js + '/Icache.bin ' + resultDir +'/Icache' + js + '.bin\n')
            f.write('mv ' + interDir + js + '/Dcache.bin ' + resultDir +'/Dcache' + js + '.bin\n')
            f.write('mv ' + interDir + js + '/L2cache.bin ' + resultDir +'/L2cache' + js + '.bin\n')
            f.write('mv ' + interDir + js + '/Time.bin ' + resultDir +'/Time' + js + '.bin\n')
            f.write('mv ' + interDir + js + '/Count.txt ' + resultDir +'/Count' + js + '.txt\n')

        #        f.write('mv ./' + js + '/my_trace_all.csv ' + resultDir +'/' + js + '.csv\n')
        #        f.write('python extract_key.py '+' ' + js + '\n')
            f.write('rm -rf ' + interDir + js + '\n')
            f.write('rm -rf ' + resultDir +'/' + js + '.csv\n')
            subprocess.call(['chmod','+x',fullDir + 'full'+str(j)+'_'+str(iterations)+'_'+con+'.sh'])     
            f.close()
    
        if options.run_type == 'normal':
            #Mfinal.write('rm -rf ' + compile_folder + '/a*.out \n')
            final.write('/manojwork/work/full_pure.sh ' + fcurr + '\n')
            #Mfinal.write('cp ' + crossCompile_folder + '/*.out ' +  compile_folder + '\n')
        if options.run_type == 'masked':
            final.write('rm -rf ./compiled_masked/a*.out \n')
            final.write('/manojwork/work/full_masked.sh\n')
            final.write('cp /home/complete/Masked/Byte/compiled/*.out compiled/\n')
            
        final.write('cp ' + seconfigDir + 'seconfig_'+con + ' ' + seconfigDir + 'seconfig\n')
        for j in range(job_count):
            final.write('nohup ' + fullDir +'/full'+str(j)+'_'+ str(iterations)+'_'+con+'.sh >>' + fullDir + 'n'+str(j)+'.log &\n')
#            final.write('pids[${'+str(j)+'}]=$!\n')
#        final.write('for pid in ${pids[*]}; do\n')
#        final.write('    wait $pid\n')
#        final.write('done\n')
        #Mfinal.write(mainDir + 'parse_dram.py ' + resultDir + fcurr+'\n') ##Since incomplete parse_dram.py was copied
        final.write('wait\n');
        final.write('head ' + seconfigDir +'seconfig\n')
        #Mfinal.write('ls q_result/*${day}_*'+con+'*/ | wc -l \n')
    
final.close()
fullConfig.close()
subprocess.call(['chmod', '+x',fullDir + 'full.sh'])
