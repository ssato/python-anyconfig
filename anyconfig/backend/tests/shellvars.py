#
# Copyright (C) 2016 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import
import anyconfig.backend.shellvars as TT
import anyconfig.backend.tests.ini

from anyconfig.compat import OrderedDict as ODict


CNF_S = """
a=0
b='bbb'   # a comment
c="ccc"   # an another comment
"""
CNF = ODict((("a", "0"), ("b", "bbb"), ("c", "ccc")))


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF
    cnf_s = CNF_S

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF
    cnf_s = CNF_S
    cnf_fn = "conf.sh"

# vim:sw=4:ts=4:et:
