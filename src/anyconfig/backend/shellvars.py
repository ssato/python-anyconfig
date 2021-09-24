#
# Copyright (C) 2016 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""A simple backend module to load and dump files contain shell variables.

- Format to support: Simple shell variables' definitions w/o any shell variable
  expansions nor complex shell statements such as conditionals, etc.
- Requirements: None (built-in)
- Development Status :: 4 - Beta
- Limitations: Currently, it only supports a varialbe defined in a line.
- Special options: None

Changelog:

.. versionadded:: 0.7.0

   - Added an experimental parser for simple shelll vars' definitions w/o shell
     variable expansions nor complex shell statements like conditionals.
"""
import itertools
import os
import re
import warnings

from . import base


def _parseline(line):
    """Parse a line contains shell variable definition.

    :param line: A string to parse, must not start with '#' (comment)
    :return: A tuple of (key, value), both key and value may be None
    """
    match = re.match(
        r'^\s*(export)?\s*(\S+)=(?:(?:'
        r"(?:\"(.*[^\\])\")|(?:'(.*[^\\])')|"
        r"(?:([^\"'#\s]+)))?)\s*#*",
        line
    )
    if not match:
        warnings.warn(f'Invalid line found: {line}', SyntaxWarning)
        return (None, None)

    tpl = match.groups()
    vals = list(itertools.dropwhile(lambda x: x is None, tpl[2:]))
    return (tpl[1], vals[0] if vals else '')


def load(stream, container=dict):
    """Load shell variable definitions data from ``stream``.

    :param stream: A file or file like object
    :param container:
        Factory function to create a dict-like object to store properties
    :return: Dict-like object holding shell variables' definitions
    """
    ret = container()

    for line in stream:
        line = line.rstrip()
        if line is None or not line:
            continue

        (key, val) = _parseline(line)
        if key is None:
            warnings.warn(f'Empty val in the line: {line}', SyntaxWarning)
            continue

        ret[key] = val

    return ret


class Parser(base.StreamParser):
    """Parser for Shell variable definition files."""

    _cid = 'shellvars'
    _type = 'shellvars'
    _extensions = ['sh']
    _ordered = True
    _dict_opts = ['ac_dict']

    def load_from_stream(self, stream, container, **kwargs):
        """Load config from given file like object ``stream``.

        :param stream:
            A file or file like object of shell scripts define shell variables
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return load(stream, container=container)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """Dump config dat ``cnf`` to a file or file-like object ``stream``.

        :param cnf: Shell variables data to dump
        :param stream: Shell script file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        for key, val in cnf.items():
            stream.write(f"{key}='{val}'{os.linesep}")

# vim:sw=4:ts=4:et:
