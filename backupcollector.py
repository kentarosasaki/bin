#! /usr/bin/python
# -*- coding: utf-8 -*-

import autotier
import csv
import os

def csv_to_list(filename):
    return [row for row in filename]

def main():

    # Create a resource file object.
    csvfile = open(os.path.join('mappings.csv'))
    csvloop = csv.reader(csvfile)

    # Create objects.
    backup = autotier.DataSync()
    delete = autotier.TrimArchives()
    [(backup.synchronize(path[0], path[1]), delete.trimming(path[1]))
      for path in csv_to_list(csvloop)]

    # Close csv file.
    csvfile.close()

if __name__ == '__main__':
    main()
