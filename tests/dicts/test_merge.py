#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# pylint: disable=missing-docstring,invalid-name
import anyconfig.dicts as TT

from .. import base
from . import common


class TestCase(common.TestCase):
    kind = 'merge'

    def test_merge(self):
        for data in self.each_data():
            upd = base.load_data(data.scm, ordered=True)  # diversion.
            TT.merge(data.inp, upd, **data.opts)
            self.assertEqual(data.inp, data.exp, data)

    def test_merge_with_a_dict(self):
        for data in self.each_data():
            upd = base.load_data(data.scm)
            TT.merge(data.inp, upd, **data.opts)
            self.assertEqual(data.inp, data.exp, data)

    def test_merge_with_an_iterable(self):
        for data in self.each_data():
            upd = base.load_data(data.scm).items()
            TT.merge(data.inp, upd, **data.opts)
            self.assertEqual(data.inp, data.exp, data)

    def test_merge_with_invalid_data(self):
        with self.assertRaises((ValueError, TypeError)):
            TT.merge(dict(a=1), 1)

# vim:sw=4:ts=4:et:
