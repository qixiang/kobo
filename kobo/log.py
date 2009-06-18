# -*- coding: utf-8 -*-


import os
import logging
import logging.handlers


__all__ = (
    "BRIEF_LOG_FORMAT",
    "VERBOSE_LOG_FORMAT",
    "add_stderr_logger",
    "add_file_logger",
    "add_rotating_file_logger",
)


BRIEF_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(message)s"
VERBOSE_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] {%(process)5d} %(name)s:%(lineno)4d %(message)s"


def add_stderr_logger(logger, log_level=None, format=None):
    """Add a stderr logger to the logger."""
    log_level = log_level or logging.DEBUG
    format = format or BRIEF_LOG_FORMAT
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))
    handler.setLevel(log_level)
    logger.addHandler(handler)


def add_file_logger(logger, logfile, log_level=None, format=None, mode="a"):
    """Add a file logger to the logger."""
    log_level = log_level or logging.DEBUG
    format = format or BRIEF_LOG_FORMAT

    # touch the logfile
    if not os.path.exists(logfile):
        try:
            fo = open(logfile, "w")
            fo.close()
        except (ValueError, IOError):
            return

    # is the logfile really a file?
    if not os.path.isfile(logfile):
        return

    # check if the logfile is writable
    if not os.access(logfile, os.W_OK):
        return

    handler = logging.FileHandler(logfile, mode=mode)
    handler.setFormatter(logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))
    handler.setLevel(log_level)
    logger.addHandler(handler)


def add_rotating_file_logger(logger, logfile, log_level=None, format=None, mode="a"):
    """Add a rotating file logger to the logger."""
    log_level = log_level or logging.DEBUG
    format = format or BRIEF_LOG_FORMAT

    # touch the logfile
    if not os.path.exists(logfile):
        try:
            fo = open(logfile, "w")
            fo.close()
        except (ValueError, IOError):
            return

    # is the logfile really a file?
    if not os.path.isfile(logfile):
        return

    # check if the logfile is writable
    if not os.access(logfile, os.W_OK):
        return

    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*(1024**2), backupCount=5, mode=mode)
    handler.setFormatter(logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))
    handler.setLevel(log_level)
    logger.addHandler(handler)