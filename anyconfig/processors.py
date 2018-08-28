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
import anyconfig.ioinfo
import anyconfig.models.processor

from anyconfig.globals import (
    UnknownProcessorTypeError, UnknownFileTypeError, IOInfo
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


def find_with_pred(predicate, prs):
    """
    :param predicate: any callable to filter results
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return: Most appropriate processor class or None

    >>> class A(anyconfig.models.processor.Processor):
    ...    _type = "json"
    ...    _extensions = ['json', 'js']
    >>> class A2(A):
    ...    _priority = 99  # Higher priority than A.
    >>> class B(anyconfig.models.processor.Processor):
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


def find_by_type(ptype, prs, cls=anyconfig.models.processor.Processor):
    """
    :param ptype:
        Type of the data to process or
        :class:`anyconfig.models.processor.Processor` class object or its
        instance
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :param cls: A class object to compare with `ptype`
    :return:
        Most appropriate processor instance to process files of given data type
        `ptype` or None
    :raises: UnknownProcessorTypeError
    """
    if isinstance(ptype, cls):
        return ptype

    elif type(ptype) == type(cls) and issubclass(ptype, cls):
        return ptype()

    def pred(pcls):
        """Predicate"""
        return pcls.type() == ptype

    processor = find_with_pred(pred, prs)
    if processor is None:
        raise UnknownProcessorTypeError(ptype)

    return processor()


def find_by_fileext(fileext, prs):
    """
    :param fileext: File extension
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :return:
        Most appropriate processor class to process files with given
        extentsions or None
    :raises: UnknownFileTypeError
    """
    def pred(pcls):
        """Predicate"""
        return fileext in pcls.extensions()

    return find_with_pred(pred, prs)


def find_by_maybe_file(obj, prs):
    """
    :param obj:
        a file path, file or file-like object, pathlib.Path object or
        `~anyconfig.globals.IOInfo` (namedtuple) object
    :param cps_by_ext: A list of processor classes

    :return:
        An instance of most appropriate processor class to process given data
    :raises: UnknownFileTypeError
    """
    if not isinstance(obj, IOInfo):
        obj = anyconfig.ioinfo.make(obj)

    processor = find_by_fileext(obj.extension, prs)
    if processor is None:
        raise UnknownFileTypeError("file extension={}".format(obj.extension))

    return processor()


def find(obj, prs, forced_type=None, cls=anyconfig.models.processor.Processor):
    """
    :param obj:
        a file path, file or file-like object, pathlib.Path object or
        `~anyconfig.globals.IOInfo` (namedtuple) object
    :param prs: A list of :class:`anyconfig.models.processor.Processor` classes
    :param forced_type: Forced processor type or processor object itself
    :param cls: A class object to compare with `forced_type` later

    :return: an instance of processor class to process `obj` data
    :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
    """
    if (obj is None or not obj) and forced_type is None:
        raise ValueError("The first argument 'obj' or the second argument "
                         "'forced_type' must be something other than "
                         "None or False.")

    if forced_type is None:
        processor = find_by_maybe_file(obj, prs)
        if processor is None:
            raise UnknownFileTypeError(obj)

        return processor

    processor = find_by_type(forced_type, prs, cls=cls)
    if processor is None:
        raise UnknownProcessorTypeError(forced_type)

    return processor


class Processors(object):
    """An abstract class of which instance holding processors.
    """
    _processors = dict()  # {<processor_class_id>: <processor_class>}
    _pgroup = None  # processor group name to load plugins

    def __init__(self, processors=None):
        """
        :param processors:
            A list of :class:`Processor` or its children class objects or None
        """
        if processors is not None:
            self.register(*processors)

        self.load_plugins()

    def register(self, *pclss):
        """
        :param pclss: A list of :class:`Processor` or its children classes
        """
        for pcls in pclss:
            if pcls.cid() not in self._processors:
                self._processors[pcls.cid()] = pcls

    def load_plugins(self):
        """Load and register pluggable processor classes internally.
        """
        if self._pgroup:
            self.register(*load_plugins(self._pgroup))

    def list(self, sort=True):
        """
        :return: A list of :class:`Processor` or its children classes
        """
        if sort:
            return sorted(self._processors.values(),
                          key=operator.methodcaller("cid"))

        return self._processors.values()

    def find_by_type(self, ptype):
        """
        :param ptype: Processor's type to find
        """
        return find_by_type(ptype, self.list(sort=False))

    def find(self, ipath, ptype=None,
             cls=anyconfig.models.processor.Processor):
        """
        :param ipath: file path
        :param ptype: Processor's type or None
        :param cls: A class object to compare with `ptype`

        :return: an instance of processor class to process `ipath` data later
        :raises: ValueError, UnknownProcessorTypeError, UnknownFileTypeError
        """
        return find(ipath, self.list(sort=False), forced_type=ptype, cls=cls)

# vim:sw=4:ts=4:et:
