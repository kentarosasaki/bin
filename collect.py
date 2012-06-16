#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from lib import log
from lib import sync
from lib import trimming


def csv_to_list(filename):
    return [row for row in filename]


def main():

    # Create a resource file object.
    csvfile = open(os.path.join("config", "mapping.csv"), 'r')
    csvloop = csv.reader(csvfile)

    # Create a logging file.
    log.logging_config('backup.log')

    # Create objects.
    backup = sync.Sync()
    delete = trimming.Trimming()
    [(backup.sync(path[0], path[1]), delete.trimming(path[1]))
      for path in csv_to_list(csvloop)]

    # Close csv file.
    csvfile.close()


if __name__ == '__main__':
    main()

