#! /usr/bin/python
# -*- coding: utf-8 -*-

import autotier
import logging
import logging.handlers
import os
import shlex

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

def rcfile_to_list(filename):
    output = []
    with open(filename) as f_in:
        dic = {}
        lex = shlex.shlex(f_in)
        lex.whitespace_split = True
        while True:
            key = lex.get_token()
            val = lex.get_token()
            if not key or not val:
                break
            dic[key] = val
            output.append([key, val])
    return output

# Create a backup object.
backup = autotier.DataSync()
delete = autotier.TrimArchives()

[backup.synchronize(list[0], list[1]) for list in rcfile_to_list(rcfile)]
[delete.trimming(list[1]) for list in rcfile_to_list(rcfile)]

# Close the logging out.
logging_handler.close()
