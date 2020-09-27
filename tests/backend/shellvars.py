#
# Copyright (C) 2016 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

from collections import OrderedDict

import anyconfig.backend.shellvars as TT
import tests.backend.common as TBC


CNF = OrderedDict((("a", "0"), ("b", "bbb"), ("c", "ccc"), ("d", "ddd"),
                   ("e", "eee")))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = TBC.read_from_res("20-00-cnf.sh")


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    pass


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
