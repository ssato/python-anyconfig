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
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = TT.load(a_path)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_20_dump_and_multi_load(self):
        a = dict(name="a", a=1, b=dict(b=[0, 1], c="C"))
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        TT.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        TT.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a1 = TT.multi_load([a_path, b_path], merge=TT.MS_DICTS)

        self.assertEquals(a1["name"], a["name"])
        self.assertEquals(a1["a"], b["a"])
        self.assertEquals(a1["b"]["b"], b["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])
        self.assertEquals(a1["b"]["d"], b["b"]["d"])

        a2 = TT.multi_load([a_path, b_path], merge=TT.MS_DICTS_AND_LISTS)

        self.assertEquals(a2["name"], a["name"])
        self.assertEquals(a2["a"], b["a"])
        self.assertEquals(a2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

# vim:sw=4:ts=4:et:
