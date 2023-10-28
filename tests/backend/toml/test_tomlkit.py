#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=raise-missing-from
import tests.backend.common as TBC
try:
    import anyconfig.backend.toml.tomlkit as TT
except ImportError:
    import unittest
    raise unittest.SkipTest

from .common import CNF


CNF["owner"]["dob"] = TT.tomlkit.loads("dob = 1979-05-27T07:32:00Z")['dob']


class HasParserTrait(TBC.HasParserTrait):
    psr = TT.Parser()
    cnf = CNF
    cnf_s = TBC.read_from_res("20-00-cnf.toml")


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):
    load_options = dump_options = {"dummy": "this_will_be_ignored"}


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):
    pass

# vim:sw=4:ts=4:et:
