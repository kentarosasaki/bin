#!/usr/local/bin/python3
# coding=utf-8

import csv
import fcntl
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
    # Create a object.
    backup = bkutil.BackupCollector()
    # Open csv file.
    with open(mapping_file, 'r') as csv_file:
        csv_loop = csv.reader(csv_file)
        # Perform a backup.
        [(backup.run(item[0], item[1], item[2])) if len(item) == 3
          else (backup.run(item[0], item[1])) for item in csv_to_list(csv_loop)]



if __name__ == '__main__':
    with open(sys.argv[0], 'r') as lockfile:
        fcntl.flock(lockfile.fileno(), fcntl.LOCK_EX)
        main()

