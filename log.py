#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os


def logging_config(loggingfile):
    # Logging to a file done here
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s %(message)s')
    handler = logging.handlers.TimedRotatingFileHandler(
              filename=loggingfile,
              when='D',
              backupCount=7)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


