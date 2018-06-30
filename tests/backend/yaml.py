#
# Copyright (C) 2012 - 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import os
import anyconfig.backend.yaml as TT
import tests.backend.common as TBC

from anyconfig.compat import OrderedDict


CNF_S = """
a: 0
b: bbb
c:
  - 1
  - 2
  - 3

sect0: &sect0
  d: ["x", "y", "z"]
sect1:
  <<: *sect0
  e: true
"""

CNF = OrderedDict((("a", 0), ("b", "bbb"), ("c", [1, 2, 3]),
                   ("sect0", OrderedDict((("d", "x y z".split()), ))),
                   ("sect1", OrderedDict((("d", "x y z".split()),
                                          ("e", True))))))


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = CNF_S


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dict(ac_safe=True, Loader=TT.yaml.loader.Loader)
    dump_options = dict(ac_safe=True)
    empty_patterns = [('', {}), (' ', {}), ('[]', []),
                      ("#%s#%s" % (os.linesep, os.linesep), {})]


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    def test_18_load__list(self):
        if self.is_ready():
            # overwrite it.
            with self.psr.wopen(self.cnf_path) as out:
                out.write("- 1\n- 2\n")

            ioi = self._to_ioinfo(self.cnf_path)

            cnf = self.psr.load(ioi)
            self.assertTrue(cnf)
            self.assertEqual(cnf, [1, 2])

    def test_19_load__nested_list(self):
        if self.is_ready():
            with self.psr.wopen(self.cnf_path) as out:
                out.write('[{"a": 1}, {"a": 2}]\n')

            ioi = self._to_ioinfo(self.cnf_path)

            cnf = self.psr.load(ioi)
            self.assertTrue(cnf)
            self.assertEqual(cnf, [{"a": 1}, {"a": 2}])

# vim:sw=4:ts=4:et:
