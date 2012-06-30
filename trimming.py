#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time


class Trimming(object):

    def __init__(self):
        self.cache = {}
        self.log = logging.getLogger("Trimming")

    def os_walk_cache(self, directory):
        if directory in self.cache:
            for x in self.cache[directory]:
                yield x
        else:
            self.cache[directory] = []
            for x in os.walk(directory):
                self.cache[directory].append(x)
                yield x
        raise StopIteration()

    def trimming(self, removedir, retention=90):
        """ Delete old archives - This deletes files, be careful with it.
        removedir - The directory which is deleted.
        retention - (Optional) Delete older than this days, defaults to 90.
        """
        self.log.info("Start deletion: %s" % removedir)
        limit_timestamp = time.time() - 86400 * retention
        for root, dirs, files in self.os_walk_cache(removedir):
            # If file is all old, turn delflag True
            for file in files:
                filepath = os.path.join(root, file)
                filemtime = os.path.getmtime(filepath)
                if filemtime < limit_timestamp: # Old file
                    try:
                        os.unlink(filepath)
                        self.log.debug("File deletion successful in %s" %
                                       filepath)
                    except OSError as e:
                        pass
            # Delete blank directories
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                try:
                    os.rmdir(dirpath)
                    self.log.debug("Blank Directory deletion successful in %s" %
                                   dirpath)
                except OSError as e:
                    pass
        return 1


