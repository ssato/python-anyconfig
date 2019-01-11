#
# Copyright (C) 2011 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# type() is used to exactly match check instead of isinstance here.
# pylint: disable=unidiomatic-typecheck
r"""JSON backends:

- std.json: python standard JSON support library
- simplejson: https://github.com/simplejson/simplejson

Changelog:

.. versionchanged:: 0.9.8

   - Started to split JSON support modules
"""
from __future__ import absolute_import
from . import default

Parser = default.Parser  # To keep backward compatibility.
PARSERS = [Parser]

try:
    from .simplejson import Parser as SimpleJsonParser
    PARSERS.append(SimpleJsonParser)
except ImportError:
    pass

# vim:sw=4:ts=4:et:
