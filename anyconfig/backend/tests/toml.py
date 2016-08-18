#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anyconfig.backend.toml as TT
import anyconfig.backend.tests.ini

from anyconfig.compat import OrderedDict as ODict


# Taken from https://github.com/toml-lang/toml:
CNF_S = """title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00Z # First class dates

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"

  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

  [clients]
  data = [ ["gamma", "delta"], [1, 2] ]

hosts = [
  "alpha",
  "omega"
]
"""

_DOB = TT.toml.loads("dob = 1979-05-27T07:32:00Z")['dob']

CNF = ODict((('clients',
              ODict((('data', [['gamma', 'delta'], [1, 2]]),
                     ('hosts', ['alpha', 'omega'])))),
             ('database',
              ODict((('connection_max', 5000),
                     ('enabled', True),
                     ('ports', [8001, 8001, 8002]),
                     ('server', '192.168.1.1')))),
             ('owner',
              ODict((('dob', _DOB),
                     ('name', 'Tom Preston-Werner')))),
             ('servers',
              ODict((('alpha',
                      ODict((('dc', 'eqdc10'), ('ip', '10.0.0.1')))),
                     ('beta',
                      ODict((('dc', 'eqdc10'), ('ip', '10.0.0.2'))))))),
             ('title', 'TOML Example')))


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF
    cnf_s = CNF_S
    load_options = dump_options = dict(dummy="this_will_be_ignored")
    is_order_kept = False  # ..note:: toml backend cannot do this yet.

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    psr_cls = TT.Parser
    cnf = CNF
    cnf_s = CNF_S
    cnf_fn = "cnf.toml"

# vim:sw=4:ts=4:et:
