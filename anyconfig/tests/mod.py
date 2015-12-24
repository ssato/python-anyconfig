#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anyconfig as TT
import anyconfig.tests.common


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_dump_and_load(self):
        obj = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))
        obj_path = os.path.join(self.workdir, "a.json")

        TT.dump(obj, obj_path)
        self.assertTrue(os.path.exists(obj_path))

        obj1 = TT.load(obj_path)

        self.assertEqual(obj1["name"], obj["name"])
        self.assertEqual(obj1["a"], obj["a"])
        self.assertEqual(obj1["b"]["b"], obj["b"]["b"])
        self.assertEqual(obj1["b"]["c"], obj["b"]["c"])

    def test_20_dump_and_multi_load(self):
        obja = dict(name="a", a=1, b=dict(b=[0, 1], c="C"))
        objb = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        TT.dump(obja, a_path)
        self.assertTrue(os.path.exists(a_path))

        TT.dump(objb, b_path)
        self.assertTrue(os.path.exists(b_path))

        obja1 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_DICTS)

        self.assertEqual(obja1["name"], obja["name"])
        self.assertEqual(obja1["a"], objb["a"])
        self.assertEqual(obja1["b"]["b"], objb["b"]["b"])
        self.assertEqual(obja1["b"]["c"], obja["b"]["c"])
        self.assertEqual(obja1["b"]["d"], objb["b"]["d"])

        obja2 = TT.multi_load([a_path, b_path], ac_merge=TT.MS_DICTS_AND_LISTS)

        self.assertEqual(obja2["name"], obja["name"])
        self.assertEqual(obja2["a"], objb["a"])
        self.assertEqual(obja2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEqual(obja2["b"]["c"], obja["b"]["c"])
        self.assertEqual(obja2["b"]["d"], objb["b"]["d"])

# vim:sw=4:ts=4:et:
