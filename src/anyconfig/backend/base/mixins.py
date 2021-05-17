#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=consider-using-with
r"""Basic mixin classes for anyconfig.backend.**.*.
"""
import typing


class TextFilesMixin:
    """Mixin class to open configuration files as a plain text.

    Arguments of :func:`open` is different depends on python versions.

    - python 2: https://docs.python.org/2/library/functions.html#open
    - python 3: https://docs.python.org/3/library/functions.html#open
    """
    _open_flags: typing.Tuple[str, str] = ('r', 'w')

    @classmethod
    def ropen(cls, filepath, **kwargs):
        """
        :param filepath: Path to file to open to read data
        """
        return open(filepath, cls._open_flags[0], **kwargs)

    @classmethod
    def wopen(cls, filepath, **kwargs):
        """
        :param filepath: Path to file to open to write data to
        """
        return open(filepath, cls._open_flags[1], **kwargs)


class BinaryFilesMixin(TextFilesMixin):
    """Mixin class to open binary (byte string) configuration files.
    """
    _open_flags = ('rb', 'wb')

# vim:sw=4:ts=4:et:
