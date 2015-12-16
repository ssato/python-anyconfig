#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import anyconfig.utils as TT


class Test(unittest.TestCase):

    def test_00_get_file_extension(self):
        self.assertEqual(TT.get_file_extension("/a/b/c"), '')
        self.assertEqual(TT.get_file_extension("/a/b.txt"), "txt")
        self.assertEqual(TT.get_file_extension("/a/b/c.tar.xz"), "xz")

# vim:sw=4:ts=4:et:
