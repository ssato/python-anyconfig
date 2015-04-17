#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""anyconfig module initialization before any other things.
"""
import logging
import anyconfig.compat

# See: "Configuring Logging for a Library" in python standard logging howto,
# e.g. https://docs.python.org/2/howto/logging.html#library-config.
LOGGER = logging.getLogger("anyconfig")
LOGGER.addHandler(anyconfig.compat.NullHandler())

# vim:sw=4:ts=4:et:
