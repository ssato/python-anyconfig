#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
json = None
import anyconfig.tests.common as C
C.mask_modules("json")

import anyconfig.backend.json_ as T
import unittest


# FIXME:
class Test_00_JsonConfigParser(unittest.TestCase):

    def test_00(self):
        # self.assertFalse(T.SUPPORTED)
        pass

    def test_10_load(self):
        # self.assertEquals(T.JsonConfigParser.load_impl("/dev/null"), {})
        pass

    def test_40_dump(self):
        # T.JsonConfigParser.dump({}, "/file/not/exist")
        T.JsonConfigParser

# vim:sw=4:ts=4:et:
