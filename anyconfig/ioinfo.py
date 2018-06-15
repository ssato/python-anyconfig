#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=invalid-name
r"""Functions for value objects represent inputs and outputs.

.. versionadded:: 0.9.5

- Add functions to make and process input and output object holding some
  attributes like input and output type (path, stream or pathlib.Path object),
  path, opener, etc.
"""
from __future__ import absolute_import

import anyconfig.utils

from anyconfig.globals import (
    IOInfo, IOI_NONE, IOI_PATH_STR, IOI_PATH_OBJ, IOI_STREAM,
    UnknownFileTypeError, UnknownParserTypeError
)


def guess_io_type(obj):
    """Guess input or output type of ``obj``.

    :param obj: a path string, a pathlib.Path or a file / file-like object
    :return: IOInfo type defined in anyconfig.globals.IOI_TYPES

    >>> apath = "/path/to/a_conf.ext"
    >>> assert guess_io_type(apath) == IOI_PATH_STR

    >>> from anyconfig.compat import pathlib
    >>> if pathlib is not None:
    ...     assert guess_io_type(pathlib.Path(apath)) == IOI_PATH_OBJ
    >>> assert guess_io_type(open(__file__)) == IOI_STREAM
    """
    if obj is None:
        return IOI_NONE
    elif anyconfig.utils.is_path(obj):
        return IOI_PATH_STR
    elif anyconfig.utils.is_path_obj(obj):
        return IOI_PATH_OBJ

    return IOI_STREAM


def inspect_io_obj(obj):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object

    :return: A tuple of (objtype, objpath, objopener)
    :raises: UnknownFileTypeError
    """
    itype = guess_io_type(obj)

    if itype == IOI_PATH_STR:
        ipath = anyconfig.utils.normpath(obj)
        opener = open
    elif itype == IOI_PATH_OBJ:
        ipath = anyconfig.utils.normpath(obj.as_posix())
        opener = obj.open
    elif itype == IOI_STREAM:
        ipath = anyconfig.utils.get_path_from_stream(obj)
        opener = anyconfig.utils.noop
    elif itype == IOI_NONE:
        ipath = None
        opener = anyconfig.utils.noop
    else:
        raise UnknownFileTypeError("%r" % obj)

    return (itype, ipath, opener)


def find_by_fileext(fileext, cps_by_ext):
    """
    :param fileext: File extension
    :param cps_by_ext: A list of pairs (file_extension, [processor_class])

    :return: Most appropriate processor class to process given file

    >>> from anyconfig.backends import _PARSERS_BY_EXT as cps
    >>> find_by_fileext("json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_fileext("ext_should_not_be_found", cps) is None
    True
    """
    return next((psrs[-1] for ext, psrs in cps_by_ext if ext == fileext),
                None)


def find_by_filepath(filepath, cps_by_ext):
    """
    :param filepath: Path to the file to find out processor to process it
    :param cps_by_ext: A list of pairs (file_extension, [processor_class])

    :return: Most appropriate processor class to process given file

    >>> from anyconfig.backends import _PARSERS_BY_EXT as cps
    >>> find_by_filepath("/a/b/c/x.json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_filepath("/path/to/a.ext_should_not_be_found", cps) is None
    True
    """
    fileext = anyconfig.utils.get_file_extension(filepath)
    return find_by_fileext(fileext, cps_by_ext)


def find_by_type(cptype, cps_by_type):
    """
    :param cptype: Config file's type
    :param cps_by_type: A list of pairs, (processor_type, [processor_class])

    :return: Most appropriate processor class to process given type or None

    >>> from anyconfig.backends import _PARSERS_BY_TYPE as cps
    >>> find_by_type("json", cps)
    <class 'anyconfig.backend.json.Parser'>
    >>> find_by_type("missing_type", cps) is None
    True
    """
    return next((psrs[-1] or None for t, psrs in cps_by_type if t == cptype),
                None)


def find_processor(ipath, cps_by_ext, cps_by_type, forced_type=None):
    """
    :param ipath: file path
    :param cps_by_ext: A list of pairs (file_extension, [processor_cls])
    :param cps_by_type: A list of pairs (processor_type, [processor_cls])
    :param forced_type: Forced processor type or processor object

    :return: Instance of processor class appropriate for the input `ipath`
    :raises: ValueError, UnknownParserTypeError, UnknownFileTypeError
    """
    if (ipath is None or not ipath) and forced_type is None:
        raise ValueError("ipath or forced_type must be some value")

    if isinstance(forced_type, anyconfig.backend.base.Parser):
        return forced_type

    if forced_type is None:
        processor = find_by_filepath(ipath, cps_by_ext)
        if processor is None:
            raise UnknownFileTypeError(ipath)

        return processor()

    processor = find_by_type(forced_type, cps_by_type)
    if processor is None:
        raise UnknownParserTypeError(forced_type)

    return processor()


def make(obj, cps_by_ext, cps_by_type, forced_type=None):
    """
    :param obj: a path string, a pathlib.Path or a file / file-like object
    :param cps_by_ext: A list of pairs (file_extension, [processor_cls])
    :param cps_by_type: A list of pairs (processor_type, [processor_cls])
    :param forced_type: Forced configuration processor type

    :return:
        Namedtuple object represents a kind of input object such as a file /
        file-like object, path string or pathlib.Path object

    :raises: ValueError, UnknownParserTypeError, UnknownFileTypeError
    """
    if anyconfig.utils.is_ioinfo(obj):
        return obj

    if (obj is None or not obj) and forced_type is None:
        raise ValueError("obj or forced_type must be some value")

    (itype, ipath, opener) = inspect_io_obj(obj)
    psr = find_processor(ipath, cps_by_ext, cps_by_type,
                         forced_type=forced_type)

    return IOInfo(src=obj, type=itype, path=ipath, processor=psr,
                  opener=opener)

# vim:sw=4:ts=4:et:
