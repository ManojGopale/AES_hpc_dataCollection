cd /manojwork/work/complete_cross/
./runs.py -f ${1} ##Taking the file name which was created before calling this file
./compile_all.sh ${1} ## fcurr is given so that a[].out can be placed appropriately

## 
## /home/vagrant/work/complete_cross/runs.py ## This generates main*.c 
## /home/vagrant/work/complete_cross/compile_all.sh ## Compile all the main*.c
## /home/vagrant/work/complete_cross/main.c ## Change the WORKLOAD here to generate all main_*.c
## /home/vagrant/work/complete_cross/main0.c
## /home/vagrant/work/complete_cross/aes.c

