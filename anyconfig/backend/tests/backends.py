#
# Copyright (C) 2012 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.backends as T
import unittest


class Test_00_pure_functions(unittest.TestCase):

    def test_10_find_by_file(self):
        ini_cf = "/a/b/c.ini"
        jsn_cf = "/a/b/c.jsn"
        yml_cf = "/a/b/c.yml"
        unknown_cf = "/a/b/c.xyz"

        def instchk(cf, cls):
            isinstance(T.find_by_file(cf), cls)

        self.assertTrue(ini_cf, T.BINI.IniConfigParser)
        self.assertTrue(jsn_cf, T.BJSON.JsonConfigParser)
        self.assertTrue(yml_cf, T.BYAML.YamlConfigParser)
        self.assertTrue(T.find_by_file(unknown_cf) is None)

    def test_20_find_by_type(self):
        ini_t = "ini"
        jsn_t = "json"
        yml_t = "yaml"
        unknown_t = "unknown_type"

        def instchk(cf, ctype):
            isinstance(T.find_by_type(ctype), cls)

        self.assertTrue(ini_t, T.BINI.IniConfigParser)
        self.assertTrue(jsn_t, T.BJSON.JsonConfigParser)
        self.assertTrue(yml_t, T.BYAML.YamlConfigParser)
        self.assertTrue(T.find_by_type(unknown_t) is None)

    def test_30_list_types(self):
        types = T.list_types()

        self.assertTrue(isinstance(types, list))
        self.assertTrue(bool(list))  # ensure it's not empty.

# vim:sw=4:ts=4:et:
