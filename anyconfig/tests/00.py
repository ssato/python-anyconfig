#
# Copyright (C) 2012 Satoru SATOH <ssato at redhat.com>
#
import anyconfig as A
import anyconfig.tests.common as C

import os.path
import unittest


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        pass  # C.cleanup_workdir(self.workdir)

    def test_10_dump_and_load(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = A.load(a_path)

        # FIXME: Too verbose
        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      a["a"])
        self.assertEquals(a1["b"]["b"], a["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])

    def test_20_dump_and_multi_load(self):
        a = dict(name="a", a=1, b=dict(b=[0, 1], c="C"))
        b = dict(a=2, b=dict(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        a1 = A.multi_load([a_path, b_path], merge=A.MS_DICTS)

        self.assertEquals(a1["name"],   a["name"])
        self.assertEquals(a1["a"],      b["a"])
        self.assertEquals(a1["b"]["b"], b["b"]["b"])
        self.assertEquals(a1["b"]["c"], a["b"]["c"])
        self.assertEquals(a1["b"]["d"], b["b"]["d"])

        a2 = A.multi_load([a_path, b_path], merge=A.MS_DICTS_AND_LISTS)

        self.assertEquals(a2["name"],   a["name"])
        self.assertEquals(a2["a"],      b["a"])
        self.assertEquals(a2["b"]["b"], [0, 1, 2, 3, 4, 5])
        self.assertEquals(a2["b"]["c"], a["b"]["c"])
        self.assertEquals(a2["b"]["d"], b["b"]["d"])

# vim:sw=4:ts=4:et:
