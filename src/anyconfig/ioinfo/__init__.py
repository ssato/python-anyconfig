#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""ioinfo module to provide objects wrap pathlib.Path and io objects.

.. versionchanged:: 0.10.1

- simplify inspect_io_obj and make; detect type in make, remove the member
  opener from ioinfo object, etc.

.. versionadded:: 0.9.5

- Add functions to make and process input and output object holding some
  attributes like input and output type (path, stream or pathlib.Path object),
  path, opener, etc.
"""
from .main import make

__all__ = [
    'make',
]

# vim:sw=4:ts=4:et:
