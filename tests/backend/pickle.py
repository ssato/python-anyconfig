#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

try:
    import anyconfig.backend.pickle as TT
except ImportError:
    TT = None

import tests.backend.ini
from tests.common import dicts_equal


CNF_0 = dict(a=0, b="bbb", c=5, sect0=dict(d=["x", "y", "z"]))


class Test10(tests.backend.ini.Test10):

    cnf = CNF_0
    cnf_s = TT.pickle.dumps(cnf)
    load_options = dump_options = dict(protocol=TT.pickle.HIGHEST_PROTOCOL)
    is_order_kept = False

    def setUp(self):
        self.psr = TT.Parser()


class Test20(tests.backend.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = TT.pickle.dumps(cnf, protocol=TT.pickle.HIGHEST_PROTOCOL)
    cnf_fn = "conf0.pkl"

    def test_22_dump__w_special_option(self):
        self.psr.dump(self.cnf, self.cpath,
                      protocol=TT.pickle.HIGHEST_PROTOCOL)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
