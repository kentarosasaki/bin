#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
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
    csvfile = open(os.path.join(''.join((initfilepath, os.sep, "config")),
                   "mapping.csv"), 'r')
    csvloop = csv.reader(csvfile)

    # Create a logging file.
    loggingfile = os.path.join(''.join((initfilepath, os.sep, "log")),
                               'backup.log')
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

