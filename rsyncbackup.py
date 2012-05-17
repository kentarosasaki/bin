#! /usr/bin/python
# -*- coding: utf-8 -*-

import commands
import logging
import os
import os.path
import re
import time
from datetime import date

class RsyncBackup:
    def __init__(self, rsync="/usr/bin/rsync"):
        """ Creates an object that can perform backups using Rsync.
        rsync         - Specify the location of the rsync binary.
        """
        self.log = logging.getLogger("RsyncBackup")
        self.rsync = rsync

    def backup(self, source, destination):
        """ Perform a backup using rsync.
        source        - The source directory who's contents should be backed up.
        destination   - The directory that the backup should go into.
        Returns true if successful, false if an error occurs.
        """
        cmnd = "%s '%s' '%s' -acvzut" % (self.rsync, source, destination)
        self.log.debug ("Running command: %s" % cmnd)
        result = commands.getstatusoutput(cmnd)
        if (result[0] == 0):
            self.log.info("Rsync backup successful.")
            self.log.debug("Rsync output: %s" % result[1])
        else:
            self.log.error("Error running rsync: %s" % result[1])
            return 0
        return 1

    def trim_archives(self, removedir, retention=90):
        """ Delete old archives - WARNING: This deletes files, be careful with it.
        removeDir     - The directory which is deleted.
        retention     - (Optional) Delete older than this days, defaults to 7.
        """
        self.log.info("Starting deletion.")
        limit_timestamp = time.time() - 86400 * retention
        def _os_walk_cache(dir):
            cache = {}
            if dir in cache:
                for x in cache[dir]:
                    yield x
            else:
                cache[dir] = []
                for x in os.walk(dir):
                    cache[dir].append(x)
                    yield x
            raise StopIteration()
        for root, dirs, files in _os_walk_cache(removedir):
            # If file is all old, turn delflag True
            for file in files:
                filepath = os.path.join(root, file)
                filemtime = os.path.getmtime(filepath)
                if filemtime < limit_timestamp: # Old file
                    try:
                        os.unlink(filepath)
                        self.log.info("File deletion successful.")
                    except OSError, e:
                        pass
            # Delete blank directories
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                try:
                    os.rmdir(dirpath)
                    self.log.info("Blank Directory deletion successful.")
                except OSError, e:
                    pass
