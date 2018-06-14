#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
Abstract processor module will be base for parsers (loaders and dumpers), etc.
"""
from __future__ import absolute_import

import pkg_resources


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

# vim:sw=4:ts=4:et:
