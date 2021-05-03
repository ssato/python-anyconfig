#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""JSON backends:

- std.json: python standard JSON support library [default]
- simplejson: https://github.com/simplejson/simplejson

Changelog:

.. versionchanged:: 0.9.8

   - Started to split JSON support modules
"""
import typing

import anyconfig.backend.base
from . import default


ParserTVar = typing.TypeVar('ParserTVar', bound=anyconfig.backend.base.Parser)

Parser = default.Parser  # To keep backward compatibility.
PARSERS: typing.List[ParserTVar] = [Parser]

try:
    from ._simplejson import Parser as SimpleJsonParser
    PARSERS.append(SimpleJsonParser)
except ImportError:
    pass

# vim:sw=4:ts=4:et:
