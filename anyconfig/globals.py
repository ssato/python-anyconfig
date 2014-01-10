#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""anyconfig globals.
"""
import logging


AUTHOR = 'Satoru SATOH <ssat@redhat.com>'
VERSION = "0.0.3.11"

_LOGGING_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"


def get_logger(name="anyconfig", log_format=_LOGGING_FORMAT,
               level=logging.WARNING):
    """
    Initialize custom logger.
    """
    logging.basicConfig(level=level, format=log_format)
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(handler)

    return logger


LOGGER = get_logger()

# vim:sw=4:ts=4:et:
