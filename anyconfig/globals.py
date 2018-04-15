#
# Copyright (C) 2013 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""anyconfig globals.
"""
import anyconfig.init


PACKAGE = "anyconfig"
AUTHOR = "Satoru SATOH <ssato@redhat.com>"
VERSION = "0.9.4"

LOGGER = anyconfig.init.getLogger(PACKAGE)


class UnknownParserTypeError(RuntimeError):
    """Raise if no parsers were found for given type."""
    def __init__(self, forced_type):
        msg = "No parser found for type '%s'" % forced_type
        super(UnknownParserTypeError, self).__init__(msg)


class UnknownFileTypeError(RuntimeError):
    """Raise if not parsers were found for given file path."""
    def __init__(self, path):
        msg = "No parser found for file '%s'" % path
        super(UnknownFileTypeError, self).__init__(msg)

# vim:sw=4:ts=4:et:
