#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""test cases for anyconfig.utils.
"""
import collections
import pathlib
import unittest
import typing

import anyconfig.ioinfo
import anyconfig.utils.detectors as TT


class TestCase(unittest.TestCase):

    def _run(self,
             target_fn: typing.Callable[..., typing.Any],
             ies: typing.Iterable[typing.Tuple[typing.Any, bool]]
             ) -> None:
        for inp, exp in ies:
            meth = self.assertTrue if exp else self.assertFalse
            meth(target_fn(inp), f'input: {inp!r}, expected: {exp!r}')

    def test_is_iterable(self):
        self._run(
            TT.is_iterable,
            (
             (None, False),
             ([], True), ((), True),
             ((str(x) for x in range(10)), True),
             ([str(x) for x in range(10)], True),
             ('abc', False), (0, False), ({}, False),
             )
        )

    def test_is_list_like(self):
        self._run(
            TT.is_list_like,
            (
             (None, False),
             (0, False),
             ('aaa', False),
             ({}, False),
             ([], True), ((), True),
             ((str(x) for x in range(10)), True),
             ([str(x) for x in range(10)], True),
             )
        )

    def test_is_dict_like(self):
        self._run(
            TT.is_dict_like,
            (
             (None, False),
             (0, False),
             ('aaa', False),
             ([], False),
             ((1, ), False),
             (collections.namedtuple('Point', ('x', 'y'))(1, 2), False),
             ({}, True),
             (collections.OrderedDict((('a', 1), ('b', 2))), True),
             )
        )

    def test_is_path(self):
        self._run(
            TT.is_path,
            (
             (None, False),
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
            (
             (None, False),
             (__file__, False),
             (pathlib.Path(__file__), True),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), False),
             )
        )

    def test_is_file_stream(self):
        self._run(
            TT.is_file_stream,
            (
             (None, False),
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
            (
             (None, False),
             (__file__, False),
             (pathlib.Path(__file__), False),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), True),
             (anyconfig.ioinfo.make(open(__file__)), True),
             )
        )

    def test_is_path_like_object(self):
        self._run(
            TT.is_path_like_object,
            (
             (False, False),
             (None, False),
             (__file__, True),
             (pathlib.Path(__file__), True),
             (str(pathlib.Path(__file__).resolve()), True),
             (open(__file__), True),
             (anyconfig.ioinfo.make(__file__), True),
             (anyconfig.ioinfo.make(open(__file__)), True),
             )
        )

    def test_is_paths(self):
        self._run(
            TT.is_paths,
            (
             (False, False),
             (None, False),
             (__file__, False),
             (pathlib.Path(__file__), False),
             (str(pathlib.Path(__file__).resolve()), False),
             (open(__file__), False),
             (anyconfig.ioinfo.make(__file__), False),
             (anyconfig.ioinfo.make(open(__file__)), False),
             ('/tmp/*.txt', True),
             (pathlib.Path('/tmp/*.txt'), True),
             ((__file__, ), True),
             ((pathlib.Path(__file__), ), True),
             ((str(pathlib.Path(__file__).resolve()), ), True),
             ((open(__file__), ), True),
             ((anyconfig.ioinfo.make(__file__), ), True),
             ((anyconfig.ioinfo.make(open(__file__)), ), True),
             )
        )

# vim:sw=4:ts=4:et:
