#
# Copyright (C) 2018 Satoru SATOH <ssato@redhat.com>
# Copyright (C) 2019 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract processor module.

.. versionadded:: 0.9.5

   - Add to abstract processors such like Parsers (loaders and dumpers).
"""
from __future__ import absolute_import

import typing


CidT = str
TypeT = str
ExtensionT = str


class Processor:
    """
    Abstract processor class to provide basic implementation of some methods,
    interfaces and members.

    - _type: type indicates data types it can process
    - _priority: Priority to select it if there are others of same type
    - _extensions: File extensions of data type it can process

    .. note::
       This class ifself is not a singleton but its children classes should so
       in most cases, I think.
    """
    _cid: CidT = ''
    _type: TypeT = 'processor'
    _priority: int = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions: typing.Iterable[ExtensionT] = []

    @classmethod
    def cid(cls) -> CidT:
        """Processor class ID
        """
        return repr(cls) if not cls._cid else cls._cid

    @classmethod
    def type(cls) -> TypeT:
        """Processors' type
        """
        return cls._type

    @classmethod
    def priority(cls) -> int:
        """Processors's priority
        """
        return cls._priority

    @classmethod
    def extensions(cls) -> typing.Iterable[ExtensionT]:
        """A list of file extensions of files which this process can process.
        """
        return cls._extensions

    @classmethod
    def __eq__(cls, other) -> bool:
        return cls.cid() == other.cid()

    def __str__(self) -> str:
        return ("<Processor cid=%s, type=%s, prio=%d, "
                "extensions=%r" % (self.cid(), self.type(), self.priority(),
                                   self.extensions()))

# vim:sw=4:ts=4:et:
