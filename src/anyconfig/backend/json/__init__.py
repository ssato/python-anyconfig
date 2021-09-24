#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Backend modules to load and dump JSON data.

- std.json: python standard JSON support library [default]
- simplejson: https://github.com/simplejson/simplejson

Changelog:

.. versionchanged:: 0.9.8

   - Started to split JSON support modules
"""
from . import default
from ..base import ParserClssT


Parser = default.Parser  # To keep backward compatibility.
PARSERS: ParserClssT = [Parser]

try:
    from .simplejson import Parser as SimpleJsonParser
    PARSERS.append(SimpleJsonParser)
except ImportError:
    pass

# vim:sw=4:ts=4:et:
