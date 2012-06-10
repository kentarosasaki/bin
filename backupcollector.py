#! /usr/bin/python
# -*- coding: utf-8 -*-

import autotier
import logging
import logging.handlers
import os
import shlex

def rcfile_to_list(filename):
    output = []
    with open(filename) as f_in:
        dic = {}
        lex = shlex.shlex(f_in)
        lex.whitespace_split = True
        while True:
            key = lex.get_token()
            value = lex.get_token()
            if not key or not value:
                break
            if not key.endswith(os.sep):
                modkey = ''.join([key, os.sep])
            if not value.endswith(os.sep):
                modval = "".join([value, os.sep])
            dic[modkey] = modval
            output.append([modkey, modval])
    return output

def main():
    # Logging to a file done here
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logging_formatter = logging.Formatter(
                        '%(asctime)s %(levelname)s %(name)s %(message)s')
    logging_handler = logging.handlers.TimedRotatingFileHandler(
                      filename='backup.log',
                      when='D',
                      backupCount=7)
    logging_handler.setFormatter(logging_formatter)
    logging_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(logging_handler)

    # Create a resource file object.
    rcfile = os.path.join('mappings.rc')

    # Create objects.
    backup = autotier.DataSync()
    delete = autotier.TrimArchives()
    [(backup.synchronize(path[0], path[1]), delete.trimming(path[1]))
      for path in rcfile_to_list(rcfile)]

    # Close the logging out.
    logging_handler.close()

if __name__ == '__main__':
    main()
