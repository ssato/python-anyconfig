#
# Copyright (C) 2018 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Abstract processor module.

.. versionadded:: 0.9.5

   - Add to abstract processors such like Parsers (loaders and dumpers).
"""
import typing


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
    _cid: typing.Optional[str] = None
    _type: typing.Optional[str] = None
    _priority: int = 0   # 0 (lowest priority) .. 99  (highest priority)
    _extensions: typing.List[str] = []

    @classmethod
    def cid(cls) -> str:
        """Processor class ID
        """
        return typing.cast(
            str,
            repr(cls) if getattr(cls, "_cid", None) is None else cls._cid
        )

    @classmethod
    def type(cls) -> str:
        """Processors' type
        """
        return str(cls._type)

    @classmethod
    def priority(cls) -> int:
        """Processors's priority
        """
        return cls._priority

    @classmethod
    def extensions(cls) -> typing.List[str]:
        """A list of file extensions of files which this process can process.
        """
        return cls._extensions

    @classmethod
    def __eq__(cls, other) -> bool:
        return cls.cid() == other.cid()

    def __str__(self) -> str:
        return (
            f'<Processor cid={self.cid()}, type={self.type()}, '
            f'prio={self.priority()}, extensions={self.extensions()!r}'
        )

# vim:sw=4:ts=4:et:
