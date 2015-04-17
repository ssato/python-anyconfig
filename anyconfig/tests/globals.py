#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import logging
import unittest
import anyconfig.globals as TT


class Test_00(unittest.TestCase):

    def test_00(self):
        self.assertTrue(isinstance(TT.LOGGER, logging.Logger))

# vim:sw=4:ts=4:et:
