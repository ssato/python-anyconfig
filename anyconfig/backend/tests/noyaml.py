#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
yaml = None
import anyconfig.tests.common as C
C.mask_modules("yaml")

import anyconfig.backend.yaml_ as T
import unittest


# FIXME:
class Test_YamlConfigParser(unittest.TestCase):

    def test_00(self):
        # self.assertFalse(T.SUPPORTED)
        pass

    def test_10_load(self):
        # self.assertEquals(T.YamlConfigParser.load_impl("/dev/null"), {})
        pass

    def test_40_dump(self):
        # T.YamlConfigParser.dump({}, "/file/not/exist")
        T.YamlConfigParser.dump

# vim:sw=4:ts=4:et:
