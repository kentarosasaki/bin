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
logging_handler.setLevel(logging.INFO)
root_logger.addHandler(logging_handler)

# Logging to email of any errors
## email_handler = logging.handlers.SMTPHandler(
##                 "localhost", "backup@rock", ["root@rock"], "Backup error.")
## email_handler.setFormatter(logging_formatter)
## email_handler.setLevel(logging.ERROR)
## root_logger.addHandler(email_handler)

# Create a backup object.
backup = autotier.AutoTier(rsync="/usr/bin/rsync")

# Create a resource file object.
rcfile = os.path.join(os.path.dirname(__file__),
                      'mappings.rc')

try:
    f_in = open(rcfile)
except IOError, (errno, msg):
    logging.error("Cannot read file %s: %s" % (rcfile, msg))
else:
    try:
        try:
            dic = {}
            lex = shlex.shlex(f_in)
            lex.whitespace_split = True
            while True:
                key = lex.get_token()
                val = lex.get_token()
                if not key or not val:
                    break
                dic[key] = val
                for key, value in dic.iteritems():
                    try:
                        backup.sync(source=key, destination=value)
                        backup.trim_archives(removedir=value)
                    except Exception, e:
                        logging.error("Exception occured during backup: %s"
                                      % str (e))
        except IOError, (errno, msg):
            logging.error("Cannot read file %s: %s" % (rcfile, msg))
    finally:
        f_in.close()

# Close the logging out.
logging_handler.close()

