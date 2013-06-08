#!/bin/bash
#
# ex).
# file_serial_number.sh /Users/${USER}/Documents/pictures/${path_to_jpeg} ${date}
#

PATH=${1}
DATE=${2}
i=1
for f in ${PATH}/*.jpg
do
  g=0000$i.jpg
  /bin/mv $f ${PATH}/${2}_${g:(-9)}
  i=$((i+1))
done
