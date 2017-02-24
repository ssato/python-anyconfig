#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

try:
    import anyconfig.backend.cbor as TT
except ImportError:
    TT = None

import anyconfig.backend.tests.ini


if TT is not None:
    class Test10(anyconfig.backend.tests.ini.Test10):

        cnf = dict(a=0, b="bbb", c=5, sect0=dict(d=["x", "y", "z"]))
        cnf_s = TT.cbor.dumps(cnf)
        load_options = dump_options = dict(sort_keys=False)
        is_order_kept = False

        def setUp(self):
            self.psr = TT.Parser()


# pylint: disable=pointless-string-statement
""" TODO:
class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = CNF_0_S
    cnf_fn = "conf0.cbor"

    def test_22_dump__w_special_option(self):
        self.psr.dump(self.cnf, self.cpath, sort_keys=True)
        cnf = self.psr.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))
"""

# vim:sw=4:ts=4:et:
