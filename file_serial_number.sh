#!/bin/bash
#
# ex).
# file_serial_number.sh /Users/${USER}/Documents/pictures/${path_to_jpeg} ${date}
#

PATH=${1}
#DATE=${2}

#for file in ${PATH}/*.jpg
#do
#  mv "$file" `echo $file | tr ' ' '_' | tr '[A-Z]' '[a-z]'`
#done

i=1
FLIST=`/usr/bin/find ${PATH} -type f -name "*.jpg"`
#for f in ${PATH}/*.jpg
for f in ${FLIST}
do
  g=0000$i.jpg
  /bin/mv $f ${PATH}/${g:(-9)}
  i=$((i+1))
done
