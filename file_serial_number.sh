#!/bin/bash

i=1
for f in *.jpg
do
  g=0000$i.jpg
  mv $f ${g:(-9)}
  i=$((i+1))
done
