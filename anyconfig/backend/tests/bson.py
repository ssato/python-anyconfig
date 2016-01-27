#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import anyconfig.backend.bson as TT
import anyconfig.backend.tests.ini

from anyconfig.compat import OrderedDict as ODict, IS_PYTHON_3
from anyconfig.tests.common import to_bytes as _bytes


CNF_0 = ODict((("a", 0.1), ("b", _bytes("bbb")),
               ("sect0",
                ODict((("c", [_bytes("x"), _bytes("y"), _bytes("z")]), )))))


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF_0
    cnf_s = TT.bson.BSON.encode(CNF_0)
    load_options = dict(as_class=dict)
    dump_options = dict(check_keys=True)

    if IS_PYTHON_3:
        is_order_kept = False  # FIXME: Make it work w/ python 3.

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF_0
    cnf_s = TT.bson.BSON.encode(CNF_0)
    cnf_fn = "conf0.bson"

# vim:sw=4:ts=4:et:
