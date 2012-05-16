#!/usr/bin/python

import RSyncBackup
import logging, logging.handlers

LOG_FILE="backup.log"
LAST_RUN_FILE="backup.lrf"

# Logging to a file done here
rootLogger = logging.getLogger()
loggingHandler = logging.FileHandler (LOG_FILE)
loggingFormatter = logging.Formatter ('%(asctime)s %(levelname)s %(name)s %(message)s')
loggingHandler.setFormatter (loggingFormatter)
rootLogger.setLevel (logging.DEBUG)
rootLogger.addHandler (loggingHandler)

# Logging to email of any errors
## emailHandler = logging.handlers.SMTPHandler ("localhost", "backup@rock", ["root@rock"], "Backup error.")
## emailHandler.setFormatter (loggingFormatter)
## emailHandler.setLevel (logging.ERROR)
## rootLogger.addHandler (emailHandler)

# Create a backup object.  Remove testRun once you've debugged it.
backup = RSyncBackup.RSyncBackup (lastRunFile = LAST_RUN_FILE, rsync="/usr/bin/rsync", testRun=0)
try:
    if (backup.timeToBackup()):
        # It's time to perform a backup.
        
        # Exclude the media directory - it's too large to backup.
        # Backup all the home directories to /backup/current/ with archives to /backup/archives/
        # exclude = ['colin/media']
        #backup.backup (source="/Users/kentaro/tmp1/", destination="/Users/kentaro/tmp2/", archive="/backup/archives/", excludeList=exclude)
        
        # Backup MySQL with no archives
        backup.backup (source="/Users/kentaro/tmp1/", destination="/Users/kentaro/tmp2/")
        
        # Only keep 5 days worth of evolution archives - it changes too rapidly and is big!
        # This demonstrates the use of the filter regular expression - use with great care!
        #backup.trimArchives ('/backup/archives', filter="evolution$", entriesToKeep=5)
        
        # Only keep 60 backups worth of archives for all files
        backup.trimArchives ('/Users/kentaro/tmp2/', filter="tmp*", entriesToKeep=60)
        
        # Backup finished
        backup.finish()
except Exception, e:
    logging.error ("Exception occured during backup: %s" % str (e))

# Close the logging out.
loggingHandler.close()
