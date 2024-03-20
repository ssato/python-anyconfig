#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import warnings

import anyconfig.api._load as TT

from anyconfig.api import UnknownProcessorTypeError

from . import common


class TestCase(common.TestCase):

    def test_loads(self):
        for data in self.each_data():
            self.assertEqual(
                TT.loads(data.inp, **data.opts),
                data.exp,
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_loads_intentional_failures(self):
        for data in self.each_data():
            with self.assertRaises(AssertionError):
                self.assertEqual(TT.loads(data.inp, **data.opts), {})

    def test_loads_failure_ac_parser_was_not_given(self):
        for data in self.each_data():
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                self.assertEqual(TT.loads(data.inp), None)
                self.assertEqual(len(warns), 1)
                self.assertTrue(issubclass(warns[-1].category, UserWarning))
                self.assertTrue(
                    'ac_parser was not given but' in str(warns[-1].message)
                )

    def test_loads_failure_invalid_ac_parser_was_given(self):
        for data in self.each_data():
            with self.assertRaises(UnknownProcessorTypeError):
                self.assertEqual(
                    TT.loads(data.inp, ac_parser='invalid_id'),
                    None
                )

# vim:sw=4:ts=4:et:
