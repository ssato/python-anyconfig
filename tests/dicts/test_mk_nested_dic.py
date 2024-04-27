#
# Forked from m9dicts.tests.{api,dicts}
#
# Copyright (C) 2011 - 2024 Satoru SATOH <satoru.satoh gmail.com>
#
# pylint: disable=missing-docstring
from __future__ import annotations

import typing

import pytest

import anyconfig.dicts as TT

from . import common


DATASETS: list[tuple[typing.Any, dict[str, typing.Any]]] = [
    (obj, data) for _, obj, data in common.collect_data("mk_nested_dic")
]


@pytest.mark.parametrize(("obj", "data"), DATASETS)
def test_mk_nested_dic(obj, data):
    val = data.get("q")
    exp = data.get("e")
    opts = data.get("o")

    assert TT.mk_nested_dic(obj, val, **opts) == exp
