#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anyconfig.backend.json as TT
import anyconfig.backend.tests.ini

from anyconfig.tests.common import dicts_equal


CNF_0_S = """{
  "a": 0,
  "b": "bbb",

  "sect0": {
    "c": ["x", "y", "z"]
  }
}
"""

CNF_0 = {'a': 0, 'b': 'bbb', 'sect0': {'c': ['x', 'y', 'z']}}


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF_0
    cnf_s = CNF_0_S
    load_options = dump_options = dict(parse_int=None, indent=3)

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.json"

    def test_12_load__w_options(self):
        cnf = self.psr.load(self.cpath, parse_int=None)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_22_dump__w_special_option(self):
        self.psr.dump(self.cnf, self.cpath, parse_int=None, indent=3)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
