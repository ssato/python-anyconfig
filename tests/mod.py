#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato@redhat.com>
# Copyright (C) 2016 - 2020 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring
import copy
import pathlib
import tempfile
import unittest

import anyconfig as TT


class TestCase(unittest.TestCase):

    obj = dict(name="a", a=1, b=dict(b=[0, 1], c='C'))

    def test_10_dump_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            obj_path = pathlib.Path(tmpdir) / 'a.json'

            TT.dump(self.obj, obj_path)
            self.assertTrue(obj_path.exists())

            obj1 = TT.load(obj_path)
            self.assertEqual(self.obj, obj1)

    def test_20_dump_and_multi_load(self):
        obj_diff = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d='D'))

        with tempfile.TemporaryDirectory() as tmpdir:
            a_path = pathlib.Path(tmpdir) / 'a.json'
            b_path = pathlib.Path(tmpdir) / 'b.json'

            TT.dump(self.obj, a_path)
            self.assertTrue(a_path.exists())

            TT.dump(obj_diff, b_path)
            self.assertTrue(b_path.exists())

            ref = copy.copy(self.obj)
            obj_1 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_DICTS)
            TT.merge(ref, obj_diff, ac_merge=TT.MS_DICTS)
            self.assertEqual(obj_1, ref)

# vim:sw=4:ts=4:et:
