#
# Copyright (C) 2012 - 2024 Satoru SATOH <satoru.satoh @ gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=ungrouped-imports,protected-access
import io

import pytest

import anyconfig.backend.properties.builtin as TT

from collections import OrderedDict


CNF = OrderedDict((("a", "0"), ("b", "bbb"), ("c", ""),
                   ("sect0.c", "x;y;z"), ("sect1.d", "1,2,3"),
                   ("d", "val1,val2,val3")))


@pytest.mark.parametrize(
    "inp,exp",
    ((" ", (None, "")),
     ("aaa", ("aaa", "")),
     ),
)
def test_parseline_warnings(inp, exp):
    with pytest.warns(SyntaxWarning):
        assert TT.parseline(inp) == exp


@pytest.mark.parametrize(
    "inp,exp",
    (("aaa:", ("aaa", "")),
     (" aaa:", ("aaa", "")),
     ("url = http://localhost", ("url", "http://localhost")),
     ("calendar.japanese.type: LocalGregorianCalendar",
      ("calendar.japanese.type", "LocalGregorianCalendar")),
     ),
)
def test_parseline(inp, exp):
    assert TT.parseline(inp) == exp


@pytest.mark.parametrize(
    "inp,exp",
    (("", None),
     ("a: A", "a: A"),
     ("# a: A", None),
     ("! a: A", None),
     ("a: A # comment", "a: A # comment"),
     ),
)
def test_pre_process_line(inp, exp):
    assert TT._pre_process_line(inp) == exp


@pytest.mark.parametrize(
    "inp,exp",
    ((r"aaa\:bbb", "aaa:bbb"),
     (r"\\a", r"\a"),
     ),
)
def test_10_unescape(inp, exp):
    assert TT.unescape(inp) == exp


@pytest.mark.parametrize(
    "inp,exp",
    ((r":=\ ", r"\:\=\\ "),
     ),
)
def test_escape(inp, exp):
    assert TT.escape(inp) == exp


@pytest.mark.parametrize(
    "inp,exp",
    ((":", "\\:"),
     ("=", "\\="),
     ("a", "a"),
     ),
)
def test_escape_char(inp, exp):
    assert TT._escape_char(inp) == exp


KEY_0 = "calendar.japanese.type"
VAL_0 = "LocalGregorianCalendar"
KV_0 = f"{KEY_0}: {VAL_0}"
KV_1 = """application/postscript: \\
x=Postscript File;y=.eps,.ps
"""


@pytest.mark.parametrize(
    "inp,exp",
    (("", {}),
     (f"# {KV_0}", {}),
     (f"! {KV_0}", {}),
     (f"{KEY_0}:", {KEY_0: ""}),
     (KV_0, {KEY_0: VAL_0}),
     (f"{KV_0}# ...", {KEY_0: f"{VAL_0}# ..."}),
     ("key=a\\:b", {"key": "a:b"}),
     (KV_1, {"application/postscript": "x=Postscript File;y=.eps,.ps"}),
     ),
)
def test_load(inp, exp):
    assert TT.load(io.StringIO(inp)) == exp
