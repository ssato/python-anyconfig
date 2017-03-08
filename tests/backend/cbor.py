#
# Copyright (C) 2017 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

try:
    import anyconfig.backend.cbor as TT
except ImportError:
    TT = None

import tests.backend.common as TBC


if TT is not None:
    class HasParserTrait(TBC.HasParserTrait):

        psr = TT.Parser()
        cnf = dict(a=0, b="bbb", c=5, sect0=dict(d=["x", "y", "z"]))
        cnf_s = TT.cbor.dumps(cnf)

    class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

        load_options = dump_options = dict(sort_keys=False)

    class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

        pass

# vim:sw=4:ts=4:et:
