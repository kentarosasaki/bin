#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import sys

from lib import bkutil


def csv_to_list(csv_name):
    return [row for row in csv_name if os.path.isdir(row[0]) and
                                       os.path.isdir(row[1])]


def main():
    # Set init file path.
    init_file_path = os.path.dirname(os.path.abspath(__file__))
    # Create a resource file object.
    if not len(sys.argv) == 2:
        sys.exit('Usage: %s CSVfile' % sys.argv[0])
    mapping_file = os.path.join(''.join((init_file_path, os.sep, "config")),
                                sys.argv[1])
    if not os.path.exists(mapping_file):
        sys.exit('ERROR: CSV File %s was not found!' % mapping_file)
    csv_file = open(mapping_file, 'r')
    csv_loop = csv.reader(csv_file)
    # Create a object.
    backup = bkutil.BackupCollector()
    # Perform a backup.
    [(backup.run(path[0], path[1])) for path in csv_to_list(csv_loop)]
    # Close csv file.
    csv_file.close()


if __name__ == '__main__':
    main()

