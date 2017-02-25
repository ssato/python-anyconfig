#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import unittest

import anyconfig.backends as TT
import anyconfig.backend.ini
import anyconfig.backend.json

try:
    import anyconfig.backend.yaml
    YAML_FOUND = True
except ImportError:
    YAML_FOUND = False


class Test(unittest.TestCase):

    def test_10_find_by_file(self):
        ini_cf = "/a/b/c.ini"
        unknown_cf = "/a/b/c.xyz"
        jsn_cfs = ["/a/b/c.jsn", "/a/b/c.json", "/a/b/c.js"]
        yml_cfs = ["/a/b/c.yml", "/a/b/c.yaml"]

        self.assertTrue(TT.find_by_file(unknown_cf) is None)
        self.assertEqual(TT.find_by_file(ini_cf), anyconfig.backend.ini.Parser)

        for cfg in jsn_cfs:
            self.assertEqual(TT.find_by_file(cfg),
                             anyconfig.backend.json.Parser)

        if YAML_FOUND:
            for cfg in yml_cfs:
                self.assertEqual(TT.find_by_file(cfg),
                                 anyconfig.backend.yaml.Parser)

    def test_20_find_by_type(self):
        ini_t = "ini"
        jsn_t = "json"
        yml_t = "yaml"
        unknown_t = "unknown_type"

        self.assertTrue(TT.find_by_type(unknown_t) is None)
        self.assertEqual(TT.find_by_type(ini_t), anyconfig.backend.ini.Parser)
        self.assertEqual(TT.find_by_type(jsn_t), anyconfig.backend.json.Parser)

        if YAML_FOUND:
            self.assertEqual(TT.find_by_type(yml_t),
                             anyconfig.backend.yaml.Parser)

    def test_30_list_types(self):
        types = TT.list_types()

        self.assertTrue(isinstance(types, list))
        self.assertTrue(bool(list))  # ensure it's not empty.

# vim:sw=4:ts=4:et:
