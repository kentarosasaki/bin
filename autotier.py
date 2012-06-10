#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time


class DataSync(object):

    def __init__(self):
        self.log = logging.getLogger("DataSync")

    def listdir(self, path):
        ans = {}
        for item in os.listdir(path):
            fullpath = os.path.join(path, item)
            if os.path.isdir(fullpath):
                ans[''.join([item, os.sep])] = self.listdir(fullpath)
            else:
                ans[item] = ()
        return ans

    def subtract(self, include, exclude):
        ans = {}
        for key, value in include.iteritems():
            if isinstance(value,dict):
                if value != exclude.get(key, None):
                    ans[key] = self.subtract(value, exclude.get(key,{}))
            else:
                if not exclude.has_key(key):
                    ans[key] = tuple(value)
        return ans

    def merge(self, include, extend):
        ans = self.subtract(include, {})
        for key, value in extend.iteritems():
            if isinstance(value,dict):
                ans[key] = self.merge(value, include.get(key, {}))
            else:
                ans[key] = tuple(value)
        return ans

    def copy(self, source, destination, index):
        if not os.path.exists(destination):
            self.log.debug("Make directory: %s" % destination)
            os.makedirs(destination)
        for key, value in index.iteritems():
            source_item = os.path.join(source, key)
            destination_item = os.path.join(destination, key)
            if isinstance(value, dict):
                self.copy(source_item, destination_item, value)
            else:
                self.log.debug("Copy file: %s" % source_item)
                shutil.copy2(source_item, destination_item)
        return 1

    def update(self, source, destination, index):
        for key, value in index.iteritems():
            source_item = os.path.join(source, key)
            destination_item = os.path.join(destination, key)
            if isinstance(value, dict):
                self.update(source_item, destination_item, value)
            else:
                d = os.path.getmtime(source_item) - os.path.getmtime(
                                                    destination_item)
                if d > 0:
                    self.log.debug("Update --->: %s" % source_item)
                    shutil.copy2(source_item, destination_item)
        return 1

    def synchronize(self, source, destination):
        """ Perform a backup.
        source       - The source directory who's contents should be backed up.
        destination  - The directory that the backup should go into.
        Returns true if successful, false if an error occurs.
        """
        self.log.info("Start backup: %s %s" % (source, destination))
        sub = self.subtract
        src = self.listdir(source)
        dst = self.listdir(destination)
        common = self.merge(src, dst)
        common = sub(common, sub(src, dst))
        common = sub(common, sub(dst, src))
        to_dst = sub(src, dst)
        if not self.copy(source, destination, to_dst):
            self.log.error("Error copping: %s %s" % (source, destination))
        if not self.update(source, destination, common):
            self.log.error("Error updating: %s %s" % (source, destination))
        return 1

class TrimArchives(object):

    def __init__(self):
        self.cache = {}
        self.log = logging.getLogger("TrimArchives")

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
                    except OSError, e:
                        pass
            # Delete blank directories
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                try:
                    os.rmdir(dirpath)
                    self.log.debug("Blank Directory deletion successful in %s" %
                                   dirpath)
                except OSError, e:
                    pass
        self.log.info("Finish deletion.")
        return 1

