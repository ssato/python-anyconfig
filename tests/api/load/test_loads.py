#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.api._load as TT

from .single_load.common import BaseTestCase


class TestCase(BaseTestCase):

    def test_loads(self):
        for inp, exp in self.ies:
            inp_s = inp.read_text()
            self.assertEqual(TT.loads(inp_s, ac_parser='json'), exp)

    def test_loads_failures(self):
        for inp, _exp in self.ies:
            inp_s = inp.read_text()
            self.assertEqual(TT.loads(inp_s), None)

# vim:sw=4:ts=4:et:
