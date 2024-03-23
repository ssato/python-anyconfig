#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=consider-using-with
"""Module to provide backward compatibility for plugins."""
from __future__ import annotations

import pathlib
import typing


class BinaryFilesMixin:
    """Mixin class to open configuration files as a binary data."""

    _open_flags: typing.Tuple[str, str] = ("rb", "wb")

    @classmethod
    def ropen(cls, filepath, **kwargs):
        """Open ``filepath`` with read only mode.

        :param filepath: Path to file to open to read data
        """
        return pathlib.Path(filepath).open(  # noqa: SIM115
            cls._open_flags[0], **kwargs
        )

    @classmethod
    def wopen(cls, filepath, **kwargs):
        """Open ``filepath`` with write mode.

        :param filepath: Path to file to open to write data to
        """
        return pathlib.Path(filepath).open(  # noqa: SIM115
            cls._open_flags[1], **kwargs
        )
