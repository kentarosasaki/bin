#!/bin/sh

for file in *
do
  mv "$file" `echo $file | tr ' ' '_' | tr '[A-Z]' '[a-z]'`
done
