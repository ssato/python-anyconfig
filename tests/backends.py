#
# Copyright (C) 2012 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import pathlib
import unittest

import anyconfig.backend.json
import anyconfig.backend.json.default as JSON
try:
    import anyconfig.backend.yaml.pyyaml as PYYAML
except ImportError:
    PYYAML = None

import anyconfig.backends as TT
import anyconfig.ioinfo
import tests.common as TC

from anyconfig.globals import (
    UnknownProcessorTypeError, UnknownFileTypeError
)


CNF_PATH = TC.respath('00-cnf.json')


class Test(unittest.TestCase):

    def setUp(self):
        self.psrs = TT.Parsers()

    def test_10_json_parsers(self):
        jpsrs = self.psrs.findall(None, forced_type="json")
        self.assertTrue(isinstance(jpsrs[0], JSON.Parser))

    def test_12_yaml_parsers(self):
        if PYYAML:
            ypsrs = self.psrs.findall(None, forced_type="yaml")
            self.assertTrue(isinstance(ypsrs[0], PYYAML.Parser))

    def test_30_find__ng_cases(self):
        self.assertRaises(ValueError, self.psrs.find, None)
        self.assertRaises(UnknownProcessorTypeError, self.psrs.find, None,
                          forced_type="_unkonw_type_")
        self.assertRaises(UnknownFileTypeError, self.psrs.find,
                          "cnf.unknown_ext")

    def test_32_find__ng_cases(self):
        pcls = anyconfig.backend.json.Parser
        self.assertTrue(isinstance(self.psrs.find("x.conf",
                                                  forced_type="json"),
                                   pcls))
        self.assertTrue(isinstance(self.psrs.find("x.json"), pcls))

        with open(CNF_PATH) as inp:
            self.assertTrue(isinstance(self.psrs.find(inp), pcls))

        if pathlib is not None:
            inp = pathlib.Path("x.json")
            self.assertTrue(isinstance(self.psrs.find(inp), pcls))

    def test_34_find__input_object(self):
        inp = anyconfig.ioinfo.make(CNF_PATH)
        psr = self.psrs.find(inp)
        self.assertTrue(isinstance(psr, anyconfig.backend.json.Parser))

# vim:sw=4:ts=4:et:
