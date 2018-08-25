#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
r"""Abstract processor module.

.. versionadded:: 0.9.5

   - Add to abstract processors such like Parsers (loaders and dumpers).
"""
from __future__ import absolute_import

import operator
import pkg_resources

import anyconfig.compat
import anyconfig.utils

from anyconfig.globals import (
    UnknownProcessorTypeError, UnknownFileTypeError
)


def _load_plugins_itr(pgroup, safe=True):
    """
    .. seealso:: the doc of :func:`load_plugins`
    """
    for res in pkg_resources.iter_entry_points(pgroup):
        try:
            yield res.load()
        except ImportError:
            if safe:
                continue
            raise


def load_plugins(pgroup, safe=True):
    """
    :param pgroup: A string represents plugin type, e.g. anyconfig_backends
    :param safe: Do not raise ImportError during load if True
    :raises: ImportError
    """
    return list(_load_plugins_itr(pgroup, safe=safe))


class Processor(object):
    """
    Abstract processor class to provide basic implementation of some methods,
    interfaces and members.

    - _type: type indicates data types it can process
    - _priority: Priority to select it if there are others of same type
    - _extensions: File extensions of data type it can process

    .. note:: This class is not a singleton but its children may be so.
    """
    _id = None
    _type = None
    _priority = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions = []

    @classmethod
    def id(cls):
        """Processors' ID
        """
        return repr(cls) if cls._id is None else cls._id

    @classmethod
    def type(cls):
        """Processors' type
        """
        return cls._type

    @classmethod
    def priority(cls):
        """Processors's priority
        """
        return cls._priority

    @classmethod
    def extensions(cls):
        """A list of extensions of files which this process can process.
        """
        return cls._extensions

    def __eq__(self, other):
        return isinstance(other, Processor) and self.id() == other.id()


def find_with_pred(predicate, prs):
    """
    :param predicate: any callable to filter results
    :param prs: A list of :class:`Processor` classes
    :return: Most appropriate processor class or None

    >>> class A(Processor):
    ...    _type = "json"
    ...    _extensions = ['json', 'js']
    >>> class A2(A):
    ...    _priority = 99  # Higher priority than A.
    >>> class B(Processor):
    ...    _type = "yaml"
    ...    _extensions = ['yaml', 'yml']
    >>> prs = [A, A2, B]

    >>> find_with_pred(lambda p: 'js' in p.extensions(), prs)
    <class 'anyconfig.processors.A2'>
    >>> find_with_pred(lambda p: 'yml' in p.extensions(), prs)
    <class 'anyconfig.processors.B'>
    >>> x = find_with_pred(lambda p: 'xyz' in p.extensions(), prs)
    >>> assert x is None

    >>> find_with_pred(lambda p: p.type() == "json", prs)
    <class 'anyconfig.processors.A2'>
    >>> find_with_pred(lambda p: p.type() == "yaml", prs)
    <class 'anyconfig.processors.B'>
    >>> x = find_with_pred(lambda p: p.type() == "x", prs)
    >>> assert x is None
    """
    _prs = sorted((p for p in prs if predicate(p)),
                  key=operator.methodcaller("priority"), reverse=True)
    if _prs:
        return _prs[0]  # Found.

    return None


def find_by_type(ptype, prs):
    """
    :param ptype: Type of the data to process
    :param prs: A list of :class:`Processor` classes
    :return:
        Most appropriate processor class to process files of given data type
        `ptype` or None
    :raises: UnknownProcessorTypeError
    """
    def pred(pcls):
        """Predicate"""
        return pcls.type() == ptype

    processor = find_with_pred(pred, prs)
    if processor is None:
        raise UnknownProcessorTypeError(ptype)

    return processor


def find_by_fileext(fileext, prs):
    """
    :param fileext: File extension
    :param prs: A list of :class:`Processor` classes
    :return:
        Most appropriate processor class to process files with given
        extentsions or None
    :raises: UnknownFileTypeError
    """
    def pred(pcls):
        """Predicate"""
        return fileext in pcls.extensions()

    return find_with_pred(pred, prs)


def find_by_filepath(filepath, prs):
    """
    :param filepath: Path to the file to find out processor to process it
    :param cps_by_ext: A list of processor classes

    :return: Most appropriate processor class to process given file
    :raises: UnknownFileTypeError
    """
    fileext = anyconfig.utils.get_file_extension(filepath)
    processor = find_by_fileext(fileext, prs)
    if processor is None:
        raise UnknownFileTypeError(fileext)

    return processor


def find(ipath, prs, forced_type=None):
    """
    :param ipath: file path
    :param prs: A list of processor classes
    :param forced_type: Forced processor type or processor object itself

    :return: an instance of processor class appropriate to process `ipath` data
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if (ipath is None or not ipath) and forced_type is None:
        raise ValueError("file path or file type must be given")

    if forced_type is None:
        processor = find_by_filepath(ipath, prs)
        if processor is None:
            raise UnknownFileTypeError(ipath)

        return processor()

    elif isinstance(forced_type, Processor):
        return forced_type

    elif type(forced_type) == type(Processor):
        return forced_type()

    processor = find_by_type(forced_type, prs)
    if processor is None:
        raise UnknownProcessorTypeError(forced_type)

    return processor()

# vim:sw=4:ts=4:et:
