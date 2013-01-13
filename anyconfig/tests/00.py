#
# Copyright (C) 2012 Satoru SATOH <ssato at redhat.com>
#
import anyconfig as A
import anyconfig.Bunch as B
import anyconfig.tests.common as C

import os.path
import unittest


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        pass  # C.cleanup_workdir(self.workdir)

    def test_10_dump_and_load(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))

        a_path = os.path.join(self.workdir, "a.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        a1 = A.load(a_path)

        # FIXME: Too verbose
        self.assertEquals(a.name, a1.name)
        self.assertEquals(a.a, a1.a)
        self.assertEquals(a.b.b, a1.b.b)
        self.assertEquals(a.b.c, a1.b.c)

    def test_20_dump_and_multi_load(self):
        a = B.Bunch(name="a", a=1, b=B.Bunch(b=[1, 2], c="C"))
        b = B.Bunch(a=2, b=B.Bunch(b=[1, 2, 3, 4, 5], d="D"))

        a_path = os.path.join(self.workdir, "a.json")
        b_path = os.path.join(self.workdir, "b.json")

        A.dump(a, a_path)
        self.assertTrue(os.path.exists(a_path))

        A.dump(b, b_path)
        self.assertTrue(os.path.exists(b_path))

        x = A.multi_load([a_path, b_path], merge=A.MS_DICTS)

        # FIXME: Too verbose
        self.assertEquals(a.name, x.name)
        self.assertEquals(b.a, x.a)
        self.assertEquals(b.b.b, x.b.b)
        self.assertEquals(a.b.c, x.b.c)
        self.assertEquals(b.b.d, x.b.d)

        x = A.multi_load([a_path, b_path])

        self.assertEquals(a.name, x.name)
        self.assertEquals(b.a, x.a)
        self.assertEquals([1, 2, 3, 4, 5], x.b.b)
        self.assertEquals(a.b.c, x.b.c)
        self.assertEquals(b.b.d, x.b.d)

# vim:sw=4:ts=4:et:
