#
# Copyright (C) 2016 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
Parser for simple Shell vars' definitions.

.. versionadded:: 0.7.0
   Added an experimental parser for simple shelll vars' definitions w/o shell
   variable expansions nor complex shell statements like conditionals.

- Format to support: Simple shell variables' definitions w/o any shell variable
  expansions nor complex shell statements such as conditionals, etc.
- Requirements: None (built-in)
- Limitations: Currently, it only supports a varialbe defined in a line.
- Special options: None
"""
from __future__ import absolute_import

import logging
import itertools
import re

import anyconfig.backend.base


LOGGER = logging.getLogger(__name__)


def _parseline(line):
    """
    Parse a line contains shell variable definition.

    :param line: A string to parse, must not start with '#' (comment)
    :return: A tuple of (key, value), both key and value may be None

    >>> _parseline("aaa=")
    ('aaa', '')
    >>> _parseline("aaa=bbb")
    ('aaa', 'bbb')
    >>> _parseline("aaa='bb b'")
    ('aaa', 'bb b')
    >>> _parseline('aaa="bb#b"')
    ('aaa', 'bb#b')
    >>> _parseline('aaa="bb\\"b"')
    ('aaa', 'bb"b')
    >>> _parseline("aaa=bbb   # ccc")
    ('aaa', 'bbb')
    """
    match = re.match(r"^\s*(\S+)=(?:(?:"
                     r"(?:\"(.*[^\\])\")|(?:'(.*[^\\])')|"
                     r"(?:([^\"'#\s]+)))?)\s*#*", line)
    if not match:
        LOGGER.warning("Invalid line found: %s", line)
        return (None, None)

    tpl = match.groups()
    vals = list(itertools.dropwhile(lambda x: x is None, tpl[1:]))
    return (tpl[0], vals[0] if vals else '')


def load(stream, to_container=dict):
    """
    Load and parse a file or file-like object `stream` provides simple shell
    variables' definitions.

    :param stream: A file or file like object
    :param to_container:
        Factory function to create a dict-like object to store properties
    :return: Dict-like object holding shell variables' definitions

    >>> from anyconfig.compat import StringIO as to_strm
    >>> load(to_strm(''))
    {}
    >>> load(to_strm("# "))
    {}
    >>> load(to_strm("aaa="))
    {'aaa': ''}
    >>> load(to_strm("aaa=bbb"))
    {'aaa': 'bbb'}
    >>> load(to_strm("aaa=bbb # ..."))
    {'aaa': 'bbb'}
    """
    ret = to_container()

    for line in stream.readlines():
        line = line.rstrip()
        if line is None or not line:
            continue

        (key, val) = _parseline(line)
        if key is None:
            LOGGER.warning("Empty val in the line: %s", line)
            continue

        ret[key] = val

    return ret


class Parser(anyconfig.backend.base.FromStreamLoader,
             anyconfig.backend.base.ToStreamDumper):
    """
    Parser for Java properties files.
    """
    _type = "shellvars"

    def load_from_stream(self, stream, to_container, **kwargs):
        """
        Load config from given file like object `stream`.

        :param stream: A file or file like object of Java properties files
        :param to_container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return load(stream, to_container=to_container)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config `cnf` to a file or file-like object `stream`.

        :param cnf: Java properties config data to dump
        :param stream: Java properties file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        for key, val in anyconfig.compat.iteritems(cnf):
            stream.write("%s='%s'\n" % (key, val))

# vim:sw=4:ts=4:et:
