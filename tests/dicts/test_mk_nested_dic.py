#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
import anyconfig.dicts as TT

from . import common


class TestCase(common.TestCase):
    kind = 'mk_nested_dic'
    pattern = '*.*'
    ordered = False

    def test_mk_nested_dic(self):
        for data in self.each_data():
            val = data.query  # diversion.
            self.assertEqual(
                TT.mk_nested_dic(data.inp, val, **data.opts),
                data.exp
            )

# vim:sw=4:ts=4:et:
