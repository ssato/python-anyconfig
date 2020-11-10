#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

import os
import tests.backend.common as TBC
try:
    import anyconfig.backend.yaml.pyyaml as TT
except ImportError:
    import unittest
    raise unittest.SkipTest

from .common import CNF_S, CNF


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = CNF_S


class Test_00(TBC.unittest.TestCase):

    def test_yml_fnc_by_name(self):
        self.assertTrue(TT.yml_fnc_by_name("load", ac_safe=True),
                        TT.yaml.safe_load)
        self.assertTrue(TT.yml_fnc_by_name("dump", ac_safe=True, aaa=True),
                        TT.yaml.safe_dump)
        self.assertTrue(TT.yml_fnc_by_name("load", ac_safe=False),
                        TT.yaml.load)
        self.assertTrue(TT.yml_fnc_by_name("dump", ac_safe=False),
                        TT.yaml.dump)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dict(ac_safe=True, Loader=TT.yaml.loader.Loader)
    dump_options = dict(ac_safe=True)
    empty_patterns = [('', {}), (' ', {}), ('[]', []),
                      ("#%s#%s" % (os.linesep, os.linesep), {})]


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):
    pass

# vim:sw=4:ts=4:et:
