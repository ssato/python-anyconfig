#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
import pathlib
import tempfile

import anyconfig.api._dump as TT

from anyconfig.api import (
    UnknownProcessorTypeError, UnknownFileTypeError
)

from . import common


class TestCase(common.BaseTestCase):

    def test_dump(self):
        with tempfile.TemporaryDirectory() as tdir:
            for data in self.each_data():
                out = pathlib.Path(tdir) / 'out.json'
                TT.dump(data.inp, out, **data.opts)
                self.assertEqual(
                    out.read_text().strip(),
                    data.exp.strip(),
                    f'{data.datadir!s}, {data.inp_path!s}'
                )

    def test_dump_intentional_failures(self):
        with tempfile.TemporaryDirectory() as tdir:
            for data in self.each_data():
                out = pathlib.Path(tdir) / 'out.json'
                TT.dump(data.inp, out, **data.opts)
                with self.assertRaises(AssertionError):
                    self.assertEqual(out.read_text().strip(), '')

    def test_dump_failure_ac_parser_was_not_given(self):
        for data in self.each_data():
            with self.assertRaises(UnknownFileTypeError):
                TT.dump(data.inp, 'dummy.txt')

    def test_dump_failure_invalid_ac_parser_was_given(self):
        for data in self.each_data():
            with self.assertRaises(UnknownProcessorTypeError):
                TT.dump(data.inp, 'dummy.json', ac_parser='invalid_id')

# vim:sw=4:ts=4:et:
