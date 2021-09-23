#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions for anyconfig.api."""
import typing

if typing.TYPE_CHECKING:
    from .. import ioinfo


def are_same_file_types(objs: typing.List['ioinfo.IOInfo']) -> bool:
    """Test if given objects have same types (extensions)."""
    if not objs:
        return False

    ext = objs[0].extension
    return all(p.extension == ext for p in objs[1:])

# vim:sw=4:ts=4:et:
