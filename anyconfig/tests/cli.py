#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.cli as T
import anyconfig.api as A
import anyconfig.tests.common as C

import os
import os.path
import unittest


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10__no_args(self):
        """FIXME: no args test case"""
        pass

    def test_20__list(self):
        """FIXME: '--list' test case"""
        pass

    def test_30_single_input(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"))

        input = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        A.dump(a, input)
        self.assertTrue(os.path.exists(input))

        T.main(["dummy", "-o", output, input])
        self.assertTrue(os.path.exists(output))

    def test_40_multiple_inputs(self):
        xs = [dict(a=1, ),
              dict(b=dict(b=[1, 2], c="C")), ]

        a = xs[0].copy()
        a.update(xs[1])

        output = os.path.join(self.workdir, "b.json")

        inputs = []
        for i in [0, 1]:
            input = os.path.join(self.workdir, "a%d.json" % i)
            inputs.append(input)

            A.dump(xs[i], input)
            self.assertTrue(os.path.exists(input))

        T.main(["dummy", "-o", output] + inputs)
        self.assertTrue(os.path.exists(output))

    def test_50_single_input__w_arg_option(self):
        a = dict(name="a", a=1, b=dict(b=[1, 2], c="C"), d=[1, 2])

        input = os.path.join(self.workdir, "a.json")
        output = os.path.join(self.workdir, "b.json")

        A.dump(a, input)
        self.assertTrue(os.path.exists(input))

        T.main(["dummy", "-o", output, "-A", "a:10;name:x;d:3,4", input])
        self.assertTrue(os.path.exists(output))

        x = A.load(output)

        self.assertNotEquals(a["name"], x["name"])
        self.assertNotEquals(a["a"], x["a"])
        self.assertNotEquals(a["d"], x["d"])

        self.assertEquals(x["name"], u'x')
        self.assertEquals(x["a"], 10)
        self.assertEquals(x["d"], [3, 4])

# vim:sw=4:ts=4:et:
