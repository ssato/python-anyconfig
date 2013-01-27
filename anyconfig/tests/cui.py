#
# Copyright (C) 2013 Satoru SATOH <ssato at redhat.com>
#
import anyconfig.cui as T
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

# vim:sw=4:ts=4:et:
