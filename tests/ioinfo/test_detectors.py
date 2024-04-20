#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,consider-using-with
r"""test cases for anyconfig.ioinfo.detectors.
"""
from __future__ import annotations

import pathlib
import unittest
import typing

import anyconfig.ioinfo
import anyconfig.ioinfo.detectors as TT

if typing.TYPE_CHECKING:
    import collections.abc


class TestCase(unittest.TestCase):

    def _run(
        self, target_fn: collections.abc.Callable[..., typing.Any],
        ies: collections.abc.Iterable[tuple[typing.Any, bool]]
    ) -> None:
        for inp, exp in ies:
            meth = self.assertTrue if exp else self.assertFalse
            meth(target_fn(inp), f'input: {inp!r}, expected: {exp!r}')

    def test_is_path_str(self):
        self._run(
            TT.is_path_str,
            ((None, False),
             ('/tmp/t.xt', True),
             (0, False),
             (pathlib.Path(__file__), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), False),
             )
        )

    def test_is_path_obj(self):
        self._run(
            TT.is_path_obj,
            ((None, False),
             (__file__, False),
             (pathlib.Path(__file__), True),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), False),
             )
        )

    def test_is_io_stream(self):
        self._run(
            TT.is_io_stream,
            ((None, False),
             (__file__, False),
             (pathlib.Path(__file__), False),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), True),
             (anyconfig.ioinfo.make(__file__), False),
             )
        )

    def test_is_ioinfo(self):
        self._run(
            TT.is_ioinfo,
            ((None, False),
             (__file__, False),
             (pathlib.Path(__file__), False),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), True),
             (anyconfig.ioinfo.make(open(__file__)), True),
             )
        )

    def test_is_stream(self):
        self._run(
            TT.is_stream,
            ((None, False),
             (__file__, False),
             (pathlib.Path(__file__), False),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), False),
             (anyconfig.ioinfo.make(open(__file__)), True),
             )
        )

# vim:sw=4:ts=4:et:
