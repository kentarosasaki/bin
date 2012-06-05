#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import os.path
import re
import shlex
import subprocess
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
        args = shlex.split(cmnd)
        self.log.debug ("Running command: %s" % args)
        backuputil = BackupUtils()
        result = backuputil.get_status_output(args)
        if (result[0] == 0):
            self.log.info("Rsync backup successful.")
            self.log.debug("Rsync output: %s" % result[1])
        else:
            self.log.error("Error running rsync: %s" % result[1])
            return 0
        return 1

    def trim_archives(self, removedir, retention=90):
        """ Delete old archives - This deletes files, be careful with it.
        removeDir     - The directory which is deleted.
        retention     - (Optional) Delete older than this days, defaults to 90.
        """
        self.log.info("Starting deletion.")
        limit_timestamp = time.time() - 86400 * retention
        backuputil = BackupUtils()
        for root, dirs, files in backuputil.os_walk_cache_util(removedir):
            # If file is all old, turn delflag True
            for file in files:
                filepath = os.path.join(root, file)
                filemtime = os.path.getmtime(filepath)
                if filemtime < limit_timestamp: # Old file
                    try:
                        os.unlink(filepath)
                        self.log.info("File deletion successful in %s" %
                                      filepath)
                    except OSError, e:
                        pass
            # Delete blank directories
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                try:
                    os.rmdir(dirpath)
                    self.log.info("Blank Directory deletion successful in %s" %
                                  dirpath)
                except OSError, e:
                    pass

class BackupUtils:
    def get_status_output(self, command):
        # Return (status, output) of executing command in a shell.
        pipe = subprocess.Popen(command, universal_newlines=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = str.join("", pipe.stdout.readlines())
        status = pipe.wait()
        if status is None:
            status = 0
        return status, output

    def os_walk_cache_util(self, directory):
        cache = {}
        if directory in cache:
            for x in cache[directory]:
                yield x
        else:
            cache[directory] = []
            for x in os.walk(directory):
                cache[directory].append(x)
                yield x
        raise StopIteration()

