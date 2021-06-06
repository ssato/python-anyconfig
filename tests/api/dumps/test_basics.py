#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._dump as TT

from anyconfig.api import UnknownProcessorTypeError

from . import common


class TestCase(common.BaseTestCase):

    def test_dumps(self):
        for data in self.each_data():
            self.assertEqual(
                TT.dumps(data.inp, **data.opts).strip(),
                data.exp.strip(),
                f'{data.datadir!s}, {data.inp_path!s}'
            )

    def test_dump_failure_ac_parser_was_not_given(self):
        for data in self.each_data():
            with self.assertRaises(ValueError):
                TT.dumps(data.inp)

    def test_dump_failure_invalid_ac_parser_was_given(self):
        for data in self.each_data():
            with self.assertRaises(UnknownProcessorTypeError):
                TT.dumps(data.inp, ac_parser='invalid_id')

# vim:sw=4:ts=4:et:
