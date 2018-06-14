#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
Abstract processor module will be base for parsers (loaders and dumpers), etc.
"""
from __future__ import absolute_import

import operator
import pkg_resources

import anyconfig.compat


class Processor(object):
    """
    Abstract processor to provide basic implementation of some methods,
    interfaces and members.

    - _type: type indicates data types it can process
    - _priority: Priority to select it if there are others of same type
    - _extensions: File extensions of data type it can process
    """
    _type = None
    _priority = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions = []

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
        """File extensions which this process can process
        """
        return cls._extensions


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


def list_processors_by_type(prs):
    """
    :param prs: A list of instances of :class:`Processor`
    :return: List (generator) of (processor_type, [processor_cls])
    """
    return ((t, sorted(ps, key=operator.methodcaller("priority"))) for t, ps
            in anyconfig.utils.groupby(prs, operator.methodcaller("type")))


def _ext_proc_tpls_to_procs(xps):
    """List processors by each priority.

    :param xps: A list of (file_extension, processor_cls)
    :return: List of [processor_cls]
    """
    return sorted((operator.itemgetter(1)(xp) for xp in xps),
                  key=operator.methodcaller("priority"))


def list_processors_by_ext(prs):
    """
    :param prs: A list of instances of :class:`Processor`
    :return: List (generator) of (file_extension, [processor_cls])
    """
    ps_by_ext = anyconfig.utils.concat(([(x, p) for x in p.extensions()] for p
                                        in prs))  # [(ext, proc_cls)]

    return ((x, _ext_proc_tpls_to_procs(xps)) for x, xps
            in anyconfig.utils.groupby(ps_by_ext, operator.itemgetter(0)))


def list_types(prs):
    """List types that any processors can process them are available.
    """
    return sorted(set(next(anyconfig.compat.izip(*prs))))

# vim:sw=4:ts=4:et:
