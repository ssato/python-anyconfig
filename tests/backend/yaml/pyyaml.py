#
# Copyright (C) 2012 - 2019 Satoru SATOH <satoru.satoh@gmail.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

import os
import tests.backend.common as TBC
try:
    import anyconfig.backend.yaml.pyyaml as TT
except ImportError:
    import tests.common
    tests.common.skip_test()

from .common import CNF_S, CNF


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
    pass

# vim:sw=4:ts=4:et:
