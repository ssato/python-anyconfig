#
# Copyright (C) - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports
from __future__ import absolute_import

import os
import anyconfig.backend.yaml.pyyaml as TT
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

    opts = dict(typ="rt", pure=True,
                preserve_quotes=True,
                indent=dict(mapping=4, sequence=4, offset=2))

    setattr(psr, "dict_options", opts)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):  # noqa: N801

    load_options = dict(ac_safe=True, Loader=TT.yaml.loader.Loader)
    dump_options = dict(ac_safe=True)
    empty_patterns = [('', {}), (' ', {}), ('[]', []),
                      ("#%s#%s" % (os.linesep, os.linesep), {})]


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):  # noqa: N801

    pass

# vim:sw=4:ts=4:et:
