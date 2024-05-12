#
# Copyright (C) 2018 - 2024 Satoru SATOH <satoru.satoh gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Test cases for anyconfig.processors.utils."""
from __future__ import annotations

import typing

import pytest

import anyconfig.ioinfo
import anyconfig.processors.utils as TT

from anyconfig.common import (
    UnknownFileTypeError, UnknownProcessorTypeError
)
from .common import A, A2, A3, B, C, PRS

if typing.TYPE_CHECKING:
    import collections.abc


PRS = [p() for p in PRS]  # Instantiate all.


@pytest.mark.parametrize(
    ("items", "exp"),
    (([], []),
     (((["a"], 1), ), [("a", [1])]),
     (((["a", "aaa"], 1), (["b", "bb"], 2), (["a"], 3)),
      [("a", [1, 3]), ("aaa", [1]), ("b", [2]), ("bb", [2])])
     ),
)
def test_select_by_key(
    items: collections.abc.Iterable, exp: collections.abc.Iterable
):
    assert TT.select_by_key(items) == exp


@pytest.mark.parametrize(
    ("items", "exp"),
    ((((["a", "aaa"], 1), (["a"], 3)), [("a", [3, 1]), ("aaa", [1])]),
     ),
)
def test_select_by_key_reversed(
    items: collections.abc.Iterable, exp: collections.abc.Iterable
):
    def sfn(itr):
        return sorted(itr, reverse=True)

    assert TT.select_by_key(items, sfn) == exp


PRS10 = (AI0, AI2, AI3, BI0, CI0) = (A(), A2(), A3(), B(), C())
OBJ0 = anyconfig.ioinfo.make("/path/to/a.json")


@pytest.mark.parametrize(
    ("items", "exp"),
    ((([], "type"), []),
     (([AI0], "type"), [(AI0.type(), [AI0])]),
     (([AI0], "extensions"), [(x, [AI0]) for x in AI0.extensions()]),
     (((AI0, AI2, AI3), "type"), [(AI0.type(), [AI3, AI2, AI0])]),
     (([AI0, BI0, CI0], "type"),
      [(AI0.type(), [AI0]), (BI0.type(), [BI0, CI0])]),
     ((PRS, "type"),
      [(AI0.type(), [AI3, AI2, AI0]), (BI0.type(), [BI0, CI0])]),
     ((PRS, "extensions"),
      [("js", [AI3, AI2, AI0]), ("json", [AI3, AI2, AI0]),
       ("jsn", [AI3, AI2, AI0]), ("yaml", [BI0, CI0]), ("yml", [BI0, CI0])]),
     ),
)
def test_list_by_x(
    items: collections.abc.Iterable, exp: collections.abc.Iterable
) -> None:
    assert sorted(TT.list_by_x(*items)) == sorted(exp)


def test_list_by_x_ng_cases():
    with pytest.raises(ValueError):
        TT.list_by_x(PRS, "undef")


@pytest.mark.parametrize(
    ("typ", "exp"),
    (("json", [AI3, AI2, AI0]),
     ("yaml", [BI0, CI0]),
     ("undefined", [])
     ),
)
def test_findall_with_pred__type(
    typ: str, exp: collections.abc.Iterable
) -> None:
    def _findall_by_type(typ):
        return TT.findall_with_pred(lambda p: p.type() == typ, PRS)

    assert _findall_by_type(typ) == exp


@pytest.mark.parametrize(
    ("typ", "exp"),
    (("js", [AI3, AI2, AI0]),
     ("yml", [BI0, CI0]),
     ("xyz", []),
     ),
)
def test_findall_with_pred__ext(
    typ: str, exp: collections.abc.Iterable
) -> None:
    def _findall_with_pred__ext(ext):
        return TT.findall_with_pred(lambda p: ext in p.extensions(), PRS)

    assert _findall_with_pred__ext(typ) == exp


@pytest.mark.parametrize(
    ("items", "exp"),
    (((AI3, A3), True),
     ((A3, A3), True),
     ((B, A3), False),
     ),
)
def test_maybe_processor(
    items: collections.abc.Iterable, exp: bool
) -> None:
    res = TT.maybe_processor(*items)
    if exp:
        assert isinstance(res, A3)
    else:
        assert not isinstance(res, A3)
        assert res is None


@pytest.mark.parametrize(
    ("typ_prs", "exp"),
    ((("json", PRS), [AI3, AI2, AI0]),
     (("yaml", PRS), [BI0, CI0]),
     (("dummy", PRS), [CI0]),
     ),
)
def test_find_by_type_or_id(
    typ_prs: collections.abc.Iterable, exp: collections.abc.Iterable
) -> None:
    assert TT.find_by_type_or_id(*typ_prs) == exp


def test_find_by_type_or_id_ng_cases() -> None:
    with pytest.raises(UnknownProcessorTypeError):
        TT.find_by_type_or_id("xyz", PRS)


@pytest.mark.parametrize(
    ("typ_prs", "exp"),
    ((("js", PRS), [A3(), A2(), A()]),
     (("yml", PRS), [B(), C()]),
     ),
)
def test_find_by_fileext(
    typ_prs: collections.abc.Iterable, exp: collections.abc.Iterable
) -> None:
    assert TT.find_by_fileext(*typ_prs) == exp


def test_find_by_fileext_ng_cases():
    with pytest.raises(UnknownFileTypeError):
        TT.find_by_fileext("xyz", PRS)


@pytest.mark.parametrize(
    ("objs", "exp"),
    ((("/path/to/a.jsn", PRS), [AI3, AI2, AI0]),
     (("../../path/to/b.yml", PRS), [BI0, CI0]),
     ((OBJ0, PRS), [AI3, AI2, AI0]),
     )
)
def test_find_by_maybe_file(objs, exp):
    assert TT.find_by_maybe_file(*objs) == exp


@pytest.mark.parametrize(
    ("obj", ),
    (("/tmp/x.xyz", ),
     ("/dev/null", ),
     )
)
def test_find_by_maybe_file_ng_cases(obj):
    with pytest.raises(UnknownFileTypeError):
        TT.find_by_maybe_file(obj, PRS)


@pytest.mark.parametrize(
    ("obj", "typ", "exc"),
    ((None, None, ValueError),  # w/o path nor type
     ("/tmp/x.xyz", None, UnknownFileTypeError),
     ("/dev/null", None, UnknownFileTypeError),
     (None, "xyz", UnknownProcessorTypeError),
     )
)
def test_findall_ng_cases(obj, typ, exc):
    with pytest.raises(exc):
        TT.findall(obj, PRS, forced_type=typ)


@pytest.mark.parametrize(
    ("obj", "exp"),
    (("/path/to/a.jsn", [AI3, AI2, AI0]),
     ("../../path/to/b.yml", [BI0, CI0]),
     (OBJ0, [AI3, AI2, AI0]),
     )
)
def test_findall_by_maybe_file(obj, exp):
    assert TT.findall(obj, PRS) == exp


@pytest.mark.parametrize(
    ("typ", "exp"),
    (("json", [AI3, AI2, AI0]),
     ("yaml", [BI0, CI0]),
     ("dummy", [CI0]),
     )
)
def test_findall_by_type_or_id(typ, exp):
    assert TT.findall(None, PRS, forced_type=typ) == exp


@pytest.mark.parametrize(
    ("typ", "exp"),
    ((A2, AI2),
     (CI0.cid(), CI0),
     )
)
def test_find_by_forced_type(typ, exp):
    assert TT.find(None, PRS, forced_type=typ) == exp


@pytest.mark.parametrize(
    ("obj", "exp"),
    (("/path/to/a.jsn", AI3),
     ("../../path/to/b.yml", BI0),
     (OBJ0, AI3),
     )
)
def test_find__maybe_file(obj, exp):
    assert TT.find(obj, PRS) == exp


@pytest.mark.parametrize(
    ("typ", "exp"),
    (("json", A3()),
     ("yaml", B()),
     ("dummy", C()),
     )
)
def test_find__type_or_id(typ, exp):
    assert TT.find(None, PRS, forced_type=typ) == exp
