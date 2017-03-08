#
# Copyright (C) 2015 - 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import anyconfig.backend.bson as TT
import tests.backend.common as TBC

from anyconfig.compat import OrderedDict
from tests.common import to_bytes as _bytes


CNF_0 = OrderedDict((("a", 0.1), ("b", _bytes("bbb")),
                     ("sect0", OrderedDict((("c", [_bytes("x"), _bytes("y"),
                                                   _bytes("z")]), )))))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF_0
    cnf_s = TT.bson.BSON.encode(cnf)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    # Can't if bson.has_c():
    # load_options = dict(as_class=dict)
    # dump_options = dict(check_keys=True)
    pass


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
