#!/usr/local/bin/python3
# coding=utf-8

import filecmp
import logging
import logging.handlers
import os
import socket
import shutil
import time


init_file_path = os.path.dirname(os.path.abspath(__file__))
host = socket.gethostname()
logging_file_name = ''.join(("backup_", host, ".log"))
logging_dir = ''.join((init_file_path, os.sep, "log"))
logging_file = os.path.join(logging_dir, logging_file_name)
if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)
log = logging.getLogger()
log.setLevel(logging.INFO)
formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s')
handler = logging.handlers.TimedRotatingFileHandler(
          filename=logging_file,
          when='D',
          backupCount=7)
handler.setFormatter(formatter)
log.addHandler(handler)


class BackupCollector(object):

    def __init__(self):
        self.log = logging.getLogger("BackupCollector")
        self.cache = {}

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
        # Return the full path of exsinting files.
        return [os.path.join(root, item)
                for root, dirs, items in self.os_walk_cache(directory)
                for item in items]

    def cut_base_dir(self, base_dir, directory):
        # Return the path which cut base dir.
        return [item.replace(base_dir, "") for item in directory]

    def copy(self, source, destination, index):
        """ Copy files.

        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        index       - The index that exist only source.

        """
        for index_elem in index:
            src_item = os.path.join(source, index_elem)
            dst_item = os.path.join(destination, index_elem)
            dst_dir = os.path.dirname(dst_item)
            if not os.path.exists(dst_dir):
                self.log.debug("Make directory: %s" % dst_dir)
                os.makedirs(dst_dir)
            try:
                self.log.debug("Copy file: %s" % dst_item)
                shutil.copy2(src_item, dst_item)
            except Exception as msg:
                pass

    def update(self, source, destination, index):
        """ Update existing files.

        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        index       - The index that exist both source and destination.

        """
        for index_elem in index:
            src_item = os.path.join(source, index_elem)
            dst_item = os.path.join(destination, index_elem)
            try:
                if os.path.exists(src_item) and os.path.exists(dst_item):
                    src_mtime = os.path.getmtime(src_item)
                    dst_mtime = os.path.getmtime(dst_item)
                    duration = src_mtime - dst_mtime
                    if int(duration) > 0 or not filecmp.cmp(src_item, dst_item):
                        try:
                            self.log.debug("Update file: %s" % dst_item)
                            shutil.copy2(src_item, dst_item)
                        except Exception as msg:
                            pass
            except Exception as msg:
                pass

    def trimming(self, directory, retention):
        """ Delete old archives - This deletes files, be careful with it.

        directory   - The directory which is deleted.
        retention   - Delete older than this days

        """
        limit_timestamp = time.time() - 86400 * int(retention)
        for remove_item in directory:
            item_mtime = os.path.getmtime(remove_item)
            duration = limit_timestamp - item_mtime
            if int(duration) > 0:
                try:
                    os.unlink(remove_item)
                    self.log.debug("File delete successful in %s" %
                                   remove_item)
                except Exception as msg:
                    self.log.error("Delete error: %s %s"
                                   % (remove_item, str(msg)))
                    pass

    def run(self, source, destination, retention=90):
        """ Perform a backup.

        source      - The source directory who's contents should be backed up.
        destination - The directory that the backup should go into.
        retention   - (Optional) Delete older than this days, defaults to 90.

        """
        self.log.info("Start backup: %s %s" % (source, destination))
        # Get the full path of directory.
        full_src = self.search_file(source)
        full_dst = self.search_file(destination)
        # Get the path which is already cut the base dir in mapping file.
        src = self.cut_base_dir(source, full_src)
        dst = self.cut_base_dir(destination, full_dst)
        # Create set object.
        set_src = set(src)
        set_dst = set(dst)
        # Get the list which is in only source.
        src_only = set_src - set_dst
        # Get the line which is in both source and destination.
        common = set_src & set_dst
        # Copy the files which is in only source.
        self.copy(source, destination, src_only)
        # Update the files which mtime is updated.
        self.update(source, destination, common)
        # Trimming old archives which is older than retention, defaults to 90
        self.trimming(full_dst, retention)
        self.log.info("Finish backup: %s %s" % (source, destination))

