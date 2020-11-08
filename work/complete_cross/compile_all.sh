#!/bin/bash
dirPath="/manojwork/work/complete_cross"
SOURCE="$dirPath/m5/m5op_arm.o $dirPath/aes.c $dirPath/aes.h"
BINARY=a.out
GCCOPT="-O0 -D ASM='\"$1\"'"
COMPILER="arm-linux-gnueabi-gcc-5"

for i in `seq 0 255`;
do
		##Since the main[].c are in mainFiles/fcurr now from the earlier script[/home/vagrant/work/complete_cross/runs.py] that stores it there
    MAIN="/xdisk/manojgopale/AES/dataCollection/runDir/${1}/mainFiles/main"$i".c"
    ##OUT="./compiled/a"$[ i ]".out"
    OUT="/xdisk/manojgopale/AES/dataCollection/runDir/${1}/compiled/a"$[ i ]".out"
    mkCmd="mkdir /xdisk/manojgopale/AES/dataCollection/runDir/${1}/compiled/"
    eval "$mkCmd"
    echo $OUT
    eval "$COMPILER $GCCOPT -funroll-loops $SOURCE $MAIN -static -o $OUT -w"&
    if [ $(( $i%4 )) -eq 0 ]; then
	echo $i
	wait
    fi
done
