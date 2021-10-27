#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=protected-access
"""Test cases for .backend.ini."""
import pytest

import anyconfig.backend.ini as TT
import tests.backend.common as TBC


@pytest.mark.parametrize(
    ('inp', 'exp'),
    (
     (r'"foo string"', 'foo string'),
     ('a, b, c', ['a', 'b', 'c']),
     ('aaa', 'aaa'),
     ),
)
def test_parse(inp, exp):
    assert TT.parse(inp) == exp


@pytest.mark.parametrize(
    'inp,exp',
    (
     ([1, 2, 3], '1, 2, 3'),
     ('aaa', 'aaa'),
     ),
)
def test_to_s(inp, exp):
    assert TT._to_s(inp) == exp


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf_s = TBC.read_from_res("20-00-cnf.ini")


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    load_options = dict(allow_no_value=False, defaults=None)

    def test_42_loads_invalid_input(self):
        invalid_cnf_s = "key=name"  # No section.
        self.assertRaises(Exception, self.psr.loads, invalid_cnf_s)

    def test_44_loads_with_ac_parse_value_option(self):
        cnf = self.psr.loads(self.cnf_s, ac_parse_value=True)
        ref = self.psr.loads(self.cnf_s)
        ref["DEFAULT"]["a"] = ref["sect0"]["a"] = 0
        ref["DEFAULT"]["c"] = ref["sect0"]["c"] = 5
        ref["sect0"]["d"] = ref["sect0"]["d"].split(',')
        self._assert_dicts_equal(cnf, ref=ref)


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
