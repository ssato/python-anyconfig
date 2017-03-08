#
# Copyright (C) 2016 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import anyconfig.backend.shellvars as TT
import tests.backend.common as TBC

from anyconfig.compat import OrderedDict


CNF_S = """\
a=0
b='bbb'   # a comment
c="ccc"   # an another comment
export d='ddd'  ## double comment
 export e="eee" ### tripple comment
"""
CNF = OrderedDict((("a", "0"), ("b", "bbb"), ("c", "ccc"), ("d", "ddd"),
                   ("e", "eee")))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = CNF_S


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    pass


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
