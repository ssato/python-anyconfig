#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh @ gmmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""ioinfo.main to provide internal APIs used from other modules.
"""
import pathlib
import typing

from .. import common, utils
from .utils import guess_io_type, inspect_io_obj


def make(obj: typing.Any) -> common.IOInfo:
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if utils.is_ioinfo(obj):
        return obj

    itype = guess_io_type(obj)

    if itype == common.IOI_PATH_STR:
        obj = pathlib.Path(obj)
        itype = common.IOI_PATH_OBJ

    (ipath, ext) = inspect_io_obj(obj, itype)
    return common.IOInfo(src=obj, type=itype, path=ipath, extension=ext)

# vim:sw=4:ts=4:et:
