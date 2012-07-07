#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import logging
import os
import shutil
import time


class Sync(object):

    def __init__(self):
        self.cache = {}
        self.log = logging.getLogger("Sync")

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

    def search_file(self, directory):
        return [os.path.join(root, file)
                for root, dirs, files in self.os_walk_cache(directory)
                for file in files]

    def cut_base_dir(self, base_dir, path):
        return [item.replace(base_dir, "") for item in path]

    def copy(self, source, destination, index):
        """ Copy files.
        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        index       - The index that exist only source.
        """
        for index_elem in index:
            source_item = os.path.join(source, index_elem)
            destination_item = os.path.join(destination, index_elem)
            destination_dir = os.path.dirname(destination_item)
            if not os.path.exists(destination_dir):
                self.log.debug("Make directory: %s" % destination_dir)
                os.makedirs(destination_dir)
            try:
                self.log.debug("Copy file: %s" % destination_item)
                shutil.copy2(source_item, destination_item)
            except Exception as msg:
                self.log.error("Copy error: %s %s %s"
                               % (source, destination, str(msg)))
                pass
        return 1

    def update(self, source, destination, index):
        """ Update existing files.
        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        index       - The index that exist both source and destination.
        """
        for index_elem in index:
            source_item = os.path.join(source, index_elem)
            destination_item = os.path.join(destination, index_elem)
            source_mtime = os.path.getmtime(source_item)
            destination_mtime = os.path.getmtime(destination_item)
            if source_mtime > destination_mtime:
                try:
                    self.log.debug("Update file: %s" % destination_item)
                    shutil.copy2(source_item, destination_item)
                except Exception as msg:
                    self.log.error("Update error: %s %s %s"
                                   % (source, destination, str(msg)))
                    pass
        return 1

    def trimming(self, path, retention=90):
        """ Delete old archives - This deletes files, be careful with it.
        path        - The directory which is deleted.
        retention   - (Optional) Delete older than this days, defaults to 90.
        """
        limit_timestamp = time.time() - 86400 * retention
        for remove_file in path:
            file_mtime = os.path.getmtime(remove_file)
            if limit_timestamp > file_mtime: # Old file
                try:
                    os.unlink(remove_file)
                    self.log.debug("File delete successful in %s" %
                                   remove_file)
                except Exception as msg:
                    self.log.error("Delete error: %s %s"
                                   % (remove_file, str(msg)))
                    pass
        return 1

    def run(self, source, destination):
        """ Perform a backup.
        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        """
        self.log.info("Start backup: %s %s" % (source, destination))
        full_src = self.search_file(source)
        full_dst = self.search_file(destination)
        src = self.cut_base_dir(source, full_src)
        dst = self.cut_base_dir(destination, full_dst)
        set_src = set(src)
        set_dst = set(dst)
        # Difference set.
        src_only = set_src - set_dst
        # Product set.
        common = set_src & set_dst
        self.copy(source, destination, src_only)
        self.update(source, destination, common)
        self.trimming(full_dst)
        return 1


