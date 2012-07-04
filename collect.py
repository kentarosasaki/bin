#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import socket
import sys

from lib import log
from lib import sync
from lib import trimming


def csv_to_list(csvname):
    return [row for row in csvname if os.path.isdir(row[0]) and
                                      os.path.isdir(row[1])]


def main():

    # Set init file path.
    initfilepath = os.path.dirname(os.path.abspath(__file__))

    # Create a resource file object.
    if not len(sys.argv) == 2:
        sys.exit('Usage: %s mappingfile' % sys.argv[0])

    mappingfile = os.path.join(''.join((initfilepath, os.sep, "config")),
                               sys.argv[1])

    if not os.path.exists(mappingfile):
        sys.exit('ERROR: Mapping File %s was not found!' % mappingfile)

    csvfile = open(mappingfile, 'r')
    csvloop = csv.reader(csvfile)

    # Create a logging file.
    host = socket.gethostname()
    loggingfilename = ''.join(("backup_", host, ".log"))
    loggingfile = os.path.join(''.join((initfilepath, os.sep, "log")),
                               loggingfilename)
    log.logging_config(loggingfile)

    # Create objects.
    backup = sync.Sync()
    delete = trimming.Trimming()
    [(backup.sync(path[0], path[1]), delete.trimming(path[1]))
      for path in csv_to_list(csvloop)]

    # Close csv file.
    csvfile.close()


if __name__ == '__main__':
    main()

