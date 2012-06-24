#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time


class Sync(object):

    def __init__(self):
        self.cache = {}
        self.log = logging.getLogger("Sync")

    def os_listdir_cache(self, directory):
        if directory in self.cache:
            for x in self.cache[directory]:
                yield x
        else:
            self.cache[directory] = []
            for x in os.listdir(directory):
                self.cache[directory].append(x)
                yield x
        raise StopIteration()

    def listdir(self, path):
        ans = {}
        if not os.path.exists(path):
            self.log.debug("Make directory: %s" % path)
            os.makedirs(path)
        for item in self.os_listdir_cache(path):
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
                try:
                    self.log.debug("Copy file: %s" % destination_item)
                    shutil.copy2(source_item, destination_item)
                except Exception, msg:
                    self.log.error("Copy error: %s %s %s"
                                   % (source, destination, str(msg)))
                    pass
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
                    try:
                        self.log.debug("Update file: %s" % destination_item)
                        shutil.copy2(source_item, destination_item)
                    except Exception, msg:
                        self.log.error("Update error: %s %s %s"
                                       % (source, destination, str(msg)))
                        pass
        return 1

    def sync(self, source, destination):
        """ Perform a backup.
        source       - The source directory who's contents should be backed up.
        destination  - The directory that the backup should go into.
        Returns true if successful, false if an error occurs.
        """
        self.log.info("Start backup: %s %s" % (source, destination))
        src = self.listdir(source)
        dst = self.listdir(destination)
        merge = self.merge(src, dst)
        src_only = self.subtract(src, dst)
        dst_only = self.subtract(dst, src)
        del_src = self.subtract(merge, src_only)
        common = self.subtract(del_src, dst_only)
        #self.copy(source, destination, src_only)
        #self.update(source, destination, common)
        return 1


