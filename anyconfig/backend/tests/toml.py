#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import datetime
import unittest

import anyconfig.backend.toml as TT
import anyconfig.tests.common

from anyconfig.tests.common import dicts_equal


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


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anyconfig.tests.common.setup_workdir()
        self.cpath = os.path.join(self.workdir, "test0.toml")
        self.cnf_s = CNF_S
        self.cnf = CNF
        open(self.cpath, 'w').write(self.cnf_s)

    def tearDown(self):
        anyconfig.tests.common.cleanup_workdir(self.workdir)

    def test_10_loads(self):
        cnf = TT.Parser.loads(self.cnf_s)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_20_load(self):
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

    def test_30_dumps(self):
        cnf = TT.Parser.loads(self.cnf_s)
        cnf2 = TT.Parser.loads(TT.Parser.dumps(cnf))
        self.assertTrue(dicts_equal(cnf2, cnf), str(cnf2))

    def test_40_dump(self):
        cnf = TT.Parser.loads(self.cnf_s)
        TT.Parser.dump(cnf, self.cpath)
        cnf = TT.Parser.load(self.cpath)
        self.assertTrue(dicts_equal(cnf, self.cnf), str(cnf))

# vim:sw=4:ts=4:et:
