#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anyconfig.backend.properties as TT
import anyconfig.backend.tests.ini


CNF_S = """
a = 0
b = bbb

sect0.c = x;y;z
sect1.d = \\
    1,2,3
"""
CNF = {"a": "0", "b": "bbb", "sect0.c": "x;y;z",
       "sect1.d": "1,2,3"}


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF
    cnf_s = CNF_S
    load_options = dict(comment_markers=("//", "#", "!"))
    dump_options = dict(dummy_opt="this_will_be_ignored")

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF
    cnf_s = CNF_S
    cnf_fn = "conf.properties"

# vim:sw=4:ts=4:et:
