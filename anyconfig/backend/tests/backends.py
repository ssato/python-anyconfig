#
# Copyright (C) 2012 - 2014 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import anyconfig.backend.backends as T
import random
import unittest


class Test_00_pure_functions(unittest.TestCase):

    def test_10_find_by_file(self):
        ini_cf = "/a/b/c.ini"
        unknown_cf = "/a/b/c.xyz"
        jsn_cfs = ["/a/b/c.jsn", "/a/b/c.json", "/a/b/c.js"]
        yml_cfs = ["/a/b/c.yml", "/a/b/c.yaml"]

        self.assertTrue(ini_cf, T.BINI.IniConfigParser)
        self.assertTrue(T.find_by_file(unknown_cf) is None)

        for f in jsn_cfs:
            self.assertTrue(f, T.BJSON.JsonConfigParser)

        for f in yml_cfs:
            self.assertTrue(f, T.BYAML.YamlConfigParser)

    def test_20_find_by_type(self):
        ini_t = "ini"
        jsn_t = "json"
        yml_t = "yaml"
        unknown_t = "unknown_type"

        self.assertTrue(ini_t, T.BINI.IniConfigParser)
        self.assertTrue(jsn_t, T.BJSON.JsonConfigParser)
        self.assertTrue(yml_t, T.BYAML.YamlConfigParser)
        self.assertTrue(T.find_by_type(unknown_t) is None)

    def test_30_list_types(self):
        types = T.list_types()

        self.assertTrue(isinstance(types, list))
        self.assertTrue(bool(list))  # ensure it's not empty.

    def test_40_cmp_cps(self):
        cps = T._CPs
        if cps:
            x = T.cmp_cps(random.choice(cps), random.choice(cps))
            self.assertTrue(x in (-1, 0, 1))

# vim:sw=4:ts=4:et:
