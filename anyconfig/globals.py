#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import logging


AUTHOR = 'Satoru SATOH <ssat@redhat.com>'
VERSION = "0.0.3.10"

_LOGGING_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"


def getLogger(name="anyconfig", format=_LOGGING_FORMAT,
              level=logging.WARNING, **kwargs):
    """
    Initialize custom logger.
    """
    logging.basicConfig(level=level, format=format)
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler()

    return logger


LOGGER = getLogger()

# vim:sw=4:ts=4:et:
