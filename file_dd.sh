#!/bin/sh

PREFIX=$1
SIZE=$2
AMOUNT=$3
for COUNTER in `seq 1 1 $AMOUNT`; do
  INDEX=`printf "%06d" $COUNTER`
  dd if=/dev/zero of=$PREFIX-$INDEX bs=1024 count=`expr 1024 \* $SIZE`
done

