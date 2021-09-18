#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
r"""test cases for anyconfig.utils.
"""
import collections
import unittest
import typing

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

# vim:sw=4:ts=4:et:
