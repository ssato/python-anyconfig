#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.base as T  # stands for test target
import unittest


class Test_00_ConfigParser(unittest.TestCase):

    def test_10_type(self):
        self.assertEquals(T.ConfigParser.type(), T.ConfigParser._type)

    def test_10_type__force_set(self):
        T.ConfigParser._type = 1
        self.assertEquals(T.ConfigParser.type(), 1)

# vim:sw=4:ts=4:et:
