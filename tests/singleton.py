#
# Copyright (C) 2018 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, too-few-public-methods
import unittest
import anyconfig.singleton as TT


class TestSingleton(unittest.TestCase):

    def test_10_basic(self):
        class A(TT.Singleton):
            pass

        class B(TT.Singleton):
            pass

        (a1, a2) = (A(), A())
        (b1, b2) = (B(), B())
        self.assertTrue(a1 is a2)
        self.assertTrue(b1 is b2)
        self.assertTrue(a1 is not b1)

    def test_20_decendant(self):
        class A(TT.Singleton):
            pass

        class A2(A):
            pass

        (a1, a2) = (A(), A2())
        self.assertTrue(a1 is a2)

    def test_30_mixin(self):
        class Base:
            pass

        class A(Base, TT.Singleton):
            pass

        (a1, a2) = (A(), A())
        self.assertTrue(a1 is a2)

# vim:sw=4:ts=4:et:
