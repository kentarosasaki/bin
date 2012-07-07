#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import logging
import logging.handlers
import os
import socket
import sys

from lib import sync


def logging_config(logging_file):
    # Logging to a file done here.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s %(message)s')
    handler = logging.handlers.TimedRotatingFileHandler(
              filename=logging_file,
              when='D',
              backupCount=7)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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

    # Create a logging file.
    host = socket.gethostname()
    logging_file_name = ''.join(("backup_", host, ".log"))
    logging_file = os.path.join(''.join((init_file_path, os.sep, "log")),
                                logging_file_name)
    logging_config(logging_file)

    # Create objects.
    backup = sync.Sync()
    [(backup.run(path[0], path[1])) for path in csv_to_list(csv_loop)]

    # Close csv file.
    csv_file.close()


if __name__ == '__main__':
    main()

