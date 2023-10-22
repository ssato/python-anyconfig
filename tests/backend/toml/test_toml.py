#
# Copyright (C) 2023 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=raise-missing-from
import tests.backend.common as TBC
try:
    import anyconfig.backend.toml.toml as TT
except ImportError:
    import unittest
    raise unittest.SkipTest

from .common import CNF


def odict_to_dict(obj):
    try:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, dict):
            return {k: odict_to_dict(v) for k, v in obj.items()}
        # other iterables.
        return [odict_to_dict(e) for e in obj]
    except TypeError:
        return obj


CNF["owner"]["dob"] = TT.toml.loads("dob = 1979-05-27T07:32:00Z")['dob']


class HasParserTrait(TBC.HasParserTrait):
    psr = TT.Parser()

    # convert collections.OrderedDict object to dict object.
    cnf = odict_to_dict(CNF)
    cnf_s = TBC.read_from_res("20-00-cnf.toml")


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):
    load_options = dump_options = {"dummy": "this_will_be_ignored"}


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):
    pass

# vim:sw=4:ts=4:et:
