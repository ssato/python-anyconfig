#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.utils as U
import unittest


class Test_functions(unittest.TestCase):

    def test_00_get_file_extension(self):
        self.assertEquals(U.get_file_extension("/a/b/c"), '')
        self.assertEquals(U.get_file_extension("/a/b.txt"), "txt")
        self.assertEquals(U.get_file_extension("/a/b/c.tar.xz"), "xz")


# vim:sw=4:ts=4:et:
