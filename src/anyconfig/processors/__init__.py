#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract class provides a list of :class:`anyconfig.models.processor` class
objects, related utility functions and data types.

.. versionchanged:: 0.10.2

   - Split and re-organize the module and add some data types.

.. versionadded:: 0.9.5

   - Add to abstract processors such like Parsers (loaders and dumpers).
"""
from .common import (
    ProcT, ProcClsT, ProcClssT
)
from .processors import Processors
from .utils import (
    list_by_x, load_plugins
)

__all__ = [
    'ProcT', 'ProcClsT', 'ProcClssT',
    'Processors',
    'list_by_x', 'load_plugins',
]

# vim:sw=4:ts=4:et:
