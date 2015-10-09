#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import datetime

import anyconfig.backend.toml as TT
import anyconfig.backend.tests.ini


# Taken from https://github.com/toml-lang/toml:
CNF_S = """title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

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

CNF = {'clients': {'data': [['gamma', 'delta'],
                            [1, 2]],
                   'hosts': ['alpha', 'omega']},
       'database': {'connection_max': 5000,
                    'enabled': True,
                    'ports': [8001, 8001, 8002],
                    'server': '192.168.1.1'},
       'owner': {'dob': datetime.datetime(1979, 5, 27, 7, 32),
                 'name': 'Tom Preston-Werner'},
       'servers': {'alpha': {'dc': 'eqdc10', 'ip': '10.0.0.1'},
                   'beta': {'dc': 'eqdc10', 'ip': '10.0.0.2'}},
       'title': 'TOML Example'}


class Test10(anyconfig.backend.tests.ini.Test10):

    cnf = CNF
    cnf_s = CNF_S
    load_options = dump_options = dict(dummy="this_will_be_ignored")

    def setUp(self):
        self.psr = TT.Parser()


class Test20(anyconfig.backend.tests.ini.Test20):

    cnf = CNF
    cnf_s = CNF_S
    cnf_fn = "cnf.toml"

    def setUp(self):
        super(Test20, self).setUp()
        self.psr = TT.Parser()

# vim:sw=4:ts=4:et:
