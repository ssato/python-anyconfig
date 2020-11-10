#
# Copyright (C) - 2018, 2019 Satoru SATOH <satoru.satoh@gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

import os
import tests.backend.common as TBC
try:
    import anyconfig.backend.yaml.pyyaml as TT
except ImportError:
    import unittest
    raise unittest.SkipTest

from .common import CNF_S, CNF


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = CNF
    cnf_s = CNF_S

    opts = dict(typ="rt", pure=True,
                preserve_quotes=True,
                indent=dict(mapping=4, sequence=4, offset=2))

    setattr(psr, "_dict_opts", opts)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):  # noqa: N801

    load_options = dict(ac_safe=True, Loader=TT.yaml.loader.Loader)
    dump_options = dict(ac_safe=True)
    empty_patterns = [('', {}), (' ', {}), ('[]', []),
                      ("#%s#%s" % (os.linesep, os.linesep), {})]


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):  # noqa: N801

    pass

# vim:sw=4:ts=4:et:
