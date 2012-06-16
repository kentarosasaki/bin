#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import time


def logging_config(conffile):
    # Logging to a file done here
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logging_formatter = logging.Formatter(
                        '%(asctime)s %(levelname)s %(name)s %(message)s')
    logging_handler = logging.handlers.TimedRotatingFileHandler(
                      filename=os.path.join("log", conffile),
                      when='D',
                      backupCount=7)
    logging_handler.setFormatter(logging_formatter)
    logging_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(logging_handler)


