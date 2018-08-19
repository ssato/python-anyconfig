#
# Copyright (C) 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
r"""Singleton class

.. versionadded:: 0.9.8

   - Add to make a kind of manager instancne later to manage plugins.
"""
from __future__ import absolute_import
import threading


class Singleton(object):
    """Singleton utilizes __new__ special method.

    >>> class A(Singleton):
    ...     pass
    >>> class B(Singleton):
    ...     pass
    >>> (a1, a2, b1, b2) = (A(), A(), B(), B())
    >>> assert a1 is a2 and b1 is b2
    >>> assert a1 is not b1
    """
    __instance = None
    __lock = threading.RLock()

    def __new__(cls):
        if cls.__instance is None:
            cls.__lock.acquire()
            if cls.__instance is None:
                try:
                    cls.__instance = object.__new__(cls)
                finally:
                    cls.__lock.release()

        return cls.__instance

# vim:sw=4:ts=4:et:
