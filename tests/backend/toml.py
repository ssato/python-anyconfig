#
# Copyright (C) 2015 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

from collections import OrderedDict as ODict

try:
    import anyconfig.backend.toml as TT
except ImportError:
    import unittest
    raise unittest.SkipTest

import tests.backend.common as TBC


_DOB = TT.toml.loads("dob = 1979-05-27T07:32:00Z")['dob']

CNF = ODict((('title', 'TOML Example'),
             ('owner',
              ODict((('name', 'Tom Preston-Werner'),
                     ('dob', _DOB)))),
             ('database',
              ODict((('server', '192.168.1.1'),
                     ('ports', [8001, 8001, 8002]),
                     ('connection_max', 5000),
                     ('enabled', True)))),
             ('servers',
              ODict((('alpha',
                      ODict((('ip', '10.0.0.1'), ('dc', 'eqdc10')))),
                     ('beta',
                      ODict((('ip', '10.0.0.2'), ('dc', 'eqdc10'))))))),
             ('clients',
              ODict((('data', [['gamma', 'delta'], [1, 2]]),
                     ('hosts', ['alpha', 'omega']))))))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = TBC.read_from_res("20-00-cnf.toml")


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dump_options = dict(dummy="this_will_be_ignored")


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
