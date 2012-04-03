#!/bin/sh

#####################################
# Backup Script
#####################################

#
# Shell Environmental Variables
#

BK_FILE="user_account"
BK_DIR="/Users/"
BK_HD="ext_HD_name"
DEST="/Volumes/$BK_HD"
DATE=`date +%Y%m%d`

#####################################
# Error Handling
#####################################

#
# Check Mount Flag
#

mount_flag()
{
  if [ $1 -eq 0 ]
  then
    echo "mount $BK_HD"
  else
    echo "mount error $BK_HD"
    exit 1
  fi
}

#
# Check Mount HD
#

check_mount()
{
  if [ ! -d $DEST ]
  then
    hdiutil attach /dev/disk1s3
    mount_flag ${?}
  else
    echo "$BK_HD is still mounted"
  fi
}

#####################################
# Backup Handling
#####################################

check_mount

#
# Done archive and compress
#

if [ -d $DEST ]
then
  cd $BK_DIR
  tar -cvf - $BK_FILE | gzip > $DEST/backup/$DATE-backup.tar.gz
else
  echo "Couldn't backup because HDD couldn't be mounted"
  exit 1
fi

#
# Delete old backup files
#

if [ -e $DEST/backup/$DATE-backup.tar.gz ]
then
  find $DEST/backup/ -name '*.tar.gz' -mtime +30 -exec rm -f {} \;
fi
