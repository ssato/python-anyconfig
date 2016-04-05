#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anyconfig.backend.tests.ini
try:
    import anyconfig.backend.yaml as TT
except ImportError:
    TT = None

from anyconfig.compat import OrderedDict as ODict


CNF_0_S = """
a: 0
b: bbb
c:
  - 1
  - 2
  - 3

sect0:
  d: ["x", "y", "z"]
"""

CNF_0 = ODict((("a", 0), ("b", "bbb"), ("c", [1, 2, 3]),
               ("sect0", ODict((("d", "x y z".split()), )))))


if TT is not None:
    import yaml

    class Test10(anyconfig.backend.tests.ini.Test10):

        cnf = CNF_0
        cnf_s = CNF_0_S
        load_options = dict(ac_safe=True, Loader=yaml.loader.Loader)
        dump_options = dict(ac_safe=True)
        is_order_kept = False  # ..note:: yaml backend cannot do this yet.

        def setUp(self):
            self.psr = TT.Parser()

    class Test20(anyconfig.backend.tests.ini.Test20):

        psr_cls = TT.Parser
        cnf = CNF_0
        cnf_s = CNF_0_S
        cnf_fn = "test0.yml"
        # load_options = Test10.load_options
        # dump_options = Test20.load_options

# vim:sw=4:ts=4:et:
